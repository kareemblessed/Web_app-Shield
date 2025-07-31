"""
PayShield Storage Manager - Corrected Version
"""

import asyncio
import json
import logging
import hashlib
import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
import redis.asyncio as redis
import asyncpg
from dataclasses import dataclass, asdict
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VendorProfile:
    """Vendor voice profile data structure"""
    email: str
    company_name: str
    contact_name: str
    voiceprint_hash: str
    enrollment_date: datetime
    last_verification: Optional[datetime] = None
    verification_count: int = 0
    confidence_threshold: float = 92.0
    expires_at: Optional[datetime] = None

    def __post_init__(self):
        if self.expires_at is None:
            self.expires_at = self.enrollment_date + timedelta(days=90)

@dataclass
class VerificationAttempt:
    """Voice verification attempt record"""
    id: str
    vendor_email: str
    thread_id: str
    challenge_words: str
    confidence_score: float
    success: bool
    timestamp: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

@dataclass
class OAuthToken:
    """OAuth token data structure"""
    user_email: str
    access_token: str
    refresh_token: str
    expires_at: datetime
    scope: str
    created_at: datetime

class StorageManager:
    """
    Dual-layer storage system with Redis caching and PostgreSQL persistence
    
    Features:
    - Redis Cluster for high-speed caching (1-hour TTL)
    - PostgreSQL fallback for reliability (+150ms latency)
    - Automatic failover and recovery
    - Connection pooling for performance
    """
    
    def __init__(self):
        self.redis_pool = None
        self.postgres_pool = None
        self.redis_available = True
        
        # Configuration from environment
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.postgres_url = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/payshield")
        
        # Cache TTL settings
        self.oauth_ttl = 3600  # 1 hour
        self.voiceprint_ttl = 3600  # 1 hour (then fallback to PostgreSQL)
        self.verification_ttl = 86400  # 24 hours for audit trail

    async def initialize(self):
        """Initialize Redis and PostgreSQL connections"""
        try:
            await self._init_redis()
            await self._init_postgres()
            logger.info("✅ Storage Manager initialized successfully")
        except Exception as e:
            logger.error(f"❌ Storage initialization failed: {e}")
            raise

    async def _init_redis(self):
        """Initialize Redis connection pool"""
        try:
            self.redis_pool = redis.ConnectionPool.from_url(
                self.redis_url,
                max_connections=20,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test connection
            async with redis.Redis(connection_pool=self.redis_pool) as r:
                await r.ping()
                logger.info("✅ Redis connection established")
                self.redis_available = True
                
        except Exception as e:
            logger.warning(f"⚠️ Redis unavailable, using PostgreSQL only: {e}")
            self.redis_available = False

    async def _init_postgres(self):
        """Initialize PostgreSQL connection pool"""
        try:
            self.postgres_pool = await asyncpg.create_pool(
                self.postgres_url,
                min_size=5,
                max_size=20,
                command_timeout=60
            )
            
            # Create tables if they don't exist
            await self._create_tables()
            logger.info("✅ PostgreSQL connection established")
            
        except Exception as e:
            logger.error(f"❌ PostgreSQL connection failed: {e}")
            raise

    async def _create_tables(self):
        """Create PostgreSQL tables for persistence"""
        async with self.postgres_pool.acquire() as conn:
            # Vendor profiles table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS vendor_profiles (
                    email VARCHAR(255) PRIMARY KEY,
                    company_name VARCHAR(255) NOT NULL,
                    contact_name VARCHAR(255) NOT NULL,
                    voiceprint_hash VARCHAR(255) NOT NULL,
                    enrollment_date TIMESTAMP WITH TIME ZONE NOT NULL,
                    last_verification TIMESTAMP WITH TIME ZONE,
                    verification_count INTEGER DEFAULT 0,
                    confidence_threshold FLOAT DEFAULT 92.0,
                    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """)

            # Verification attempts table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS verification_attempts (
                    id VARCHAR(255) PRIMARY KEY,
                    vendor_email VARCHAR(255) NOT NULL,
                    thread_id VARCHAR(255) NOT NULL,
                    challenge_words TEXT NOT NULL,
                    confidence_score FLOAT NOT NULL,
                    success BOOLEAN NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
                    ip_address INET,
                    user_agent TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """)

            # OAuth tokens table (backup only, primary in Redis)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS oauth_tokens (
                    user_email VARCHAR(255) PRIMARY KEY,
                    access_token TEXT NOT NULL,
                    refresh_token TEXT,
                    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    scope VARCHAR(255),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """)

            # Create indexes for performance
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_verification_attempts_vendor 
                ON verification_attempts(vendor_email, timestamp DESC)
            """)
            
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_verification_attempts_thread 
                ON verification_attempts(thread_id)
            """)

    @asynccontextmanager
    async def get_redis(self):
        """Get Redis connection with automatic fallback handling"""
        if not self.redis_available or not self.redis_pool:
            yield None
            return
            
        try:
            async with redis.Redis(connection_pool=self.redis_pool) as r:
                yield r
        except Exception as e:
            logger.warning(f"Redis error, falling back to PostgreSQL: {e}")
            self.redis_available = False
            yield None

    # OAuth Token Management
    async def store_oauth_token(self, token: OAuthToken) -> bool:
        """Store OAuth token with 1-hour TTL in Redis + PostgreSQL backup"""
        try:
            token_data = asdict(token)
            token_data['expires_at'] = token.expires_at.isoformat()
            token_data['created_at'] = token.created_at.isoformat()
            
            # Primary: Redis with TTL
            async with self.get_redis() as r:
                if r:
                    await r.setex(
                        f"oauth:{token.user_email}",
                        self.oauth_ttl,
                        json.dumps(token_data)
                    )
            
            # Backup: PostgreSQL
            async with self.postgres_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO oauth_tokens 
                    (user_email, access_token, refresh_token, expires_at, scope, updated_at)
                    VALUES ($1, $2, $3, $4, $5, NOW())
                    ON CONFLICT (user_email) DO UPDATE SET
                        access_token = EXCLUDED.access_token,
                        refresh_token = EXCLUDED.refresh_token,
                        expires_at = EXCLUDED.expires_at,
                        scope = EXCLUDED.scope,
                        updated_at = NOW()
                """, token.user_email, token.access_token, token.refresh_token,
                    token.expires_at, token.scope)
            
            logger.info(f"✅ OAuth token stored for {token.user_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to store OAuth token: {e}")
            return False

    async def get_oauth_token(self, user_email: str) -> Optional[OAuthToken]:
        """Retrieve OAuth token with Redis-first, PostgreSQL fallback"""
        try:
            # Try Redis first (fast path)
            async with self.get_redis() as r:
                if r:
                    token_data = await r.get(f"oauth:{user_email}")
                    if token_data:
                        data = json.loads(token_data)
                        return OAuthToken(
                            user_email=data['user_email'],
                            access_token=data['access_token'],
                            refresh_token=data['refresh_token'],
                            expires_at=datetime.fromisoformat(data['expires_at']),
                            scope=data['scope'],
                            created_at=datetime.fromisoformat(data['created_at'])
                        )
            
            # Fallback to PostgreSQL (+150ms latency)
            async with self.postgres_pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT * FROM oauth_tokens 
                    WHERE user_email = $1 AND expires_at > NOW()
                """, user_email)
                
                if row:
                    token = OAuthToken(
                        user_email=row['user_email'],
                        access_token=row['access_token'],
                        refresh_token=row['refresh_token'],
                        expires_at=row['expires_at'],
                        scope=row['scope'],
                        created_at=row['created_at']
                    )
                    
                    # Refresh Redis cache
                    await self.store_oauth_token(token)
                    return token
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to get OAuth token: {e}")
            return None

    # Vendor Profile Management
    async def store_vendor_profile(self, profile: VendorProfile) -> bool:
        """Store vendor voiceprint profile"""
        try:
            # Hash the voiceprint for security if it's not already hashed
            if not self._is_hashed(profile.voiceprint_hash):
                profile.voiceprint_hash = self._hash_voiceprint(profile.voiceprint_hash)
            
            # Store in PostgreSQL (persistent)
            async with self.postgres_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO vendor_profiles 
                    (email, company_name, contact_name, voiceprint_hash, 
                     enrollment_date, verification_count, confidence_threshold, expires_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW())
                    ON CONFLICT (email) DO UPDATE SET
                        company_name = EXCLUDED.company_name,
                        contact_name = EXCLUDED.contact_name,
                        voiceprint_hash = EXCLUDED.voiceprint_hash,
                        enrollment_date = EXCLUDED.enrollment_date,
                        verification_count = EXCLUDED.verification_count,
                        confidence_threshold = EXCLUDED.confidence_threshold,
                        expires_at = EXCLUDED.expires_at,
                        updated_at = NOW()
                """, profile.email, profile.company_name, profile.contact_name,
                    profile.voiceprint_hash, profile.enrollment_date,
                    profile.verification_count, profile.confidence_threshold, profile.expires_at)
            
            # Cache in Redis for fast access
            profile_data = asdict(profile)
            profile_data['enrollment_date'] = profile.enrollment_date.isoformat()
            profile_data['expires_at'] = profile.expires_at.isoformat()
            if profile.last_verification:
                profile_data['last_verification'] = profile.last_verification.isoformat()
            else:
                profile_data['last_verification'] = None
            
            async with self.get_redis() as r:
                if r:
                    await r.setex(
                        f"vendor:{profile.email}",
                        self.voiceprint_ttl,
                        json.dumps(profile_data)
                    )
            
            logger.info(f"✅ Vendor profile stored for {profile.email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to store vendor profile: {e}")
            return False

    async def get_vendor_profile(self, email: str) -> Optional[VendorProfile]:
        """Get vendor profile with Redis-first, PostgreSQL fallback"""
        try:
            # Try Redis first
            async with self.get_redis() as r:
                if r:
                    profile_data = await r.get(f"vendor:{email}")
                    if profile_data:
                        data = json.loads(profile_data)
                        return VendorProfile(
                            email=data['email'],
                            company_name=data['company_name'],
                            contact_name=data['contact_name'],
                            voiceprint_hash=data['voiceprint_hash'],
                            enrollment_date=datetime.fromisoformat(data['enrollment_date']),
                            last_verification=datetime.fromisoformat(data['last_verification']) if data.get('last_verification') else None,
                            verification_count=data['verification_count'],
                            confidence_threshold=data['confidence_threshold'],
                            expires_at=datetime.fromisoformat(data['expires_at'])
                        )
            
            # Fallback to PostgreSQL
            async with self.postgres_pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT * FROM vendor_profiles 
                    WHERE email = $1 AND expires_at > NOW()
                """, email)
                
                if row:
                    profile = VendorProfile(
                        email=row['email'],
                        company_name=row['company_name'],
                        contact_name=row['contact_name'],
                        voiceprint_hash=row['voiceprint_hash'],
                        enrollment_date=row['enrollment_date'],
                        last_verification=row['last_verification'],
                        verification_count=row['verification_count'],
                        confidence_threshold=row['confidence_threshold'],
                        expires_at=row['expires_at']
                    )
                    
                    # Refresh Redis cache
                    await self.store_vendor_profile(profile)
                    return profile
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to get vendor profile: {e}")
            return None

    # Verification Attempts Logging
    async def log_verification_attempt(self, attempt: VerificationAttempt) -> bool:
        """Log verification attempt for audit trail"""
        try:
            # Store in PostgreSQL for permanent audit trail
            async with self.postgres_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO verification_attempts 
                    (id, vendor_email, thread_id, challenge_words, confidence_score,
                     success, timestamp, ip_address, user_agent)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                """, attempt.id, attempt.vendor_email, attempt.thread_id,
                    attempt.challenge_words, attempt.confidence_score,
                    attempt.success, attempt.timestamp, attempt.ip_address,
                    attempt.user_agent)
            
            # Cache recent attempts in Redis
            attempt_data = asdict(attempt)
            attempt_data['timestamp'] = attempt.timestamp.isoformat()
            
            async with self.get_redis() as r:
                if r:
                    await r.setex(
                        f"verification:{attempt.id}",
                        self.verification_ttl,
                        json.dumps(attempt_data)
                    )
            
            # Update vendor verification count
            if attempt.success:
                await self._increment_verification_count(attempt.vendor_email)
            
            logger.info(f"✅ Verification attempt logged: {attempt.id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to log verification attempt: {e}")
            return False

    async def get_verification_history(self, vendor_email: str, limit: int = 50) -> List[VerificationAttempt]:
        """Get verification history for a vendor"""
        try:
            async with self.postgres_pool.acquire() as conn:
                rows = await conn.fetch("""
                    SELECT * FROM verification_attempts 
                    WHERE vendor_email = $1 
                    ORDER BY timestamp DESC 
                    LIMIT $2
                """, vendor_email, limit)
                
                attempts = []
                for row in rows:
                    attempts.append(VerificationAttempt(
                        id=row['id'],
                        vendor_email=row['vendor_email'],
                        thread_id=row['thread_id'],
                        challenge_words=row['challenge_words'],
                        confidence_score=row['confidence_score'],
                        success=row['success'],
                        timestamp=row['timestamp'],
                        ip_address=str(row['ip_address']) if row['ip_address'] else None,
                        user_agent=row['user_agent']
                    ))
                
                return attempts
                
        except Exception as e:
            logger.error(f"❌ Failed to get verification history: {e}")
            return []

    # Utility Methods
    async def _increment_verification_count(self, vendor_email: str):
        """Increment verification count for vendor"""
        async with self.postgres_pool.acquire() as conn:
            await conn.execute("""
                UPDATE vendor_profiles 
                SET verification_count = verification_count + 1,
                    last_verification = NOW(),
                    updated_at = NOW()
                WHERE email = $1
            """, vendor_email)

    def _hash_voiceprint(self, voiceprint_data: str) -> str:
        """Hash voiceprint data for security"""
        return hashlib.sha256(voiceprint_data.encode()).hexdigest()
    
    def _is_hashed(self, data: str) -> bool:
        """Check if data is already hashed (SHA256 hex format)"""
        return len(data) == 64 and all(c in '0123456789abcdef' for c in data.lower())

    async def cleanup_expired_tokens(self):
        """Cleanup expired OAuth tokens (background task)"""
        try:
            async with self.postgres_pool.acquire() as conn:
                deleted = await conn.execute("""
                    DELETE FROM oauth_tokens WHERE expires_at < NOW()
                """)
                logger.info(f"🧹 Cleaned up {deleted} expired OAuth tokens")
        except Exception as e:
            logger.error(f"❌ Token cleanup failed: {e}")

    async def health_check(self) -> Dict[str, Any]:
        """System health check"""
        health = {
            "redis": False,
            "postgres": False,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        try:
            # Check Redis
            async with self.get_redis() as r:
                if r:
                    await r.ping()
                    health["redis"] = True
        except:
            pass
        
        try:
            # Check PostgreSQL
            async with self.postgres_pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
                health["postgres"] = True
        except:
            pass
        
        return health

    async def close(self):
        """Close all connections"""
        try:
            if self.redis_pool:
                await self.redis_pool.disconnect()
            if self.postgres_pool:
                await self.postgres_pool.close()
            logger.info("✅ Storage connections closed")
        except Exception as e:
            logger.error(f"❌ Error closing connections: {e}")

# Singleton instance
storage_manager = StorageManager()

# Convenience functions for main.py
async def init_storage():
    """Initialize storage manager"""
    await storage_manager.initialize()

async def store_oauth_token(token: OAuthToken) -> bool:
    """Store OAuth token"""
    return await storage_manager.store_oauth_token(token)

async def get_oauth_token(user_email: str) -> Optional[OAuthToken]:
    """Get OAuth token"""
    return await storage_manager.get_oauth_token(user_email)

async def store_vendor_profile(profile: VendorProfile) -> bool:
    """Store vendor profile"""
    return await storage_manager.store_vendor_profile(profile)

async def get_vendor_profile(email: str) -> Optional[VendorProfile]:
    """Get vendor profile"""
    return await storage_manager.get_vendor_profile(email)

async def log_verification_attempt(attempt: VerificationAttempt) -> bool:
    """Log verification attempt"""
    return await storage_manager.log_verification_attempt(attempt)

async def get_verification_history(vendor_email: str, limit: int = 50) -> List[VerificationAttempt]:
    """Get verification history"""
    return await storage_manager.get_verification_history(vendor_email, limit)

async def storage_health_check() -> Dict[str, Any]:
    """Get storage health status"""
    return await storage_manager.health_check()

# Background task for cleanup
async def cleanup_task():
    """Background cleanup task"""
    while True:
        try:
            await storage_manager.cleanup_expired_tokens()
            await asyncio.sleep(3600)  # Run every hour
        except Exception as e:
            logger.error(f"❌ Cleanup task error: {e}")
            await asyncio.sleep(3600)

if __name__ == "__main__":
    # Test the storage manager
    async def test_storage():
        await init_storage()
        
        # Test OAuth token
        token = OAuthToken(
            user_email="test@example.com",
            access_token="test_token_123",
            refresh_token="refresh_123",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            scope="read write",
            created_at=datetime.now(timezone.utc)
        )
        
        success = await store_oauth_token(token)
        print(f"Token stored: {success}")
        
        retrieved = await get_oauth_token("test@example.com")
        print(f"Token retrieved: {retrieved is not None}")
        
        # Test vendor profile
        profile = VendorProfile(
            email="vendor@example.com",
            company_name="Test Company",
            contact_name="John Doe",
            voiceprint_hash="test_voiceprint_data",
            enrollment_date=datetime.now(timezone.utc)
        )
        
        profile_success = await store_vendor_profile(profile)
        print(f"Profile stored: {profile_success}")
        
        retrieved_profile = await get_vendor_profile("vendor@example.com")
        print(f"Profile retrieved: {retrieved_profile is not None}")
        
        # Health check
        health = await storage_health_check()
        print(f"Health check: {health}")
        
        await storage_manager.close()
    
    asyncio.run(test_storage())
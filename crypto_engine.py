"""
Cryptographic vault for voice verification badges.

This module handles JWT creation and verification for voice authentication badges.
Only main.py and gmail_handler.py should import from this module.

Key responsibilities:
- Sign JWTs with RSA private key after voice verification
- Verify JWTs with RSA public key for badge validation
- Maintain cryptographic isolation from rest of application
"""

import jwt
import time
from pathlib import Path
from typing import Dict, Any
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import logging

logger = logging.getLogger(__name__)

# Key file paths
PRIVATE_KEY_PATH = Path("keys/private.pem")
PUBLIC_KEY_PATH = Path("keys/public.pem")

# JWT configuration
JWT_ALGORITHM = "RS256"
JWT_ISSUER = "voice-verification-system"


class CryptoEngineError(Exception):
    """Base exception for crypto engine operations."""
    pass


class KeyNotFoundError(CryptoEngineError):
    """Raised when required cryptographic keys are not found."""
    pass


class BadgeVerificationError(CryptoEngineError):
    """Raised when badge verification fails."""
    pass


def _load_private_key() -> bytes:
    """Load RSA private key from disk."""
    try:
        if not PRIVATE_KEY_PATH.exists():
            raise KeyNotFoundError(f"Private key not found at {PRIVATE_KEY_PATH}")
        
        with open(PRIVATE_KEY_PATH, 'rb') as key_file:
            return key_file.read()
    except Exception as e:
        logger.error(f"Failed to load private key: {e}")
        raise KeyNotFoundError(f"Could not load private key: {e}")


def _load_public_key() -> bytes:
    """Load RSA public key from disk."""
    try:
        if not PUBLIC_KEY_PATH.exists():
            raise KeyNotFoundError(f"Public key not found at {PUBLIC_KEY_PATH}")
        
        with open(PUBLIC_KEY_PATH, 'rb') as key_file:
            return key_file.read()
    except Exception as e:
        logger.error(f"Failed to load public key: {e}")
        raise KeyNotFoundError(f"Could not load public key: {e}")


def _generate_key_pair() -> None:
    """Generate RSA key pair if keys don't exist."""
    if PRIVATE_KEY_PATH.exists() and PUBLIC_KEY_PATH.exists():
        return
    
    logger.info("Generating new RSA key pair...")
    
    # Create keys directory if it doesn't exist
    PRIVATE_KEY_PATH.parent.mkdir(exist_ok=True)
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Get public key
    public_key = private_key.public_key()
    
    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serialize public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Write keys to disk
    with open(PRIVATE_KEY_PATH, 'wb') as f:
        f.write(private_pem)
    
    with open(PUBLIC_KEY_PATH, 'wb') as f:
        f.write(public_pem)
    
    # Set restrictive permissions on private key
    PRIVATE_KEY_PATH.chmod(0o600)
    
    logger.info("RSA key pair generated successfully")


def create_badge(email: str, voice_hash: str) -> str:
    """
    Create a signed JWT badge for verified voice authentication.
    
    Called by main.py immediately after AssemblyAI confirms voiceprint.
    
    Args:
        email: The verified email address
        voice_hash: Hash of the voice authentication data
        
    Returns:
        Signed JWT string that can be attached to emails or verified later
        
    Raises:
        CryptoEngineError: If badge creation fails
    """
    try:
        # Ensure keys exist
        _generate_key_pair()
        
        # Load private key
        private_key_pem = _load_private_key()
        
        # Create JWT payload
        current_time = int(time.time())
        payload = {
            "email": email,
            "verified_at": current_time,
            "voice_hash": voice_hash,
            "iss": JWT_ISSUER,
            "iat": current_time,
            "exp": current_time + (365 * 24 * 60 * 60)  # 1 year expiration
        }
        
        # Sign JWT
        jwt_token = jwt.encode(
            payload=payload,
            key=private_key_pem,
            algorithm=JWT_ALGORITHM
        )
        
        logger.info(f"Created verification badge for {email}")
        return jwt_token
        
    except Exception as e:
        logger.error(f"Failed to create badge for {email}: {e}")
        raise CryptoEngineError(f"Badge creation failed: {e}")


def verify_badge(jwt_string: str) -> Dict[str, Any]:
    """
    Verify a JWT badge and return its payload.
    
    Called by gmail_handler.py when buyer hovers badge or /decode endpoint is hit.
    
    Args:
        jwt_string: The JWT token to verify
        
    Returns:
        Dictionary containing the verified payload with keys:
        - email: verified email address
        - verified_at: timestamp of verification
        - voice_hash: hash of voice authentication data
        
    Raises:
        BadgeVerificationError: If verification fails
    """
    try:
        # Load public key
        public_key_pem = _load_public_key()
        
        # Verify and decode JWT
        payload = jwt.decode(
            jwt=jwt_string,
            key=public_key_pem,
            algorithms=[JWT_ALGORITHM],
            issuer=JWT_ISSUER,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iat": True,
                "verify_iss": True
            }
        )
        
        # Validate required fields
        required_fields = ["email", "verified_at", "voice_hash"]
        for field in required_fields:
            if field not in payload:
                raise BadgeVerificationError(f"Missing required field: {field}")
        
        logger.info(f"Successfully verified badge for {payload['email']}")
        return payload
        
    except jwt.ExpiredSignatureError:
        logger.warning("Badge verification failed: token expired")
        raise BadgeVerificationError("Badge has expired")
    
    except jwt.InvalidTokenError as e:
        logger.warning(f"Badge verification failed: invalid token - {e}")
        raise BadgeVerificationError(f"Invalid badge: {e}")
    
    except Exception as e:
        logger.error(f"Badge verification failed: {e}")
        raise BadgeVerificationError(f"Verification failed: {e}")


def get_public_key_pem() -> str:
    """
    Get the public key in PEM format for external verification.
    
    This can be called by an endpoint like /public-key to allow
    external auditors to verify badges offline.
    
    Returns:
        Public key in PEM format as string
    """
    try:
        _generate_key_pair()  # Ensure keys exist
        public_key_bytes = _load_public_key()
        return public_key_bytes.decode('utf-8')
    except Exception as e:
        logger.error(f"Failed to get public key: {e}")
        raise CryptoEngineError(f"Could not retrieve public key: {e}")


# Initialize keys on module import
try:
    _generate_key_pair()
    logger.info("Crypto engine initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize crypto engine: {e}")

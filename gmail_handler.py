"""
PayShield Gmail Handler - File 3
Simple Gmail API key integration (no OAuth complexity)
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import requests
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GmailHandler:
    """Simple Gmail API with just an API key"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gmail handler
        
        Args:
            api_key: Gmail API key. If None, will try to get from environment
        """
        self.api_key = api_key or "o"
        self.base_url = "https://gmail.googleapis.com/gmail/v1"
        self._initialized = False
    
    def _ensure_initialized(self):
        """Ensure the handler is properly initialized with API key"""
        if not self.api_key:
            raise ValueError(
                "Gmail API key required. Set GMAIL_API_KEY environment variable "
                "or pass api_key parameter to GmailHandler constructor"
            )
        self._initialized = True
    
    async def get_thread_data(self, thread_id: str, access_token: str) -> Dict[str, Any]:
        """Extract sender email + subject from thread (privacy-safe)"""
        self._ensure_initialized()
        
        try:
            # Build request URL
            url = f"{self.base_url}/users/me/threads/{thread_id}"
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            params = {
                "format": "metadata",
                "key": self.api_key
            }
            
            # Make API request
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            thread = response.json()
            
            if not thread.get('messages'):
                raise ValueError("Thread contains no messages")
            
            # Get first message (thread starter)
            first_message = thread['messages'][0]
            headers_list = first_message['payload']['headers']
            
            # Extract sender and subject
            sender_email = None
            subject = None
            
            for header in headers_list:
                if header['name'].lower() == 'from':
                    # Extract email from "Name <email@domain.com>" format
                    from_field = header['value']
                    if '<' in from_field and '>' in from_field:
                        sender_email = from_field.split('<')[1].split('>')[0].strip()
                    else:
                        sender_email = from_field.strip()
                
                elif header['name'].lower() == 'subject':
                    subject = header['value']
            
            if not sender_email:
                raise ValueError("Could not extract sender email from thread")
            
            thread_data = {
                'thread_id': thread_id,
                'sender_email': sender_email,
                'subject': subject or "No Subject",
                'message_count': len(thread['messages']),
                'extracted_at': datetime.utcnow().isoformat()
            }
            
            logger.info(f"✅ Thread data extracted: {sender_email} - {subject}")
            return thread_data
            
        except requests.RequestException as e:
            logger.error(f"❌ Gmail API request error: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Failed to extract thread data: {e}")
            raise
    
    def _create_verification_badge_html(self, jwt_badge: str, sender_email: str) -> str:
        """Create the HTML for the verification badge"""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        return f"""
        <div style="background: linear-gradient(135deg, #38a169 0%, #2d7d32 100%); 
                    color: white; 
                    padding: 20px; 
                    border-radius: 12px; 
                    margin: 15px 0; 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    border-left: 5px solid #00d4aa;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;">
                <span style="font-size: 24px;">🛡️</span>
                <div>
                    <div style="font-weight: 600; font-size: 18px; margin-bottom: 4px;">
                        PayShield Voice Verification
                    </div>
                    <div style="opacity: 0.9; font-size: 14px;">
                        ✅ Voice-verified by <strong>{sender_email}</strong>
                    </div>
                    <div style="opacity: 0.8; font-size: 12px; margin-top: 2px;">
                        Verified on {timestamp} UTC
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 15px; padding: 12px; 
                       background: rgba(255,255,255,0.1); 
                       border-radius: 8px;
                       font-size: 11px; 
                       font-family: 'Monaco', 'Menlo', monospace;
                       word-break: break-all;
                       line-height: 1.4;">
                <strong>JWT Verification Badge:</strong><br>
                <span style="opacity: 0.9;">{jwt_badge}</span>
            </div>
            
            <div style="margin-top: 15px; font-size: 12px; opacity: 0.9; 
                       padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.2);">
                🔍 Verify this badge at: 
                <a href="https://payshield.live/decode" 
                   style="color: #00d4aa; text-decoration: none; font-weight: 500;">
                    payshield.live/decode
                </a>
            </div>
            
            <div style="margin-top: 8px; font-size: 10px; opacity: 0.7;">
                This message was automatically generated by PayShield Voice Verification System
            </div>
        </div>
        """
    
    async def inject_verification_badge(self, thread_id: str, jwt_badge: str, sender_email: str, access_token: str) -> bool:
        """Create draft reply with JWT verification badge"""
        self._ensure_initialized()
        
        try:
            # Create badge message content
            badge_html = self._create_verification_badge_html(jwt_badge, sender_email)
            
            # Create message
            message = MIMEText(badge_html, 'html')
            message['Subject'] = "PayShield Voice Verification Badge"
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Create draft payload
            draft_data = {
                'message': {
                    'raw': raw_message,
                    'threadId': thread_id
                }
            }
            
            # Build request
            url = f"{self.base_url}/users/me/drafts"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            params = {"key": self.api_key}
            
            # Send request
            response = requests.post(url, headers=headers, params=params, json=draft_data, timeout=30)
            response.raise_for_status()
            
            draft = response.json()
            draft_id = draft['id']
            
            logger.info(f"✅ Verification badge injected as draft {draft_id} in thread {thread_id}")
            return True
            
        except requests.RequestException as e:
            logger.error(f"❌ Gmail API request error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to inject verification badge: {e}")
            return False
    
    async def health_check(self, access_token: str) -> Dict[str, Any]:
        """Gmail API health check"""
        self._ensure_initialized()
        
        try:
            url = f"{self.base_url}/users/me/profile"
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {"key": self.api_key}
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            profile = response.json()
            
            return {
                "status": "healthy",
                "authenticated": True,
                "email": profile.get('emailAddress'),
                "messages_total": profile.get('messagesTotal', 0),
                "threads_total": profile.get('threadsTotal', 0)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "authenticated": False,
                "error": str(e)
            }

# Lazy initialization - only create instance when needed
_gmail_handler_instance = None

def get_gmail_handler(api_key: Optional[str] = None) -> GmailHandler:
    """Get Gmail handler instance (lazy initialization)"""
    global _gmail_handler_instance
    if _gmail_handler_instance is None:
        _gmail_handler_instance = GmailHandler(api_key)
    return _gmail_handler_instance

# Convenience functions for main.py
async def get_thread_data(thread_id: str, access_token: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Get thread metadata"""
    handler = get_gmail_handler(api_key)
    return await handler.get_thread_data(thread_id, access_token)

async def inject_verification_badge(thread_id: str, jwt_badge: str, sender_email: str, access_token: str, api_key: Optional[str] = None) -> bool:
    """Inject verification badge as draft"""
    handler = get_gmail_handler(api_key)
    return await handler.inject_verification_badge(thread_id, jwt_badge, sender_email, access_token)

async def gmail_health_check(access_token: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Gmail health check"""
    handler = get_gmail_handler(api_key)
    return await handler.health_check(access_token)

if __name__ == "__main__":
    # Test Gmail handler initialization
    import asyncio
    
    async def test_gmail():
        print("🧪 Testing Gmail Handler initialization...")
        
        try:
            # Test handler creation
            handler = GmailHandler()
            print(f"✅ Gmail handler created successfully")
            print(f"✅ API key loaded: {handler.api_key[:20]}...")
            print(f"✅ Base URL: {handler.base_url}")
            
            # Test initialization check
            handler._ensure_initialized()
            print("✅ Handler initialization check passed")
            
            print("\n📝 To test actual Gmail API calls, you need:")
            print("   1. A valid Gmail access token")
            print("   2. A real Gmail thread ID")
            print("   3. Set these as environment variables:")
            print("      - GMAIL_ACCESS_TOKEN=your_token_here")
            print("      - TEST_THREAD_ID=your_thread_id_here")
            
            # If you have access token, uncomment these lines:
            # access_token = os.getenv("GMAIL_ACCESS_TOKEN")
            # if access_token:
            #     health = await handler.health_check(access_token)
            #     print(f"Gmail health: {health}")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    asyncio.run(test_gmail())

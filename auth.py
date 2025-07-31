# auth.py
import os, json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

CREDS_FILE = "credentials.json"   # OAuth client ID JSON from console.cloud.google
TOKEN_FILE = "token.json"         # created after first login
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", 
          "https://www.googleapis.com/auth/gmail.compose"]

def authenticate():
    """Run OAuth flow to get user authentication"""
    creds = None
    
    # Load existing token if available
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDS_FILE):
                raise RuntimeError(f"{CREDS_FILE} missing—download from Google Cloud Console")
            
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def get_service():
    """Get authenticated Gmail service"""
    if not os.path.exists(TOKEN_FILE):
        print("🔐 No token found. Starting authentication...")
        authenticate()
    
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # Check if credentials are still valid
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Save refreshed credentials
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        else:
            print("🔐 Token expired. Re-authenticating...")
            authenticate()
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    return build("gmail", "v1", credentials=creds)

def get_access_token():
    """Get current access token for API calls"""
    if not os.path.exists(TOKEN_FILE):
        authenticate()
    
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            authenticate()
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    return creds.token

if __name__ == "__main__":
    # Test authentication
    print("🧪 Testing authentication...")
    try:
        service = get_service()
        profile = service.users().getProfile(userId='me').execute()
        print(f"✅ Authenticated as: {profile.get('emailAddress')}")
        print(f"✅ Access token: {get_access_token()[:20]}...")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
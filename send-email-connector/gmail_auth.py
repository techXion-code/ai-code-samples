import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def get_gmail_service():
    """Return an authenticated Gmail API service."""
    creds = get_credentials()
    return build("gmail", "v1", credentials=creds)

# Define scopes here so they are centralized
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_credentials():
    """Load, refresh, or create Google API credentials."""
    creds = None
    token_path = "token.json"
    creds_path = "credentials.json"

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES
            ).run_local_server(port=0)

        with open(token_path, "w") as f:
            f.write(creds.to_json())

    return creds

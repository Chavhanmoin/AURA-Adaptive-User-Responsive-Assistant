import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes needed for Gmail DRAFT and Calendar access
SCOPES = [
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/calendar.events'
]

def get_gmail_service():
    """Authenticate and return the Gmail API service"""
    creds = None
    token_path = 'token.json'
    creds_path = 'credentials.json'

    # Load credentials from existing token.json
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        # Force re-auth if scopes have changed
        if set(creds.scopes or []) != set(SCOPES):
            print("[INFO] Scopes have changed. Re-authenticating...")
            creds = None

    # If credentials are not valid or missing, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError("credentials.json not found")
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save new token for future use
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def send_gmail_api(to_email, subject, body):
    """Create a Gmail draft or send email via Gmail API"""
    try:
        service = get_gmail_service()

        # Compose MIME message
        message = MIMEText(body)
        message['subject'] = subject
        if to_email:
            message['to'] = to_email

        # Encode message
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        if not to_email:
            # Create draft (for manual recipient)
            draft = service.users().drafts().create(
                userId="me",
                body={'message': {'raw': raw}}
            ).execute()
            return f"[✓] Draft created with subject: '{subject}'. You can add the recipient manually in Gmail."
        else:
            # Send directly
            sent = service.users().messages().send(
                userId="me",
                body={'raw': raw}
            ).execute()
            return f"[✓] Email sent to {to_email} with subject: '{subject}'"

    except Exception as e:
        return f"[✗] Gmail API failed: {e}"

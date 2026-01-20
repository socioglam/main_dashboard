from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

# --- CONFIGURATION ---
CREDENTIALS_FILE = "oauth_credentials.json"
TOKEN_FILE = "token.json"
SCOPES = ["https://www.googleapis.com/auth/blogger"]


def authenticate_blogger():
    creds = None
    # 1. Check if token.json exists
    if os.path.exists(TOKEN_FILE):
        print(f"✅ Found existing {TOKEN_FILE}, checking validity...")
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            print(f"⚠️ Error reading {TOKEN_FILE}: {e}")

    # 2. If no valid creds, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"⚠️ Refresh failed: {e}. Starting fresh login.")
                creds = None

        if not creds:
            print("🚀 Starting new login flow...")
            if not os.path.exists(CREDENTIALS_FILE):
                print(
                    f"❌ Error: '{CREDENTIALS_FILE}' not found! Please check the file name."
                )
                return

            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # 3. Save the credentials for the next run
        print(f"💾 Saving new token to {TOKEN_FILE}...")
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    print("\n🎉 Authentication Successful!")
    print(f"Token saved to: {os.path.abspath(TOKEN_FILE)}")
    print("You can now run app.py")


if __name__ == "__main__":
    authenticate_blogger()

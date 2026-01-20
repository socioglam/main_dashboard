from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

# From app.py
BLOGGER_ID = "3060640816717102767"
BLOGGER_SCOPES = ["https://www.googleapis.com/auth/blogger"]
TOKEN_FILE = "token.json"


def verify_access():
    if not os.path.exists(TOKEN_FILE):
        print("❌ No token.json found.")
        return

    try:
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, BLOGGER_SCOPES)
        service = build("blogger", "v3", credentials=creds)

        print("🔍 Listing all blogs for this user...")
        user_blogs = service.blogs().listByUser(userId="self").execute()

        if "items" in user_blogs:
            for blog in user_blogs["items"]:
                print(f"✅ Found Blog:")
                print(f"   Name: {blog['name']}")
                print(f"   ID: {blog['id']}")
                print(f"   URL: {blog['url']}")
                print("-" * 20)

                if blog["id"] == BLOGGER_ID:
                    print(f"   >>> MATCHES CONFIGURED ID ({BLOGGER_ID}) <<<")
        else:
            print("❌ No blogs found for this user.")

    except Exception as e:
        print(f"❌ Verification Failed: {e}")


if __name__ == "__main__":
    verify_access()

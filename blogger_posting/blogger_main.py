import requests
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ================= 1. CONFIGURATION (SETTINGS) =================

# --- CONTENT SOURCE ---
SOURCE_API_URL = "https://www.livyalife.com/api/all-links-data"
FIXED_LINK = "https://www.livyalife.com/daily-feed"
TODAY_DATE = datetime.date.today().strftime("%Y-%m-%d")
POST_TITLE = f"🔥 Trending Now: Today's Top Updates & Viral Links - {TODAY_DATE}"

# --- BLOGGER SETTINGS ---
BLOGGER_ID = "3060640816717102767"
BLOGGER_SCOPES = ["https://www.googleapis.com/auth/blogger"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "oauth_credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")

# ================= 2. CONTENT GENERATOR =================


def fetch_data_and_generate_html():
    print("\n⏳ [Step 1] Fetching data from API...")
    try:
        response = requests.get(SOURCE_API_URL)
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"❌ API Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

    if not data:
        print("❌ No data received from API.")
        return None

    print(f"✅ Found {len(data)} items. Preparing content...")

    # Intro Paragraph
    full_html = f"<p>Here is the list of latest updates fetched on {TODAY_DATE}. Check them out below:</p><hr>"

    for item in data:
        api_title = item.get("title", "Unknown Title")
        target_url = item.get("target_url", "#")
        description = item.get("description", "No description available.")

        item_html = f"""
        <div style="margin-bottom: 30px; padding: 15px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9;">
            <h3 style="margin-top: 0; color: #333;">{api_title}</h3>
            <p style="margin-bottom: 20px;">
                <a href="{target_url}" rel="dofollow" target="_blank" style="background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-right: 10px;">
                    { target_url }
                </a>
                <a href="{FIXED_LINK}" rel="dofollow" target="_blank" style="background-color: #28a745; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                    📅 Daily Feed
                </a>
            </p>
            <p style="margin-top: 15px; color: #555;">
                <strong>Description:</strong><br>
                {description}
            </p>
        </div>
        """
        full_html += item_html

    return full_html


# ================= 3. BLOGGER FUNCTION =================


def post_to_blogger(
    title, content, credentials_file=None, token_file=None, blog_id=None
):
    print("\n🚀 [Step 2] Uploading to Blogger...")
    creds = None

    # Use defaults if not provided
    eff_token_file = token_file or TOKEN_FILE
    eff_credentials_file = credentials_file or CREDENTIALS_FILE
    eff_blog_id = blog_id or BLOGGER_ID

    # Check for existing token
    if os.path.exists(eff_token_file):
        creds = Credentials.from_authorized_user_file(eff_token_file, BLOGGER_SCOPES)

    # Refresh or Login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(eff_credentials_file):
                print(f"❌ Blogger Error: '{eff_credentials_file}' not found.")
                return
            flow = InstalledAppFlow.from_client_secrets_file(
                eff_credentials_file, BLOGGER_SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save new token
        with open(eff_token_file, "w") as token:
            token.write(creds.to_json())

    # Build Service
    try:
        service = build("blogger", "v3", credentials=creds)

        body = {
            "kind": "blogger#post",
            "title": title,
            "content": content,
            "labels": ["Daily Updates", "Cars Collection"],
        }

        posts = service.posts()
        result = posts.insert(blogId=eff_blog_id, body=body).execute()
        print(f"✅ BLOGGER SUCCESS! Link: {result['url']}")
        return result["url"]

    except Exception as e:
        print(f"❌ Blogger Failed: {e}")
        return None


# ================= MAIN EXECUTION =================

if __name__ == "__main__":
    print(f"--- BLOGGER AUTO-POSTER ({TODAY_DATE}) ---")

    # 1. Generate HTML
    final_html = fetch_data_and_generate_html()

    # 2. Post to Blogger
    if final_html:
        post_to_blogger(POST_TITLE, final_html)
    else:
        print("❌ No content generated, skipping posting.")

import requests
import datetime
import json
import os

# ================= 1. CONFIGURATION (SETTINGS) =================

# --- CONTENT SOURCE ---
SOURCE_API_URL = "https://www.livyalife.com/api/all-links-data"
SOURCE_API_URL = "https://www.livyalife.com/daily-feed"
TODAY_DATE = datetime.date.today().strftime("%Y-%m-%d")

# --- LINKEDIN SETTINGS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "linkedin_credentials.json")
LINKEDIN_API_URL = "https://api.linkedin.com/v2/ugcPosts"


# ================= 2. CONTENT GENERATOR =================


def fetch_data():
    print("\n⏳ [Step 1] Fetching data from API...")
    try:
        response = requests.get(SOURCE_API_URL)
        if response.status_code == 200:
            data = response.json()
            if not data:
                print("❌ No data received from API.")
                return None
            print(f"✅ Found {len(data)} items.")
            return data
        else:
            print(f"❌ API Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None


def generate_linkedin_post_text(data):
    # LinkedIn doesn't support HTML. We need plain text / hashtags.
    # Let's start with a generic opener
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    message = f"🔥 Trending Now ({current_time}): Today's Top Updates & Viral Links ({TODAY_DATE}) 🔥\n\n"
    message += "Check out the latest updates below! 👇\n\n"

    # Add top 3 items to avoid making the post too long
    # Or just a general summary if there are many.
    # For now, let's list titles.

    for i, item in enumerate(data[:5]):  # Top 5
        title = item.get("title", "Update")
        target_url = item.get("target_url")
        link = item.get(
            "target_url", SOURCE_API_URL
        )  # Assuming 'target_url' exists as per app.py
        message += f"• {title}\n"

    message += f"\n👉 Full List Here: {target_url}\n"
    message += "\n#Trending #DailyUpdates #Viral #News #Automation"
    return message


# ================= 3. LINKEDIN FUNCTION =================


def post_to_linkedin(message, link_url, link_title, link_desc, credentials=None):
    print("\n🚀 [Step 2] Uploading to LinkedIn...")

    if not credentials:
        if not os.path.exists(CREDENTIALS_FILE):
            print(f"❌ LinkedIn Error: {CREDENTIALS_FILE} not found.")
            return
        with open(CREDENTIALS_FILE, "r") as f:
            credentials = json.load(f)

    access_token = credentials.get("access_token")
    person_urn = credentials.get("person_urn")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    post_data = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": message},
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "description": {"text": link_desc},
                        "originalUrl": link_url,
                        "title": {"text": link_title},
                    }
                ],
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    try:
        response = requests.post(LINKEDIN_API_URL, headers=headers, json=post_data)
        if response.status_code == 201:
            print("✅ LINKEDIN SUCCESS! Post Live.")
            print(f"   Response ID: {response.json().get('id')}")
        else:
            print(f"❌ LinkedIn Failed: {response.status_code} - {response.text}")
            print(
                "\n💡 Tip: Token might be expired. Use 'oauth_linkedIn.py' to generate a new one if needed."
            )

    except Exception as e:
        print(f"❌ Connection Error: {e}")


# ================= MAIN EXECUTION =================

if __name__ == "__main__":
    print(f"--- LINKEDIN AUTO-POSTER ({TODAY_DATE}) ---")

    # 0. Load Credentials
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Error: {CREDENTIALS_FILE} not found.")
        exit(1)

    with open(CREDENTIALS_FILE, "r") as f:
        creds = json.load(f)

    # 1. Fetch Data
    data = fetch_data()

    if data:
        # 2. Prepare Content
        # LinkedIn is stricter than blogs. We typically post a short message + ONE main link/article.
        # Since we have a list of links, we'll promote the "Daily Feed" page as the main article,
        # and list the topics in the text message.

        post_text = generate_linkedin_post_text(data)

        main_link_url = SOURCE_API_URL
        main_link_title = f"Daily Updates - {TODAY_DATE}"
        main_link_desc = (
            "Click to see all the latest trending links and updates for today."
        )

        # 3. Post to LinkedIn
        post_to_linkedin(
            creds, post_text, main_link_url, main_link_title, main_link_desc
        )
    else:
        print("❌ Data nahi mila, isliye posting cancel.")

import requests
import datetime

# ================= 1. CONFIGURATION (SETTINGS) =================

# --- CONTENT SOURCE ---
SOURCE_API_URL = "https://www.livyalife.com/api/all-links-data"
FIXED_LINK = "https://www.livyalife.com/daily-feed"
TODAY_DATE = datetime.date.today().strftime("%Y-%m-%d")
POST_TITLE = f"🔥 Trending Now: Today's Top Updates & Viral Links - {TODAY_DATE}"

# --- WORDPRESS SETTINGS ---
# IMPORTANT: TO POST WITH YOUR ACCOUNT, YOU MUST UPDATE THESE VALUES!
# 1. WP_USERNAME: Your WordPress.com username.
# 2. WP_PASSWORD: Create an 'Application Password' at https://wordpress.com/me/security/two-step
# 3. CLIENT_ID/SECRET: Create an app at https://developer.wordpress.com/apps/

WP_USERNAME = "sales94897d49e6"  # REPLACE THIS
WP_PASSWORD = ""  # REPLACE THIS (Application Password)
WP_CLIENT_ID = ""  # REPLACE THIS
WP_CLIENT_SECRET = ""  # REPLACE THIS
WP_SITE_DOMAIN = "sales94897d49e6-xicot.wordpress.com"  # REPLACE THIS

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
                    { target_url}
                </a><br />
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


# ================= 3. WORDPRESS FUNCTION =================


def post_to_wordpress(
    title,
    content,
    username=None,
    password=None,
    client_id=None,
    client_secret=None,
    site_domain=None,
):
    print("\n🚀 [Step 2] Uploading to WordPress...")

    # Use defaults if not provided
    uname = username or WP_USERNAME
    upass = password or WP_PASSWORD
    uid = client_id or WP_CLIENT_ID
    usec = client_secret or WP_CLIENT_SECRET
    udomain = site_domain or WP_SITE_DOMAIN

    # 1. Get Token
    token_url = "https://public-api.wordpress.com/oauth2/token"
    token_data = {
        "client_id": uid,
        "client_secret": usec,
        "grant_type": "password",
        "username": uname,
        "password": upass,
    }

    access_token = None
    try:
        resp = requests.post(token_url, data=token_data)
        if resp.status_code == 200:
            access_token = resp.json().get("access_token")
        else:
            print(f"❌ WP Token Error: {resp.text}")
            print(
                "💡 Hint: Check your Username, Application Password, Client ID, and Secret."
            )
            return
    except Exception as e:
        print(f"❌ WP Connection Error: {e}")
        return

    # 2. Post Data
    post_url = f"https://public-api.wordpress.com/rest/v1.1/sites/{udomain}/posts/new"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    post_data = {
        "title": title,
        "content": content,
        "status": "publish",
        "categories": ["Daily Updates"],
    }

    try:
        response = requests.post(post_url, headers=headers, json=post_data)
        if response.status_code == 200:
            print(f"✅ WORDPRESS SUCCESS! Link: {response.json()['short_URL']}")
        else:
            print(f"❌ WordPress Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ WordPress Error: {e}")


# ================= MAIN EXECUTION =================

if __name__ == "__main__":
    print(f"--- WORDPRESS AUTO-POSTER ({TODAY_DATE}) ---")

    # 1. HTML Banao
    final_html = fetch_data_and_generate_html()

    if final_html:
        # 2. WordPress par bhejo
        post_to_wordpress(POST_TITLE, final_html)
    else:
        print("❌ Data nahi mila, isliye posting cancel.")

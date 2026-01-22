import requests
import datetime

# ================= 1. CONFIGURATION (SETTINGS) =================

# --- CONTENT SOURCE ---
SOURCE_API_URL = "https://www.livyalife.com/api/all-links-data"
FIXED_LINK = "https://www.livyalife.com/daily-feed"
TODAY_DATE = datetime.date.today().strftime("%Y-%m-%d")
POST_TITLE = f"🔥 Trending Now: Today's Top Updates & Viral Links - {TODAY_DATE}"

# --- DEV.TO SETTINGS ---
# Get your API Key from: https://dev.to/settings/extensions
DEVTO_API_KEY = ""
DEVTO_URL = "https://dev.to/api/articles"

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


# ================= 3. DEV.TO FUNCTION =================


def post_to_devto(title, content_html, api_key=None):
    print("\n🚀 [Step 2] Uploading to Dev.to...")

    key = api_key or DEVTO_API_KEY
    headers = {"api-key": key, "Content-Type": "application/json"}

    payload = {
        "article": {
            "title": title,
            "published": True,
            "description": "Daily automated updates for car links.",
            "tags": ["python", "automation", "cars", "dailyupdates"],
            "body_markdown": content_html,
        }
    }

    try:
        response = requests.post(DEVTO_URL, headers=headers, json=payload)
        if response.status_code == 201:
            return response.json()['url']
        else:
            return f"❌ Dev.to Failed: {response.status_code} - {response.text}"
    except Exception as e:
        print(f"❌ Dev.to Error: {e}")


# ================= MAIN EXECUTION =================

if __name__ == "__main__":
    print(f"--- DEV.TO AUTO-POSTER ({TODAY_DATE}) ---")

    # 1. HTML Banao
    final_html = fetch_data_and_generate_html()

    if final_html:
        # 2. Dev.to par bhejo
        post_to_devto(POST_TITLE, final_html)
    else:
        print("❌ Data nahi mila, isliye posting cancel.")

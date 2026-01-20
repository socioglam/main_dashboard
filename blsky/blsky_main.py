from atproto import Client, models
import requests
import datetime
import datetime as dt

# ================= 1. CONFIGURATION (SETTINGS) =================

# --- CONTENT SOURCE ---
SOURCE_API_URL = "https://www.livyalife.com/api/all-links-data"
FIXED_LINK = "https://www.livyalife.com/daily-feed"
TODAY_DATE = dt.date.today().strftime("%Y-%m-%d")

# --- BLUESKY SETTINGS ---
BSKY_HANDLE = "indexops.bsky.social"
BSKY_PASSWORD = ""

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


def generate_bluesky_post_text(data):
    # Bluesky has a 300 char limit (approx). We need to be concise.
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    message = f"🔥 Trending Updates ({current_time}) 🔥\n"

    # List top 2-3 titles maximum to save space
    for item in data[:3]:
        title = item.get("title", "Update")
        target_url = item.get("target_url", "")
        message += f"• {title}\n"

    message += f"\n🔗 Full List: {target_url}"
    message += "\n#Trending #News"
    return message


# ================= 3. BLUESKY FUNCTION =================


def post_to_bluesky(text, link_url=None, handle=None, password=None):
    print("\n🚀 [Step 2] Uploading to Bluesky...")

    eff_handle = handle or BSKY_HANDLE
    eff_password = password or BSKY_PASSWORD

    try:
        client = Client()
        client.login(eff_handle, eff_password)

        # Simple text post with link appended
        # Note: atproto automatically detects links and creating facets (clickable links)
        # is handled by the library in newer versions, or we can rely on text parsing.
        # For simplicity and reliability based on your request:

        client.send_post(text=text)

        print("✅ BLUESKY SUCCESS! Post sent.")

    except Exception as e:
        print(f"❌ Bluesky Error: {e}")


# ================= MAIN EXECUTION =================

if __name__ == "__main__":
    print(f"--- BLUESKY AUTO-POSTER ({TODAY_DATE}) ---")

    # 1. Fetch Data
    data = fetch_data()

    if data:
        # 2. Prepare Content
        post_text = generate_bluesky_post_text(data)

        # 3. Post to Bluesky
        post_to_bluesky(post_text, FIXED_LINK)
    else:
        print("❌ Data nahi mila, isliye posting cancel.")

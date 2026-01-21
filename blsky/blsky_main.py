from atproto import Client, models, client_utils
import requests
import datetime
import datetime as dt

# ================= 1. CONFIGURATION (SETTINGS) =================

SOURCE_API_URL = "https://www.livyalife.com/api/all-links-data"
FIXED_LINK = "https://www.livyalife.com/daily-feed"
TODAY_DATE = dt.date.today().strftime("%Y-%m-%d")

BSKY_HANDLE = "indexops.bsky.social"
BSKY_PASSWORD = "" # Apna password yahan daalein

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


# 👇 Maine naam wapas 'generate_bluesky_post_text' kar diya taaki server script isse dhund sake
def generate_bluesky_post_text(item):
    """
    Ye function EK item (dictionary) leta hai aur uska post content banata hai.
    NOTE: Ensure karein ki aapka main script isse 'item' pass kar raha hai, puri 'list' nahi.
    """
    
    # Safety check: Agar galti se list aa gayi, toh pehla item le lo
    if isinstance(item, list):
        item = item[0]

    title = item.get("title", "No Title")
    description = item.get("description", "")
    target_url = item.get("target_url", "")

    # --- TextBuilder Start ---
    tb = client_utils.TextBuilder()

    # 1. Title
    tb.text(f"🔥 {title}\n\n")

    # 2. Description
    if description:
        tb.text(f"{description}\n\n")

    # 3. Clickable Link
    if target_url:
        tb.text("🔗 Link: ")
        tb.link("Click Here to Open", target_url)

    tb.text("\n\n#Trending #News")

    return tb


# ================= 3. BLUESKY FUNCTION =================

def post_to_bluesky(text, link_url=None, handle=None, password=None):
    # 'text' argument yahan wo TextBuilder object hai jo upar se aa raha hai
    print("\n🚀 [Step 2] Uploading to Bluesky...")

    eff_handle = handle or BSKY_HANDLE
    eff_password = password or BSKY_PASSWORD

    try:
        client = Client()
        client.login(eff_handle, eff_password)

        # 👇 FIX: Yahan pehle 'text_builder' likha tha jo defined nahi tha. 
        # Isse 'text' kar diya hai jo function argument hai.
        client.send_post(text) 
        
        print(f"✅ Post Sent Successfully!")

    except Exception as e:
        print(f"❌ Error posting to Bluesky: {e}")


# ================= MAIN EXECUTION =================

if __name__ == "__main__":
    print(f"--- BLUESKY AUTO-POSTER ({TODAY_DATE}) ---")

    # 1. Fetch Data
    data = fetch_data()

    if data:
        print(f"🚀 Found {len(data)} items to post.\n")

        # Har item ke liye loop chalayenge
        for item in data:
            # Step A: Content generate karo (Function name ab sahi hai)
            post_content = generate_bluesky_post_text(item)

            # Step B: Post kar do
            print(f"posting: {item.get('title')}")
            post_to_bluesky(post_content)

    else:
        print("❌ Data nahi mila.")
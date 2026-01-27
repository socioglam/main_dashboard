from atproto import Client, models, client_utils
import requests
import datetime
import datetime as dt

# ================= 1. CONFIGURATION (SETTINGS) =================

SOURCE_API_URL = "https://www.livyalife.com/api/all-links-data"
FIXED_LINK = "https://www.livyalife.com/daily-feed"
TODAY_DATE = dt.date.today().strftime("%Y-%m-%d")

BSKY_HANDLE = "indexops.bsky.social"
BSKY_PASSWORD = ""  # Apna password yahan daalein

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

    # Calculate current length of non-description parts
    # Title: 🔥 {title}\n\n
    # Link: 🔗 Link: Click Here to Open ({target_url} is a link facet, doesn't count to text length usually but we should be safe.
    # Actually, Bsky text length counts the visible text "Click Here to Open", not the URL)
    # Footer: \n\n#Trending #News

    title_text = f"🔥 {title}\n\n"
    link_text = "\n🔗 Link: "
    link_anchor = "Click Here to Open"
    footer_text = "\n\n#Trending #News"

    fixed_length = (
        len(title_text) + len(link_text) + len(link_anchor) + len(footer_text)
    )
    remaining_chars = 300 - fixed_length - 5  # Buffer of 5 chars

    # 1. Title
    tb.text(title_text)

    # 2. Description (Truncated)
    if description:
        if len(description) > remaining_chars:
            description = description[:remaining_chars] + "..."
        tb.text(f"{description}")

    # 3. Clickable Link
    if target_url:
        tb.text(link_text)
        tb.link(link_anchor, target_url)

    tb.text(footer_text)

    return tb


# ================= 3. BLUESKY FUNCTION =================


def post_to_bluesky(text, link_url=None, handle=None, password=None):
    # 'text' argument yahan wo TextBuilder object hai jo upar se aa raha hai
    print("\n🚀 [Step 2] Uploading to Bluesky...")

    eff_handle = handle or BSKY_HANDLE
    eff_password = password or BSKY_PASSWORD

    client = Client()
    session = client.login(eff_handle, eff_password)

    # 👇 FIX: Yahan pehle 'text_builder' likha tha jo defined nahi tha.
    # Isse 'text' kar diya hai jo function argument hai.
    post = client.send_post(text)

    print(f"✅ Post Sent Successfully!")

    uri_parts = post.uri.split("/")
    rkey = uri_parts[-1]
    post_url = f"https://bsky.app/profile/{session.handle}/post/{rkey}"
    return post_url


# ================= MAIN EXECUTION =================

if __name__ == "__main__":
    print(f"--- BLUESKY AUTO-POSTER ({TODAY_DATE}) ---")

    # 1. Fetch Data
    data = fetch_data()

    if data:
        print(f"🚀 Found {len(data)} items to post.\n")

        # Har item ke liye loop chalayenge
        for item in data:
            try:
                # Step A: Content generate karo (Function name ab sahi hai)
                post_content = generate_bluesky_post_text(item)

                # Step B: Post kar do
                print(f"posting: {item.get('title')}")
                post_to_bluesky(post_content)
            except Exception as e:
                print(f"❌ Error posting item '{item.get('title')}': {e}")

    else:
        print("❌ Data not found.")

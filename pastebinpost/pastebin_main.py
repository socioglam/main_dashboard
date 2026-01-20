import requests
import datetime

# ================= 1. CONFIGURATION (SETTINGS) =================
API_KEY = ""
URL = "https://pastebin.com/api/api_post.php"


def post_to_pastebin(title, content_text, api_key=None):
    print("\n🚀 [Step 6] Uploading to Pastebin...")

    key = api_key or API_KEY

    if not key:
        print("❌ Error: PASTEBIN_API_KEY missing!")
        return

    data = {
        "api_dev_key": key,
        "api_option": "paste",
        "api_paste_code": content_text,
        "api_paste_name": title,
        "api_paste_expire_date": "N",
        "api_paste_format": "text",  # or 'html5'
        "api_paste_private": "0",
    }

    try:
        response = requests.post(URL, data=data)
        if "pastebin.com" in response.text:
            print(f"✅ PASTEBIN SUCCESS! Link: {response.text}")
            return response.text
        else:
            print(f"❌ Pastebin Error: {response.text}")

    except Exception as e:
        print(f"❌ Pastebin Connection Error: {e}")


if __name__ == "__main__":
    post_to_pastebin("Test Title", "Test Content")

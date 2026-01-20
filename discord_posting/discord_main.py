import requests
import json

# ================= CONFIGURATION =================
TOKEN = ""
CHANNEL_ID = ""


def post_to_discord(content, webhook_url=None, token=None, channel_id=None):
    print("\n🚀 [Step Final] Uploading to Discord (REST API)...")

    # Supports either Bot Token + Channel ID (existing method) or Webhook URL (alternative)
    # But existing code uses Bot Token. Let's stick to that for now unless webhook is passed.

    eff_token = token or TOKEN
    eff_channel_id = channel_id or CHANNEL_ID

    url = f"https://discord.com/api/v10/channels/{eff_channel_id}/messages"
    headers = {"Authorization": f"Bot {eff_token}", "Content-Type": "application/json"}

    payload = {"content": content}

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code in [200, 201]:
            data = response.json()
            print(f"✅ Discord Success! Message sent (ID: {data['id']})")
        else:
            print(f"❌ Discord Failed: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"❌ Discord Connection Error: {e}")


if __name__ == "__main__":
    post_to_discord("Hello! This is a test post using requests.")

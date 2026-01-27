import requests

# अपनी जानकारी यहाँ भरें
ACCESS_TOKEN = ""
CLIENT_KEY = ""
CLIENT_SECRET = ""
INSTANCE_URL = "https://mastodon.social"  # आपका इंस्टेंस URL


def post_to_mastodon(message, access_token=None, instance_url=None):
    eff_token = access_token or ACCESS_TOKEN
    eff_instance = instance_url or INSTANCE_URL

    url = f"{eff_instance}/api/v1/statuses"

    headers = {"Authorization": f"Bearer {eff_token}"}

    data = {
        "status": message,
        "visibility": "public",  # options: public, unlisted, private, direct
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print("✅ Post successful!")
        return response.json().get("url")
    else:
        print(f"❌ Failed: {response.status_code}")
        # print(response.text)
        return response.text


if __name__ == "__main__":
    my_url = "https://yourwebsite.com/my-post"
    msg = f"Check out my new blog post: {my_url} #SEO #Automation"
    post_to_mastodon(msg)

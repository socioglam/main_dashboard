import pytumblr
import os

# ================= 1. CONFIGURATION (SETTINGS) =================
# Credentials from existing file
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_SECRET = ""

BLOG_NAME = "indexingops"


def post_to_tumblr(
    title,
    content_html,
    consumer_key=None,
    consumer_secret=None,
    oauth_token=None,
    oauth_secret=None,
    blog_name=None,
):
    print("\n🚀 [Step 7] Uploading to Tumblr...")

    ck = consumer_key or CONSUMER_KEY
    cs = consumer_secret or CONSUMER_SECRET
    ot = oauth_token or OAUTH_TOKEN
    os_sec = oauth_secret or OAUTH_SECRET
    bn = blog_name or BLOG_NAME

    try:
        client = pytumblr.TumblrRestClient(ck, cs, ot, os_sec)

        response = client.create_text(
            bn, state="published", title=title, body=content_html, format="html"
        )

        if "id" in response:
            post_id = response["id"]
            post_url = f"https://{bn}.tumblr.com/post/{post_id}"
            print(f"✅ TUMBLR SUCCESS! Link: {post_url}")
            return post_url
        else:
            print(f"❌ Tumblr Error: {response}")

    except Exception as e:
        print(f"❌ Tumblr Connection Error: {e}")


if __name__ == "__main__":
    post_to_tumblr("Test Post", "<p>Test Content</p>")

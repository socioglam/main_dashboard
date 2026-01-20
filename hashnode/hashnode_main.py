import requests
import json
import datetime

# ================= 1. CONFIGURATION (SETTINGS) =================
# Currently hardcoded based on existing file, but ideally should come from env or args.
HASHNODE_API_TOKEN = ""
PUBLICATION_ID = "6950ef4f1f7d88975412a1e5"
URL = "https://gql.hashnode.com"


def post_to_hashnode(title, content_html, api_token=None, publication_id=None):
    print("\n🚀 [Step 5] Uploading to Hashnode...")

    eff_token = api_token or HASHNODE_API_TOKEN
    eff_pub_id = publication_id or PUBLICATION_ID

    headers = {"Content-Type": "application/json", "Authorization": eff_token}

    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
        publishPost(input: $input) {
            post {
                title
                slug
                url
            }
        }
    }
    """

    variables = {
        "input": {
            "publicationId": eff_pub_id,
            "title": title,
            "contentMarkdown": content_html,  # Hashnode accepts HTML in markdown field too essentially
            "tags": [
                {"slug": "python", "name": "Python"},
                {"slug": "automation", "name": "Automation"},
                {"slug": "daily-updates", "name": "Daily Updates"},
            ],
        }
    }

    payload = {"query": mutation, "variables": variables}

    try:
        response = requests.post(URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print(f"❌ Hashnode Error: {data['errors']}")
            else:
                post_url = data["data"]["publishPost"]["post"]["url"]
                print(f"✅ HASHNODE SUCCESS! Link: {post_url}")
                return post_url
        else:
            print(f"❌ Hashnode Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Hashnode Connection Error: {e}")


if __name__ == "__main__":
    # Test run
    post_to_hashnode("Test Post", "<p>Test Content</p>")

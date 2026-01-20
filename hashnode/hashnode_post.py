import requests
import json

HASHNODE_API_TOKEN = "8158c853-c20b-41ff-8ae1-979eeda6508e"
PUBLICATION_ID = "6950ef4f1f7d88975412a1e5"

if not HASHNODE_API_TOKEN:
    raise ValueError("HASHNODE_API_TOKEN .env में नहीं मिला!")

if not PUBLICATION_ID:
    raise ValueError("HASHNODE_PUBLICATION_ID .env में नहीं मिला!")

URL = "https://gql.hashnode.com"

headers = {
    "Content-Type": "application/json",
    "Authorization": HASHNODE_API_TOKEN
}

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

html_content = """
# This is my first post that is successful

Ye humara automatic post hai. <a href="https://www.flightbycall.com/klm-british-airways-flight-cancellations-klm/">Yahan Click Karein</a> guide dekhne ke liye.
"""

variables = {
    "input": {
        "publicationId": PUBLICATION_ID,
        "title": "This is my first Post on Hash Node Platform",
        "contentMarkdown": html_content, # Updated Content
        "tags": [
            {
                "slug": "python",
                "name": "Python"
            },
            {
                "slug": "hashnode",
                "name": "Hashnode"
            }
        ],
    }
}
# -----------------------------

payload = {
    "query": mutation,
    "variables": variables
}

response = requests.post(URL, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    data = response.json()
    if "errors" in data:
        print("Error:", json.dumps(data["errors"], indent=2, ensure_ascii=False))
    else:
        post_url = data["data"]["publishPost"]["post"]["url"]
        print("Successfully Posted on Hashnode")
        print("URL:", post_url)
else:
    print("HTTP Error:", response.status_code)
    print(response.text)
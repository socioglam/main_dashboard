import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Variables (Ya toh .env se lo ya yahan direct paste kar do testing ke liye)
ACCESS_TOKEN = "AQRXeZvcDdhes4zALgZnsqOlYa_TGnPZ7zlwRH660ThM7EAYqbWng_9OWQs6LQcfUm_RwFhmhRN8tPb5aJbKjGdeCLT1i5nvpg2_STmSsljGqB1LCTsUlPgSAYaDQjLXtMDHlvUrem-3tEaRb_qZk88jtvVPKZPqyr61q-iXhARho29nb5taNcPwJDQwXubk4ae7vYwhm2kTmiNIByA"
PERSON_URN = "urn:li:person:9tm89BfREv" # Jo aapko abhi mili

url = "https://api.linkedin.com/v2/ugcPosts"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

# Aapka blog content
blog_link = "https://karan.hashnode.dev" # Apna asli blog link yahan dalein
message = "Doston! Maine Python script se LinkedIn par ye post automate ki hai. 🚀 #Python #Automation #API"

post_data = {
    "author": PERSON_URN,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": message
            },
            "shareMediaCategory": "ARTICLE",
            "media": [
                {
                    "status": "READY",
                    "description": {
                        "text": "Checkout my latest automation project!"
                    },
                    "originalUrl": blog_link,
                    "title": {
                        "text": "Automated LinkedIn Post via Python API"
                    }
                }
            ]
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

try:
    response = requests.post(url, headers=headers, json=post_data)
    if response.status_code == 201:
        print("🚀 BOOM! Aapki post LinkedIn par LIVE ho gayi hai.")
        print("Apna LinkedIn profile check karo!")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
except Exception as e:
    print(f"❌ Connection Error: {e}")
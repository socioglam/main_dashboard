import requests
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("LINKEDIN_CLIENT_ID")
client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
# Sabse zaroori: Browser URL se mila hua code yahan dalein
auth_code = "AQSqopxrvTB29cq6OrY3TIIlF9v4tKEF3JZRoRaq5ALgH56gmFTzCWWDQNOKrO0LDpUKE4XoKoOwPTbE3eCtBU5VABciyc7xs4KtfE_kZE_7UexQNvPAi3IYCOngYj-5lVZxL7ePsuBT2QS8f-T_-gtmYDNIdRoZkfOq5tE0_CcnYWZnHMzvePEjiFE7OHQLQaQCjAfSy0BrMXm2vN4" 
redirect_uri = "http://localhost:8080"

url = "https://www.linkedin.com/oauth/v2/accessToken"

payload = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": redirect_uri,
    "client_id": client_id,
    "client_secret": client_secret,
}

# Headers add kar diye hain safety ke liye
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

try:
    response = requests.post(url, data=payload, headers=headers)
    token_res = response.json()

    if "access_token" in token_res:
        print("✅ Success! Token mil gaya.")
        print(f"Token: {token_res['access_token']}")
        print(f"Expires in: {token_res['expires_in'] // 86400} days") # Seconds ko days mein badla
    else:
        print("❌ Error Response:", token_res)
        if token_res.get('error') == 'invalid_grant':
            print("💡 Tip: Aapka code expire ho gaya hai ya use ho chuka hai. Naya code generate karein.")

except Exception as e:
    print(f"❌ Connection Error: {e}")
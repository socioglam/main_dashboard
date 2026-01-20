from requests_oauthlib import OAuth1Session
from urllib.parse import urlparse, parse_qs

# 1. Tumhari Consumer Keys
consumer_key = "XhU5dnzxqBRlOt2ZXaYve69fP0I6ZHL7N2bi7GIjdv6EFEowkD"
consumer_secret = "1i55CMnE3FCb15xUwEHeIe2yFppP7nW4FDhC2BkFd3ac0I2oGV"

# 2. Request Token Mangwana
request_token_url = 'https://www.tumblr.com/oauth/request_token'
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
fetch_response = oauth.fetch_request_token(request_token_url)
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

# 3. Authorization Link Generate Karna
base_authorization_url = 'https://www.tumblr.com/oauth/authorize'
authorization_url = oauth.authorization_url(base_authorization_url)

print('Please go here and authorize:', authorization_url)

# --- USER INPUT ---
redirect_response = input('Paste the full redirect URL here: ') 

# FIX: URL se manually verifier nikalna
parsed_url = urlparse(redirect_response)
verifier = parse_qs(parsed_url.query)['oauth_verifier'][0]

# 4. Final Keys Nikalna (Ab hum verifier explicitly pass kar rahe hain)
oauth = OAuth1Session(consumer_key,
                          client_secret=consumer_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier) # <-- Ye line fix hai

oauth_token_url = 'https://www.tumblr.com/oauth/access_token'
oauth_tokens = oauth.fetch_access_token(oauth_token_url)

print("\n\n!!! YE RAHI TUMHARI ASLI KEYS (Inhe Copy kar lo) !!!")
print(f"oauth_token = '{oauth_tokens['oauth_token']}'")
print(f"oauth_token_secret = '{oauth_tokens['oauth_token_secret']}'")
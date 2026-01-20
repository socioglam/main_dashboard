import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("HASH_NODE")

query = """
{
  me {
    publications(first: 5) {
      edges {
        node {
          id
          title
        }
      }
    }
  }
}
"""

headers = {"Authorization": token}
response = requests.post("https://gql.hashnode.com/", json={'query': query}, headers=headers)
data = response.json()

if 'data' in data and data['data']['me']['publications']['edges']:
    for pub in data['data']['me']['publications']['edges']:
        print(f"Publication Title: {pub['node']['title']}")
        print(f"Sahi wali ID ye hai: {pub['node']['id']}") # Is ID ko .env mein dalein
else:
    print("Kuch gadbad hai, response check karein:", data)
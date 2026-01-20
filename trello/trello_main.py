import requests

API_KEY = ""
TOKEN = ""
BOARD_ID = "696fa329684dc79430c68458"


def get_or_create_list_id():
    """
    Yeh function check karega ki koi List hai ya nahi.
    Agar nahi hai, toh ek nayi list create karega.
    """
    # 1. Check existing lists
    url = f"https://api.trello.com/1/boards/{BOARD_ID}/lists"
    query = {"key": API_KEY, "token": TOKEN}

    response = requests.get(url, params=query)
    lists = response.json()

    if len(lists) > 0:
        # Agar list pehle se hai, toh pehli wali use karenge
        print(f"✅ Existing List Found: {lists[0]['name']}")
        return lists[0]["id"]
    else:
        # 2. Agar list nahi hai, toh nayi banayenge
        print("⚠️ No list found. Creating 'To Do' list...")
        create_url = "https://api.trello.com/1/lists"
        create_params = {
            "key": API_KEY,
            "token": TOKEN,
            "name": "To Do",
            "idBoard": BOARD_ID,
        }
        create_res = requests.post(create_url, params=create_params)
        new_list = create_res.json()
        print(f"✅ New List Created: {new_list['name']}")
        return new_list["id"]


def post_content(title, content):
    list_id = get_or_create_list_id()

    url = "https://api.trello.com/1/cards"

    params = {
        "key": API_KEY,
        "token": TOKEN,
        "idList": list_id,  # Auto-detected List ID
        "name": title,
        "desc": content,
    }

    r = requests.post(url, params=params)

    if r.status_code == 200:
        print("\n🎉 Success! Card Posted.")
        print("Card URL:", r.json()["shortUrl"])
    else:
        print("❌ Error:", r.text)


# post_content(
#     "My First Automated Post",
#     """
#     🚀 Yeh card Python script se bana hai.
#
#     Details:
#     - Board: indexingops
#     - Account: salessales35
#     """,
# )

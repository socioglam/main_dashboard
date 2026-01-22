import requests

API_KEY = ""
TOKEN = ""
BOARD_ID = ""


def get_or_create_list_id(api_key, token, board_id):
    """
    Yeh function check karega ki koi List hai ya nahi.
    Agar nahi hai, toh ek nayi list create karega.
    """
    # 1. Check existing lists
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    query = {"key": api_key, "token": token}

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
            "key": api_key,
            "token": token,
            "name": "To Do",
            "idBoard": board_id,
        }
        create_res = requests.post(create_url, params=create_params)
        new_list = create_res.json()
        print(f"✅ New List Created: {new_list['name']}")
        return new_list["id"]


def post_content(title, content, api_key=None, token=None, board_id=None):
    eff_key = api_key or API_KEY
    eff_token = token or TOKEN
    eff_board_id = board_id or BOARD_ID

    if not eff_board_id:
        print("❌ Error: Board ID is required.")
        return None

    list_id = get_or_create_list_id(eff_key, eff_token, eff_board_id)

    url = "https://api.trello.com/1/cards"

    params = {
        "key": eff_key,
        "token": eff_token,
        "idList": list_id,  # Auto-detected List ID
        "name": title,
        "desc": content,
    }

    r = requests.post(url, params=params)

    if r.status_code == 200:
        print("Card URL:", r.json()["shortUrl"])
        return r.json()["shortUrl"]
    else:
        print("❌ Error:", r.text)
        return None

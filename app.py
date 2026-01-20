import requests
import datetime
import concurrent.futures
import time
import os
import json
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    stream_with_context,
    Response,
)

# Import your existing posting modules
# Ensure these modules are in the same directory or properly installed
try:
    from blogger_posting import blogger_main
    from wordpress_posting import wordpress_main
    from linkedin import linkedin_main
    from dev_to import devto_main
    from blsky import blsky_main
    from hashnode import hashnode_main
    from pastebinpost import pastebin_main
    from tumblr import tumblr_main
    from discord_posting import discord_main
    from mastodon import mastodon as mastodon_main
    from pixelfed import pixelfed_post
except ImportError as e:
    print(f"Warning: Some modules could not be imported: {e}")

app = Flask(__name__)
app.secret_key = "supersecretkey"

SOURCE_API_URL = "https://www.livyalife.com/api/all-links-data"
# FIXED_LINK removed as requested

ACCOUNTS_FILE = "accounts.json"  # Legacy, we now load per module

MODULE_PATHS = {
    "linkedin": "linkedin/users.json",
    "dev_to": "dev_to/users.json",
    "bluesky": "blsky/users.json",
    "hashnode": "hashnode/users.json",
    "pastebin": "pastebinpost/users.json",
    "tumblr": "tumblr/users.json",
    "discord": "discord_posting/users.json",
    "mastodon": "mastodon/users.json",
    "pixelfed": "pixelfed/users.json",
}

MODULE_SCHEMAS = {
    "linkedin": ["credentials_file"], 
    "dev_to": ["api_key"],
    "bluesky": ["handle", "password"],
    "hashnode": ["api_token", "publication_id"],
    "pastebin": ["api_key"],
    "tumblr": [
        "consumer_key",
        "consumer_secret",
        "oauth_token",
        "oauth_secret",
        "blog_name",
    ],
    "discord": ["token", "channel_id", "webhook_url"],
    "mastodon": ["access_token", "instance_url"],
    "pixelfed": ["access_token", "instance_url"],
}

def get_today_date():
    return datetime.date.today().strftime("%Y-%m-%d")


def fetch_central_data(logger=print):
    logger(
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ⏳ Fetching data from API..."
    )
    try:
        response = requests.get(SOURCE_API_URL)
        if response.status_code == 200:
            data = response.json()
            if data:
                logger(
                    f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ✅ Data Fetched: {len(data)} items."
                )
                return data
            else:
                logger("❌ API returned empty list.")
                return None
        else:
            logger(f"❌ API Error: {response.status_code}")
            return None
    except Exception as e:
        logger(f"❌ Connection Error during fetch: {e}")
        return None

def generate_html_content(data):
    today = get_today_date()
    full_html = f"<p>Here is the list of latest updates fetched on {today}. Check them out below:</p><hr>"
    for item in data:
        api_title = item.get("title", "Unknown Title")
        target_url = item.get("target_url", "#")
        description = item.get("description", "No description available.")

        full_html += f"""
        <div style="margin-bottom: 30px; padding: 15px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9;">
            <h3 style="margin-top: 0; color: #333;">{api_title}</h3>
            
            <p style="margin-bottom: 10px; color: #0056b3; word-break: break-all;">
                <strong>Target URL:</strong><br>
                <a href="{target_url}" rel="dofollow" target="_blank">{target_url}</a>
            </p>

            <p style="margin-top: 15px; color: #555;">
                <strong>Description:</strong><br>
                {description}
            </p>
        </div>
        """
    return full_html

def run_blogger(account, html_content, post_title):
    try:
        base_dir = "blogger_posting"
        creds = account.get("credentials_file")
        if creds and not os.path.exists(creds):
            creds = os.path.join(base_dir, creds)
        token = account.get("token_file")
        if token and not os.path.exists(token):
            token = os.path.join(base_dir, token)

        url = blogger_main.post_to_blogger(
            post_title,
            html_content,
            credentials_file=creds,
            token_file=token,
            blog_id=account.get("blog_id"),
        )
        if url:
            return f"✅ Blogger: SUCCESS ({url})"
        return "❌ Blogger: FAILED"
    except Exception as e:
        return f"❌ Blogger: ERROR ({e})"


def run_wordpress(account, html_content, post_title):
    try:
        wordpress_main.post_to_wordpress(
            post_title,
            html_content,
            username=account.get("username"),
            password=account.get("password"),
            client_id=account.get("client_id"),
            client_secret=account.get("client_secret"),
            site_domain=account.get("site_domain"),
        )
        return "✅ WordPress: COMPLETED"
    except Exception as e:
        return f"❌ WordPress: ERROR ({e})"


def run_linkedin(account, data_items):
    try:
        text = linkedin_main.generate_linkedin_post_text(data_items)
        today = get_today_date()
        main_link_title = f"Daily Updates - {today}"
        main_link_desc = (
            "Check out the latest trending links from our feed."
        )

        creds_file = account.get("credentials_file")
        creds = None
        if creds_file and os.path.exists(creds_file):
            if not os.path.exists(creds_file):
                creds_file = os.path.join("linkedin", creds_file)

            if os.path.exists(creds_file):
                with open(creds_file, "r") as f:
                    creds = json.load(f)

        if not creds:
            creds = account 

        first_link = data_items[0].get("target_url", "") if data_items else ""

        linkedin_main.post_to_linkedin(
            message=text,
            link_url=first_link,
            link_title=main_link_title,
            link_desc=main_link_desc,
            credentials=creds,
        )
        return "✅ LinkedIn: COMPLETED"
    except Exception as e:
        return f"❌ LinkedIn: ERROR ({e})"


def run_devto(account, html_content, post_title):
    try:
        devto_main.post_to_devto(
            post_title, html_content, api_key=account.get("api_key")
        )
        return "✅ Dev.to: COMPLETED"
    except Exception as e:
        return f"❌ Dev.to: ERROR ({e})"


def run_bluesky(account, data_items):
    try:
        text = blsky_main.generate_bluesky_post_text(data_items)
        first_link = data_items[0].get("target_url", "") if data_items else ""
        
        blsky_main.post_to_bluesky(
            text,
            first_link,
            handle=account.get("handle"),
            password=account.get("password"),
        )
        return "✅ Bluesky: COMPLETED"
    except Exception as e:
        return f"❌ Bluesky: ERROR ({e})"


def run_hashnode(account, html_content, post_title):
    try:
        hashnode_main.post_to_hashnode(
            post_title,
            html_content,
            api_token=account.get("api_token"),
            publication_id=account.get("publication_id"),
        )
        return "✅ Hashnode: COMPLETED"
    except Exception as e:
        return f"❌ Hashnode: ERROR ({e})"


def run_pastebin(account, html_content, post_title):
    try:
        pastebin_main.post_to_pastebin(
            post_title, html_content, api_key=account.get("api_key")
        )
        return "✅ Pastebin: COMPLETED"
    except Exception as e:
        return f"❌ Pastebin: ERROR ({e})"


def run_tumblr(account, html_content, post_title):
    try:
        tumblr_main.post_to_tumblr(
            post_title,
            html_content,
            consumer_key=account.get("consumer_key"),
            consumer_secret=account.get("consumer_secret"),
            oauth_token=account.get("oauth_token"),
            oauth_secret=account.get("oauth_secret"),
            blog_name=account.get("blog_name"),
        )
        return "✅ Tumblr: COMPLETED"
    except Exception as e:
        return f"❌ Tumblr: ERROR ({e})"


def run_discord(account, data_items):
    try:
        text = linkedin_main.generate_linkedin_post_text(data_items)
        # Removed FIXED_LINK append
        full_message = text 
        discord_main.post_to_discord(
            full_message,
            token=account.get("token"),
            channel_id=account.get("channel_id"),
            webhook_url=account.get("webhook_url"),
        )
        return "✅ Discord: COMPLETED"
    except Exception as e:
        return f"❌ Discord: ERROR ({e})"


def run_mastodon(account, data_items):
    try:
        text = linkedin_main.generate_linkedin_post_text(data_items)
        # Removed FIXED_LINK append
        full_message = text
        mastodon_main.post_to_mastodon(
            full_message,
            access_token=account.get("access_token"),
            instance_url=account.get("instance_url"),
        )
        return "✅ Mastodon: COMPLETED"
    except Exception as e:
        return f"❌ Mastodon: ERROR ({e})"


def run_pixelfed(account, data_items):
    try:
        text = linkedin_main.generate_linkedin_post_text(data_items)
        # Removed FIXED_LINK append
        full_message = text
        pixelfed_post.post_to_pixelfed(
            full_message,
            access_token=account.get("access_token"),
            instance_url=account.get("instance_url"),
        )
        return "✅ Pixelfed: COMPLETED"
    except Exception as e:
        return f"❌ Pixelfed: ERROR ({e})"


# ================= 5. FLASK ROUTES =================


@app.route("/")
def index():
    modules = list(MODULE_PATHS.keys())
    return render_template("dashboard.html", modules=modules)


@app.route("/credentials")
def credentials():
    return render_template("credentials.html", module_keys=MODULE_PATHS.keys())


@app.route("/api/credentials/<platform>")
def get_credentials(platform):
    path = MODULE_PATHS.get(platform)
    if not path:
        return jsonify({"error": "Platform not found"}), 404

    accounts = []
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                accounts = json.load(f)
        except Exception as e:
            print(f"Error reading {path}: {e}")

    schema = MODULE_SCHEMAS.get(platform, [])
    if not schema and accounts:
        schema = list(accounts[0].keys())

    return jsonify({"accounts": accounts, "schema": schema})


@app.route("/credentials/update", methods=["POST"])
def update_credentials():
    data = request.json
    platform = data.get("platform")
    new_account = data.get("account_data")

    path = MODULE_PATHS.get(platform)
    if not path or not new_account:
        return jsonify({"error": "Invalid data"}), 400

    accounts = []
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                accounts = json.load(f)
        except:
            pass

    accounts.append(new_account)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        json.dump(accounts, f, indent=4)

    return jsonify({"status": "success"})


@app.route("/publish", methods=["POST"])
def publish():
    req_data = request.json
    target_platform = req_data.get("platform")

    import queue
    import threading

    log_queue = queue.Queue()

    def logger_func(msg):
        log_queue.put(f"{msg}\n")

    def background_task():
        try:
            today = get_today_date()
            post_title = f"🔥 Trending Now: Today's Top Updates & Viral Links ({today})"

            logger_func("==================================================")
            logger_func(f"   SERVER MULTI-ACCOUNT POSTER - {today}")
            logger_func("==================================================")

            # 1. Fetch Data
            data = fetch_central_data(logger_func)
            if not data:
                logger_func("❌ Critical Failure: No data. Exiting.")
                log_queue.put(None)
                return

            # 2. Generate Content
            full_html = generate_html_content(data)

            # 3. Load Configs
            accounts_config = {}
            for key, path in MODULE_PATHS.items():
                if target_platform and key != target_platform:
                    continue

                if os.path.exists(path):
                    try:
                        with open(path, "r") as f:
                            accounts_config[key] = json.load(f)
                            logger_func(
                                f"   ✔️ Loaded {len(accounts_config[key])} accounts for {key}"
                            )
                    except Exception as e:
                        logger_func(f"   ❌ Error loading {path}: {e}")
                        accounts_config[key] = []
                else:
                    logger_func(f"   ⚠️ Config not found: {path} (Skipping)")
                    accounts_config[key] = []

            # 4. Dispatch Tasks
            logger_func("🚀 Starting posting process...")

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = []

                def add_tasks(module_name, func, uses_html=True):
                    if target_platform and target_platform != module_name:
                        return
                    for acc in accounts_config.get(module_name, []):
                        args = (
                            (acc, full_html, post_title) if uses_html else (acc, data)
                        )
                        futures.append(executor.submit(func, *args))

                add_tasks("linkedin", run_linkedin, uses_html=False)
                add_tasks("dev_to", run_devto)
                add_tasks("bluesky", run_bluesky, uses_html=False)
                add_tasks("hashnode", run_hashnode)
                add_tasks("pastebin", run_pastebin)
                add_tasks("tumblr", run_tumblr)
                add_tasks("discord", run_discord, uses_html=False)
                add_tasks("mastodon", run_mastodon, uses_html=False)
                add_tasks("pixelfed", run_pixelfed, uses_html=False)

                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        logger_func(
                            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {result}"
                        )
                    except Exception as exc:
                        logger_func(f"❌ Exception in task: {exc}")

            logger_func("🏁 All tasks completed.")
        except Exception as e:
            logger_func(f"CRITICAL ERROR: {e}")
        finally:
            log_queue.put(None)

    thread = threading.Thread(target=background_task)
    thread.start()

    def generate():
        while True:
            msg = log_queue.get()
            if msg is None:
                break
            yield msg

    return Response(stream_with_context(generate()), mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True, port=5432)
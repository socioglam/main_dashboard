import concurrent.futures
import threading
import json
import os
import datetime
import requests
from flask import current_app

# Import platform modules
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
    from mastodon import mastodon as mastodon_main
    from pixelfed import pixelfed_post
    from trello import trello_main
except ImportError as e:
    print(f"Warning: Some modules could not be imported: {e}")


# Re-implement data fetching here to avoid context issues or pass URL
def fetch_data_internal(source_url, logger_func):
    logger_func(
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ⏳ Fetching data from API..."
    )
    try:
        response = requests.get(source_url)
        if response.status_code == 200:
            data = response.json()
            if data:
                logger_func(
                    f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ✅ Data Fetched: {len(data)} items."
                )
                return data
            else:
                logger_func("❌ API returned empty list.")
                return None
        else:
            logger_func(f"❌ API Error: {response.status_code}")
            return None
    except Exception as e:
        logger_func(f"❌ Connection Error during fetch: {e}")
        return None


def get_today_date():
    return datetime.date.today().strftime("%Y-%m-%d")


def generate_html_internal(data):
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


# Wrapper Functions
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
        main_link_desc = "Check out the latest trending links from our feed."

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
        devTo_url = devto_main.post_to_devto(
            post_title, html_content, api_key=account.get("api_key")
        )
        return f"✅ Dev.to: {devTo_url}"
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
        hashnode_url = hashnode_main.post_to_hashnode(
            post_title,
            html_content,
            api_token=account.get("api_token"),
            publication_id=account.get("publication_id"),
        )
        return f"✅ Hashnode: {hashnode_url}"
    except Exception as e:
        return f"❌ Hashnode: ERROR ({e})"


def run_pastebin(account, data):
    try:
        today = datetime.date.today().strftime("%Y-%m-%d")
        post_title = f"🔥 Trending Updates - {today}"

        content = "Here are the latest updates:\n\n"
        for item in data:
            item_title = item.get("title", "No Title")
            item_url = item.get("target_url", "#")
            content += f"**{item_title}**\n{item_url}\n\n"

        content += "\n(Automated via Poster Service)"
        sucess_post_res = pastebin_main.post_to_pastebin(
            post_title, content, api_key=account.get("api_key")
        )
        return f"✅ Pastebin: {sucess_post_res}"
    except Exception as e:
        return f"❌ Pastebin: ERROR ({e})"


def run_tumblr(account, html_content, post_title):
    try:
        tumbler_url = tumblr_main.post_to_tumblr(
            post_title,
            html_content,
            consumer_key=account.get("consumer_key"),
            consumer_secret=account.get("consumer_secret"),
            oauth_token=account.get("oauth_token"),
            oauth_secret=account.get("oauth_secret"),
            blog_name=account.get("blog_name"),
        )
        return f"✅ Tumblr: { tumbler_url }"
    except Exception as e:
        return f"❌ Tumblr: ERROR ({e})"


def run_discord(account, data_items):
    try:
        text = linkedin_main.generate_linkedin_post_text(data_items)
        full_message = text
        discord_id = discord_main.post_to_discord(
            full_message,
            token=account.get("token"),
            channel_id=account.get("channel_id"),
            webhook_url=account.get("webhook_url"),
        )
        return f"✅ Discord: {discord_id}"
    except Exception as e:
        return f"❌ Discord: ERROR ({e})"


def run_mastodon(account, data_items):
    try:
        text = linkedin_main.generate_linkedin_post_text(data_items)
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
        full_message = text
        pixelfed_post.post_to_pixelfed(
            full_message,
            access_token=account.get("access_token"),
            instance_url=account.get("instance_url"),
        )
        return "✅ Pixelfed: COMPLETED"
    except Exception as e:
        return f"❌ Pixelfed: ERROR ({e})"


def run_trello(account, data):
    try:
        today = datetime.date.today().strftime("%Y-%m-%d")
        title = f"🔥 Trending Updates - {today}"

        content = "Here are the latest updates:\n\n"
        for item in data:
            item_title = item.get("title", "No Title")
            item_url = item.get("target_url", "#")
            content += f"**{item_title}**\n{item_url}\n\n"

        content += "\n(Automated via Poster Service)"

        trello_url = trello_main.post_content(
            title,
            content,
            api_key=account.get("api_key"),
            token=account.get("token"),
            board_id=account.get("board_id"),
        )
        return f"✅ Trello: { trello_url }"
    except Exception as e:
        return f"❌ Trello: ERROR ({e})"


def start_poster_thread(logger, target_platform, module_paths, source_api_url):

    def background_task():
        try:
            today = get_today_date()
            post_title = f"🔥 Trending Now: Today's Top Updates & Viral Links ({today})"

            logger.log("==================================================")
            logger.log(f"   SERVER MULTI-ACCOUNT POSTER - {today}")
            logger.log("==================================================")

            # 1. Fetch Data
            data = fetch_data_internal(source_api_url, logger.log)
            if not data:
                logger.log("❌ Critical Failure: No data. Exiting.")
                logger.close()
                return

            # 2. Generate Content
            full_html = generate_html_internal(data)

            # 3. Load Configs
            accounts_config = {}
            for key, path in module_paths.items():
                if target_platform and key != target_platform:
                    continue

                if os.path.exists(path):
                    try:
                        with open(path, "r") as f:
                            accounts_config[key] = json.load(f)
                            logger.log(
                                f"   ✔️ Loaded {len(accounts_config[key])} accounts for {key}"
                            )
                    except Exception as e:
                        logger.log(f"   ❌ Error loading {path}: {e}")
                        accounts_config[key] = []
                else:
                    logger.log(f"   ⚠️ Config not found: {path} (Skipping)")
                    accounts_config[key] = []

            # 4. Dispatch Tasks
            logger.log("🚀 Starting posting process...")

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
                add_tasks("pastebin", run_pastebin, uses_html=False)
                add_tasks("tumblr", run_tumblr)
                add_tasks("discord", run_discord, uses_html=False)
                add_tasks("mastodon", run_mastodon, uses_html=False)
                add_tasks("mastodon", run_mastodon, uses_html=False)
                add_tasks("pixelfed", run_pixelfed, uses_html=False)
                add_tasks("trello", run_trello, uses_html=False)
                add_tasks("blogger_posting", run_blogger)
                add_tasks("wordpress_posting", run_wordpress)

                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        logger.log(
                            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {result}"
                        )
                    except Exception as exc:
                        logger.log(f"❌ Exception in task: {exc}")

            logger.log("🏁 All tasks completed.")
        except Exception as e:
            logger.log(f"CRITICAL ERROR: {e}")
        finally:
            logger.close()

    thread = threading.Thread(target=background_task)
    thread.start()

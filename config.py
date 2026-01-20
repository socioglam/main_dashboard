import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecretkey"
    SOURCE_API_URL = "https://www.livyalife.com/api/all-links-data"
    ACCOUNTS_FILE = "accounts.json"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    MODULE_PATHS = {
        "linkedin": os.path.join(BASE_DIR, "linkedin/users.json"),
        "dev_to": os.path.join(BASE_DIR, "dev_to/users.json"),
        "bluesky": os.path.join(BASE_DIR, "blsky/users.json"),
        "hashnode": os.path.join(BASE_DIR, "hashnode/users.json"),
        "pastebin": os.path.join(BASE_DIR, "pastebinpost/users.json"),
        "tumblr": os.path.join(BASE_DIR, "tumblr/users.json"),
        "discord": os.path.join(BASE_DIR, "discord_posting/users.json"),
        "mastodon": os.path.join(BASE_DIR, "mastodon/users.json"),
        "pixelfed": os.path.join(BASE_DIR, "pixelfed/users.json"),
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

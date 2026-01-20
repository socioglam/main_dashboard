import requests
import datetime
from flask import current_app


def get_today_date():
    return datetime.date.today().strftime("%Y-%m-%d")


def fetch_central_data(logger_func=print):
    source_url = current_app.config.get("SOURCE_API_URL")
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

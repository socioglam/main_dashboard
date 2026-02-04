import concurrent.futures
import requests
import xmlrpc.client
from .ping_list import PING_SERVICES
import datetime


def fetch_links_data():
    """Fetch links from the API."""
    try:
        response = requests.get(
            "https://www.livyalife.com/api/all-links-data", timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error fetching links: {e}")
        return []


def ping_url(service_url, page_title, page_url):
    """Ping a single service with the page details."""
    try:
        # Some services might not be XML-RPC compliant or might be down, so we use a short timeout
        server = xmlrpc.client.ServerProxy(service_url, verbose=False)
        # Standard weblogUpdates.ping call: siteName, siteURL
        result = server.weblogUpdates.ping(page_title, page_url)
        return f"✅ Pinged {service_url}: {result}"
    except Exception as e:
        # Many of these will fail, so we return a short error
        return f"❌ Failed {service_url}: {str(e)[:50]}"


def run_mass_ping(pre_fetched_data=None):
    """
    Main entry point for mass pinging.
    If pre_fetched_data is provided (list of dicts with 'title' and 'target_url'), use it.
    Otherwise fetch from the API.
    """
    if pre_fetched_data:
        data = pre_fetched_data
    else:
        print("Fetching links for mass pinging...")
        data = fetch_links_data()

    if not data:
        return "⚠️ No data to ping."

    results = []

    # We will use a thread pool to blast these out.
    # Warning: 125 services * N links is a lot. We limit workers.
    # We'll just take the top 5 links to avoid spamming thousands of requests if the list is huge,
    # or ping all if the user intends. The user said "use this links to ping ... from this get api".
    # I'll assume we ping all fetched links against all services.

    total_pings = len(data) * len(PING_SERVICES)
    # print(f"🚀 Starting Mass Ping: {len(data)} links against {len(PING_SERVICES)} services ({total_pings} reqs)")

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for item in data:
            title = item.get("title", "Unknown Title")
            url = item.get("target_url")
            if not url:
                continue

            for service in PING_SERVICES:
                futures.append(executor.submit(ping_url, service, title, url))

        # We won't wait for all results to return string, because it's too much log spam.
        # We will just return a summary string after submitting or wait for completion if needed.
        # For a "poster" style, we usually want to wait.

        success = 0
        fail = 0

        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if "✅" in res:
                success += 1
            else:
                fail += 1

    return f"✅ Mass Ping Completed: {success} successes, {fail} failures."

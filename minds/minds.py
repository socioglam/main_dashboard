from seleniumbase import Driver
import time
import os

# Your Credentials
USERNAME = ""
PASSWORD = ""


def post_to_minds_updated(message):
    # 'uc=True' handles the Cloudflare bypass
    driver = Driver(browser="chrome", uc=True, headless=False)

    try:
        print("🚀 Opening Minds login page...")
        driver.uc_open_with_reconnect("https://www.minds.com/login", 6)
        time.sleep(5)

        print("🔍 Searching for login fields...")

        selectors = [
            'input[name="username"]',
            'input[type="text"]',
            'input[autocomplete="username"]',
            "#username",
        ]

        found = False
        for selector in selectors:
            if driver.is_element_visible(selector):
                driver.type(selector, USERNAME)
                found = True
                break

        if not found:
            driver.save_screenshot("login_failed_view.png")
            print(
                "❌ Could not find username field. Screenshot saved as 'login_failed_view.png'"
            )
            return

        # Handle Password
        driver.type('input[type="password"]', PASSWORD)

        driver.click('button[type="submit"]')

        print("⏳ Authenticating...")
        time.sleep(10)

        print("📤 Injecting post via API...")

        cookies = driver.get_cookies()
        xsrf_token = next(
            (c["value"] for c in cookies if c["name"] == "XSRF-TOKEN"), None
        )

        if not xsrf_token:
            print("❌ Login failed: No XSRF token found. Are your credentials correct?")
            return

        api_script = f"""
        fetch('/api/v1/newsfeed', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
                'X-XSRF-TOKEN': '{xsrf_token}'
            }},
            body: JSON.stringify({{
                'message': '{message}',
                'access': 2
            }})
        }}).then(r => r.json()).then(d => console.log(d));
        """

        driver.execute_script(api_script)
        print("✅ Post request sent! Check your Minds profile in 30 seconds.")
        time.sleep(5)

    except Exception as e:
        print(f"⚠️ An error occurred: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    msg = "Success! Automated post via SeleniumBase UC Mode. 🤖"
    post_to_minds_updated(msg)

import requests
import json
import os

# Pixelfed Credentials
ACCESS_TOKEN = ""
INSTANCE_URL = "https://pixelfed.de"


def post_to_pixelfed(message, image_path=None):
    url = f"{INSTANCE_URL}/api/v1/statuses"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "User-Agent": "MyPixelfedBot/1.0",
        "Accept": "application/json",
    }

    # Pixelfed usually requires an image, but supports text-only on some instances.
    # If image_path is provided, we upload it first.
    media_ids = []
    if image_path:
        # TODO: Implement media upload if needed
        pass

    data = {
        "status": message,
        "visibility": "public",
    }

    # If we had media: data['media_ids[]'] = media_ids

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("✅ Pixelfed Post successful!")
        try:
            print("Link:", response.json().get("url"))
        except:
            print("Response:", response.text)
        return True
    else:
        print(f"❌ Pixelfed Failed: {response.status_code}")
        print(response.text)
        return False


def upload_media(access_token, instance_url):
    # Create a dummy image
    import time

    # Let's create a minimal 1x1 GIF locally to avoid network issues
    try:
        # Minimal 1x1 GIF bytes
        dummy_gif = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x01\x44\x00\x3b"
        image_path = "temp_pixel_test.gif"  # changed extension to gif
        with open(image_path, "wb") as f:
            f.write(dummy_gif)
    except Exception as e:
        print(f"Error creating dummy image: {e}")
        return None

    # Upload
    media_url = f"{instance_url}/api/v1/media"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "MyPixelfedBot/1.0",
    }
    files = {"file": open(image_path, "rb")}
    print("Uploading media...")
    response = requests.post(media_url, headers=headers, files=files)
    if response.status_code == 200:
        media_id = response.json().get("id")
        print(f"Media uploaded! ID: {media_id}")
        return media_id
    else:
        print(f"Media upload failed: {response.text}")
        return None


def post_to_pixelfed(message, image_path=None, access_token=None, instance_url=None):
    eff_token = access_token or ACCESS_TOKEN
    eff_instance = instance_url or INSTANCE_URL

    # If no image provided, upload a dummy one
    media_id = upload_media(eff_token, eff_instance)
    if not media_id:
        print("Failed to upload media, cannot post to Pixelfed.")
        return False

    url = f"{eff_instance}/api/v1/statuses"
    headers = {
        "Authorization": f"Bearer {eff_token}",
        "User-Agent": "MyPixelfedBot/1.0",
    }
    data = {"status": message, "media_ids": [media_id], "visibility": "public"}

    print("Posting status with media...")
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("✅ Pixelfed Post successful!")
        print("Link:", response.json().get("url"))
        return True
    else:
        print(f"❌ Pixelfed Failed: {response.status_code}")
        print(response.text)
        return False


if __name__ == "__main__":
    post_to_pixelfed(
        "Hello Pixelfed! Testing automated posting from my script. #automation #python"
    )

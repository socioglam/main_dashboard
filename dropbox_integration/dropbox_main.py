import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import AuthError
import datetime
import re


def sanitize_filename(title):
    # Remove invalid characters for filenames
    return re.sub(r'[<>:"/\\|?*]', "", title)


def post_to_dropbox(title, content, access_token):
    """
    Uploads content to Dropbox as a text/html file.
    Returns the path of the uploaded file or raises an exception.
    """
    # 1. Create the client
    dbx = dropbox.Dropbox(access_token)

    # 2. Check connection
    try:
        user = dbx.users_get_current_account()
    except AuthError:
        raise Exception("Invalid Access Token")

    # 3. Prepare file
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    sanitized_title = sanitize_filename(title)
    filename = (
        f"{today}_{sanitized_title}.html"  # Saving as HTML to preserve formatting
    )
    upload_path = f"/{filename}"

    # Encode content
    if isinstance(content, str):
        file_content = content.encode("utf-8")
    else:
        file_content = content

    # 4. Upload
    try:
        meta = dbx.files_upload(file_content, upload_path, mode=WriteMode("overwrite"))
        return f"Uploaded to {meta.path_display}"
    except Exception as e:
        raise Exception(f"Upload failed: {str(e)}")


if __name__ == "__main__":
    # Test block
    # Replace with a valid token for testing
    TEST_TOKEN = "YOUR_TOKEN_HERE"
    try:
        res = post_to_dropbox("Test Title", "<h1>Hello Dropbox</h1>", TEST_TOKEN)
        print(res)
    except Exception as e:
        print(f"Error: {e}")

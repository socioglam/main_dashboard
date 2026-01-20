import requests

def post_to_pastebin():
    
    api_key = "xl3ZY6SQeod8JBZQwGcZVtSRig97PdB4"
    
    if not api_key:
        print("Error: PASTEBIN_API_KEY nahi mili!")
        return

    url = "https://pastebin.com/api/api_post.php"
    
    
    
    message = "This may seem like we haven't created anything but it is automatically created and deployed by us."
    target_link = "https://www.flightbycall.com/klm-british-airways-flight-cancellations-klm/"
    
    
    final_content = f"{message}\n\nOfficial Guide Link:\n{target_link}"
    
    data = {
        'api_dev_key': api_key,
        'api_option': 'paste',
        'api_paste_code': final_content,       
        'api_paste_name': 'Complete Official Guide Deployment', 
        'api_paste_expire_date': 'N',          
        'api_paste_format': 'text',            
        'api_paste_private': '0'               
    }
    
    try:
        response = requests.post(url, data=data)
        
        
        if "pastebin.com" in response.text:
            print("🎉 Success! Pastebin Link:")
            print(response.text)
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"Connection Error: {e}")


if __name__ == "__main__":
    post_to_pastebin()
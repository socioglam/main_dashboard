import pytumblr

# Chaaron keys yahan dalein
client = pytumblr.TumblrRestClient(
    'XhU5dnzxqBRlOt2ZXaYve69fP0I6ZHL7N2bi7GIjdv6EFEowkD',
    '1i55CMnE3FCb15xUwEHeIe2yFppP7nW4FDhC2BkFd3ac0I2oGV',
    'VjnX4I6mywbBpe0byntumdFVfld7j27ntCsfpM4mfvRUpI4q5g',
    'owCrVNFXl0r6PKafIynh6pYDMESFjgcu1YQ5cBNOwTj7DFQecn'
)

# Post create karein
response = client.create_text(
    'indexingops',
    state="published",
    title="Hello Tumblr",
    body='Ye humara automatic post hai. <a href="https://www.flightbycall.com/klm-british-airways-flight-cancellations-klm/">Yahan Click Karein</a> guide dekhne ke liye.',
    format="html"  # Ye zaroori hai taaki link clickable bane
)

if 'id' in response:
    post_id = response['id']
    blog_name = 'indexingops' # Wahi same username
    print(f"Success! Post yahan dekho: https://{blog_name}.tumblr.com/post/{post_id}")
else:
    print("Error aaya:", response)
import requests

# Yahan naya wala token paste karein
access_token = "AQUy061_73XfytvV3QAgUGk_tsiq3PMMc-BkstfJngHhjgdHgehNGZzq2a6KEbCIDIEiP3FEYA5sj3YyZfQV-i_qeVMP8tf9l0uwBNPZUQvU_-NGPoOMmb8f1IlURbdPo8Gf064vfXiDeoDGKNcCNGNc28CGH5OfVJShp_3lk9SYrqltaQti__tMQTz5Xe-zgXOLZf4s6x3h6ydvolUh_K6kKaLPOIg2dSQtgbbKyke9rBOZhLfzqsrM4l0Xpi8iBc0H3_-knsu6C4fXBZ9UABnzAH2DY6k5P3VvwIILGZEpQqNfx7FvHS6PQk6HL3uam5TyYMDOlOYutOI-xDBaQPZETzi4fw"

# OpenID Connect endpoint (User details ke liye)
url = "https://api.linkedin.com/v2/userinfo"
headers = {"Authorization": f"Bearer {access_token}"}

response = requests.get(url, headers=headers)
data = response.json()

if "sub" in data:
    print(f"✅ Success! Aapki Person ID (sub) mil gayi: {data['sub']}")
    print(f"Full URN: urn:li:person:{data['sub']}")
else:
    print("❌ Error:", data)
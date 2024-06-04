import requests
import json


url = "http://127.0.0.1:5000/api/downloadTest"

payload = ""
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    }


response = requests.request("GET", url, data=payload, headers=headers)

print(response.content.decode("utf-8"))
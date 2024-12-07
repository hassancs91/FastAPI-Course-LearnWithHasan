import requests
import json

url = "http://127.0.0.1:8000/get-name?name=hasan"

payload = json.dumps({
  "username": "hasan",
  "email": "hasan@gmail.com",
  "age": 18
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

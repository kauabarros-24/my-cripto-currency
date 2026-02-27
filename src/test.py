import requests

url = "http://127.0.0.1:8000"

response = requests.get(f"{url}/")

for c in response:
    print(c)
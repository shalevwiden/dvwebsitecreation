import requests
import certifi

url = "https://www.harvard.edu/"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers, verify=certifi.where())
print(response.status_code)
print(response.text[:500])  # show first 500 chars
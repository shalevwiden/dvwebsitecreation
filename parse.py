# learning parse
apikey='45a23037-5af6-4487-960e-946583594a7e'

import requests

url = "https://api.parse.bot/scraper/cd608c7e-0991-4562-aaad-8cc0f17f055f/fetch_departments_page"
url2="https://api.parse.bot/scraper/cd608c7e-0991-4562-aaad-8cc0f17f055f/extract_departments_and_links"

payload = { "url": "<The full URL of the Stanford departments page to fetch.>" }
headers = {
    "Content-Type": "application/json",
    "X-API-Key": apikey
}

page_html = requests.post(url, json=payload, headers=headers)
response2 = requests.post(url, json=page_html, headers=headers)

print(page_html)
# print(response2.json())
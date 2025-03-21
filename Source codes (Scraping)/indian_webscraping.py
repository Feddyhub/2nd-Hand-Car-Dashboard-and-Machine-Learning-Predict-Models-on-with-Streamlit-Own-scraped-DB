import requests

url = "https://www.akakce.com/?gad_source=1&gclid=EAIaIQobChMI3LDYl_CzigMVoZxQBh2e7wntEAAYASAAEgJLN_D_BwE"

payload = {}
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'cookie': '_gcl_aw=GCL.1734612873.EAIaIQobChMI3LDYl_CzigMVoZxQBh2e7wntEAAYASAAEgJLN_D_BwE; _gcl_gs=2.1.k1$i1734612868$u87650312; _gcl_au=1.1.864366065.1734612873; _ga_SNSZLV7115=GS1.1.1734612873.1.0.1734612873.0.0.0; _ga=GA1.1.1904094491.1734612873; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22K6HvdsVQlGDwP4ZVXy2j%22%2C%22expiryDate%22%3A%222025-12-19T12%3A54%3A35.094Z%22%7D',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
import requests
import sys

sys.stdout.reconfigure(encoding = 'utf-8')

def get_app_id(game_name):
    url = "https://store.steampowered.com/api/storesearch/"

    headers = {
        "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://store.steampowered.com/",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
    }

    params = {
        "term": game_name,
        "l": "english",
        "cc": "IN"
    }

    response = requests.get(url, headers=headers, params=params,timeout=10)
    data = response.json()

    print(data)   # see full response

    if data["total"] > 0:
        return data["items"][0]["id"]
    else:
        return None


print(get_app_id("Remedy"))
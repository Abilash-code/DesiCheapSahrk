import requests

client_id = "5gtq0ml1qcjpy56bh7engi1qiwkmiy"
access_token = "vz61epwja2wwizko955xb8z3epj63u"

url = "https://api.igdb.com/v4/games"

headers = {
    "Client-ID": client_id,
    "Authorization": f"Bearer {access_token}"
}

query = """
search "control : ultimate edition";
fields name,websites.category,websites.url;
"""

response = requests.post(url, headers=headers, data=query)


game = """
search "Fortnite";
fields websites.url;
"""

website_link = requests.post(url,headers=headers,data=game)

websites = website_link.json()

print(websites)

import requests

client_id = "5gtq0ml1qcjpy56bh7engi1qiwkmiy"
client_secret = "5khe9c9ao8jnmcywnlrj50noorm101"

url = "https://id.twitch.tv/oauth2/token"

params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "client_credentials"
}

response = requests.post(url, params=params)
data = response.json()

print(data)

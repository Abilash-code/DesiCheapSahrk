from bs4 import BeautifulSoup
import requests
import sys

sys.stdout.reconfigure(encoding = 'utf-8')

url = "https://store.steampowered.com/app/3241660/EA_SPORTS_FC_26/"

response = requests.get(url)
print(response.status_code)

content = response.text

soup = BeautifulSoup(content,"html.parser")

div = soup.find("div",class_ = "game_purchase_price price")

price = div.text.strip()

price_number = "".join(char for char in price if char.isdigit())

print(price_number)



import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://store.epicgames.com/en-US/p/control"

headers = {
    "User-Agent" : "Mozilla/5.0",
    "Accept" : "application/json,text/javascript,*/*;q=0.01",
    "Accept-Language" : "en-US,en;q=0.9",
    "Connection" : "keep-alive"
}

response = requests.get(url,headers=headers)

content = response.text

soup = BeautifulSoup(content,"html.parser")

price = soup.find_all("span")

print(price)


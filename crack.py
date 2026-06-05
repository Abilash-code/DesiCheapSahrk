import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding = 'utf-8')

headers = {
    "User-Agent" : "Mozilla/5.0 ",
    "Accept" : "application/json,text/javascript,*/*;q=0.01",
    "Referer":"https://www.igdb.com/",
    "Accept-Language" : "en-US,en;q=0.9",
    "Connection" : "keep-alive",
}

IGDB_request = requests.get("https://www.igdb.com/games/control",headers=headers,timeout=10)

print(IGDB_request)
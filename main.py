import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
from playwright_stealth import Stealth
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import playwright
import sys
import json
import os

os.environ["DEBUG"] = "pw:api"

sys.stdout.reconfigure(encoding='utf-8')

unavailable_on_steam = False
unavailable_on_epic = False
free_on_steam = False
free_on_epic = False

steam_price_number = 0
epic_price_number = 0

client_id = "5gtq0ml1qcjpy56bh7engi1qiwkmiy"
access_token = "2qqczfmuk3kdcteer96hp8toxpasq1"

state_data = {
    'cookies': [
        {'name': 'wants_mature_content', 'value': '1', 'domain': 'store.steampowered.com', 'path': '/'},
        {'name': 'birthtime', 'value': '272140201', 'domain': 'store.steampowered.com', 'path': '/'},
        {'name': 'lastagecheckage', 'value': '17-August-1978', 'domain': 'store.steampowered.com', 'path': '/'}
    ],
    'origins': []
}

with open('steam_state.json', 'w') as f:
    json.dump(state_data, f)

url = "https://api.igdb.com/v4/games"

headers = {
    "Client-ID": client_id,
    "Authorization": f"Bearer {access_token}"
}

list_of_game_names  = []

app = FastAPI()

output = {}
steam_url = ""
epic_url = ""
websites = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def GameName(user_request:str) :
    global output
    list_of_game_names.clear()
    query = f"""
    search "{user_request}";
    fields name;
    """
    try :
        response_1 = requests.post(url, headers=headers, data=query)
    except requests.exceptions.ConnectionError as e :
        print("Internet issues")
    output = response_1.json()
    i = 1
    for game in output :
        list_of_game_names.append(game["name"])
        print(f"{i}. {game['name']}")
        i+=1
    if not list_of_game_names :
        print("the game you searched for does not exist in IGDB")
    return output

@app.get("/game")
def GameSelect(game_id:int) :
    global websites
    final_game_id = output[game_id-1]["id"]
    final_query = f"""
         fields name,websites.category,websites.url;
         where id = {final_game_id};
         """
    try :
         response_2 = requests.post(url,headers=headers,data=final_query)
    except requests.exceptions.ConnectionError as e :
         print("Internet issues")
    try :
         final_IDGB_output = response_2.json()
         websites = final_IDGB_output[0]["websites"]
         return websites
    except Exception as e :
         print("The game exists on the database but does not have any marketplace listings")


@app.get("/SteamURL")
def SteamURL() :
    global steam_url
    steam_url = ""
    for site in websites :
        url = site["url"]
        if "store.steampowered.com/app/" in url :
            steam_url = url
    return steam_url,unavailable_on_steam

@app.get("/EpicURL")
def EpicURL() :
    global epic_url
    epic_url = ""
    for site in websites :
        url = site["url"]
        if "https://www.epicgames.com/store/p/" in url or "https://store.epicgames.com/en-US/p/" in url or "https://store.epicgames.com/p/" in url or "https://www.epicgames.com/store/en-US/product/" in url or "https://epicgames.com/p/" in url:
            epic_url = url
    return epic_url,unavailable_on_epic
    

@app.get("/steam") 
def SteamPrice() :
    global steam_url
    global free_on_steam
    global unavailable_on_steam
    global steam_price_number
    steam_price = 0
    try :
        with sync_playwright() as p :
            browser = p.chromium.launch(headless=True,
            proxy={
                "server" : "http://209.127.138.10:5784",
                "username" : "pgliikxt",
                "password" : "mnkraifsf582"
            })
            context = browser.new_context(
                user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
                storage_state="steam_state.json"
            )
            context.set_default_timeout(50000)
            stealth = Stealth()
            stealth.apply_stealth_sync(context)
            page = context.new_page()
            indian_steam_url = f"{steam_url}?cc=in&l=english"
            page.goto(indian_steam_url,wait_until="domcontentloaded")
            try :
                Price = page.locator("div.game_area_purchase_game_wrapper,div.game_area_purchase_game").first
                Price.wait_for(state="visible",timeout=15000)
            except  playwright._impl._errors.TimeoutError as e :
                print(e) 
                print("the game is not available on steam")  
                unavailable_on_steam = True
                return 0,free_on_steam,unavailable_on_steam     
            Price_string = Price.text_content().strip()
            if "Free To Play" in Price_string :
                steam_price_number = 0
                free_on_steam = True
                return steam_price_number,free_on_steam,unavailable_on_steam
            for i  in range(len(Price_string)) :
                letter = Price_string[i]
                if letter == "₹" :
                    steam_price = ""
                    for j in range(i,len(Price_string)) :
                        ezhuthu = Price_string[j]
                        if ezhuthu.isdigit() :
                            steam_price = steam_price + ezhuthu
            steam_price_number = int(steam_price)
            print(steam_price_number)
            return steam_price_number,free_on_steam,unavailable_on_steam
        browser.close()
    except playwright._impl._errors.TimeoutError as e :
        print(e)
        print("browser timeout , you might wanna check your internet connection")
        unavailable_on_steam = True
        return 0,free_on_steam,unavailable_on_steam
    except playwright._impl._errors.Error as e :
        print(e)
        unavailable_on_steam = True
        print("the game is not available on steam ")
        return 0,False,True

@app.get("/epic")
def EpicPrice():
    global epic_url
    global free_on_epic
    global unavailable_on_epic
    global epic_price_number
    epic_price_number = 0
    try :
        with sync_playwright() as p :
            browser = p.chromium.launch(headless=True,
            proxy={
                "server" : "http://209.127.138.10:5784",
                "username" : "pgliikxt",
                "password" : "mnkraifsf582"
            },
            args=["--no-sandbox","--disable-setuid-sandbox","--disable-blink-features=AutomationControlled"])
            context = browser.new_context(
                user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
                ignore_https_errors=True
            )
            stealth = Stealth()
            stealth.apply_stealth_sync(context)
            page = context.new_page()
            if "en-US" in epic_url :
                indian_epic_url = epic_url.replace("en-US","en-IN")
            else :
                indian_epic_url = epic_url.replace("store.epicgames.com/","store.epicgames.com/en-IN/")
            page.goto(indian_epic_url)
            page.locator('strong:has-text("₹"), strong:has-text("Free")').wait_for(state="visible", timeout=10000)
            page.wait_for_timeout(3000)
            strong = page.locator("strong").all()
            epic_price = ""
            i = 0
            for _ in strong :
                e_price = strong[i].text_content().strip()
                if "Free" in e_price :
                    free_on_epic = True
                    return epic_price_number,free_on_epic,unavailable_on_epic
                if "₹" in e_price : 
                    epic_price = e_price
                i+=1
                try:
                    if not epic_price :
                        epic_price_number = 0
                        if i == len(strong) :
                            unavailable_on_epic = True
                            return 0,free_on_epic,True
                        continue
                    epic_price_number = int("".join(char for char in epic_price if char.isdigit()))
                    if "." in epic_price :
                        epic_price_number_2 = str(epic_price_number)
                        deciding_digit = int(epic_price_number_2[len(epic_price_number_2)-2])
                        if deciding_digit >= 5 :
                            epic_price_number = (epic_price_number//100)+1
                        else :
                            epic_price_number = (epic_price_number//100)
                    print(epic_price_number)
                    return epic_price_number,free_on_epic,unavailable_on_epic
                except ValueError :
                    unavailable_on_epic = True
                return epic_price_number,free_on_epic,unavailable_on_epic
            browser.close()
    except playwright._impl._errors.TimeoutError as e :
        print("browser timeout , you might wanna check your internet connection,heyyyy")
        unavailable_on_epic = True
        return 0,False,True
    except playwright._impl._errors.Error as e :
        print(e)
        print("the game is not available on epic ")
        # --- NEW DEBUG TRAP ---
        debug_list = []
        try:
            # Grab every strong tag on the page exactly as it exists at the moment of failure
            all_strongs = page.locator("strong").all()
            for element in all_strongs:
                text = element.text_content().strip()
                if text:
                    debug_list.append(text)
        except Exception as debug_error:
            debug_list.append(f"Failed to read DOM: {debug_error}")
        # ----------------------
        unavailable_on_epic = True
        browser.close()
        return debug_list,False,True
    
@app.get("/finalResult")
def finalResult() : 
    if unavailable_on_steam and unavailable_on_epic :
        return "The game you requested is unavailable in both market places"
    elif unavailable_on_steam :
        return "the game you requested is unavailable on steam"
    elif unavailable_on_epic :
        return "The game you requested is unavailable on epic"
    else : 
        if free_on_steam and free_on_epic :
            return "The game is free on both marketplaces"
        elif free_on_steam :
            return "The game is free on steam so buy there"
        elif free_on_epic :
            return "the game is free on epic so buy there"
        else :
            if steam_price_number > epic_price_number :
                return "buy on epic"
            elif steam_price_number == epic_price_number :
                return "buy on either"
            else :
                return "buy on steam"


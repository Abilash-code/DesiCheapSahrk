import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
from playwright_stealth import Stealth
import playwright
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

unavailable_on_steam = False
unavailable_on_epic = False
free_on_steam = False
free_on_epic = False

client_id = "5gtq0ml1qcjpy56bh7engi1qiwkmiy"
access_token = "vz61epwja2wwizko955xb8z3epj63u"

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

def GameName(url,headers) :
    game_name = input("Enter game name : ")
    query = f"""
    search "{game_name}";
    fields name;
    """
    try :
        response_1 = requests.post(url, headers=headers, data=query)
    except requests.exceptions.ConnectionError as e :
        sys.exit()
        print("Internet issues")
    output = response_1.json()
    i = 1
    for game in output :
        list_of_game_names.append(game["name"])
        print(f"{i}. {game["name"]}")
        i+=1
    if not list_of_game_names :
        print("the game you searched for does not exist in IGDB")
        sys.exit()
    return output

output = GameName(url,headers)

def GameSelect(output) :
    game_id = int(input(" From the list of games displayed on the terminal \n select the serial No of the game you want the details of : "))-1
    if game_id < 0 or game_id > (len(list_of_game_names)-1) :
        print("please only enter numbers within the list of games")
        sys.exit() 
    final_game_id = output[game_id]["id"]
    final_query = f"""
        fields name,websites.category,websites.url;
        where id = {final_game_id};
        """
    try :
        response_2 = requests.post(url,headers=headers,data=final_query)
    except requests.exceptions.ConnectionError as e :
        print("Internet issues")
        sys.exit()
    try :
        final_IDGB_output = response_2.json()
        websites = final_IDGB_output[0]["websites"]
        return websites
    except Exception as e :
        print("The game exists on the database but does not have any marketplace listings")
        sys.exit()

websites = GameSelect(output)

def SteamURL(websites,unavailable_on_steam) :
    steam_url = ""
    for site in websites :
        url = site["url"]
        if "store.steampowered.com/app/" in url :
            steam_url = url
    return steam_url,unavailable_on_steam

def EpicURL(websites,unavailable_on_epic) :
    epic_url = ""
    for site in websites :
        url = site["url"]
        if "https://www.epicgames.com/store/p/" in url or "https://store.epicgames.com/en-US/p/" in url or "https://store.epicgames.com/p/" in url or "https://www.epicgames.com/store/en-US/product/" in url:
            epic_url = url
    return epic_url,unavailable_on_epic

steam_url,unavailable_on_steam = SteamURL(websites,unavailable_on_steam)    

    
def SteamPrice(steam_url,free_on_steam,unavailable_on_steam) :
    steam_price = 0
    try :
        with sync_playwright() as p :
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
                storage_state="steam_state.json"
            )
            context.set_default_timeout(50000)
            stealth = Stealth()
            stealth.apply_stealth_sync(context)
            page = context.new_page()
            page.goto(steam_url,wait_until="domcontentloaded")
            try :
                Price = page.locator("div.game_area_purchase_game_wrapper,div.game_area_purchase_game").first
                Price.wait_for(state="visible",timeout=6000)
            except  playwright._impl._errors.TimeoutError as e :
                print(e) 
                print("the game is not availaabale on steam")  
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
        print("the game is not available on steam ")
        sys.exit()

epic_url,unavailable_on_epic = EpicURL(websites,unavailable_on_epic)

def EpicPrice(epic_url,free_on_epic,unavailable_on_epic):
    epic_price_number = 0
    try :
        with sync_playwright() as p :
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
            )
            stealth = Stealth()
            stealth.apply_stealth_sync(context)
            page = context.new_page()
            page.goto(epic_url)
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
    except playwright._impl._errors.Error as e :
        print(e)
        print("the game is not available on epic ")
        sys.exit()

steam_price_number,free_on_steam,unavailable_on_steam = SteamPrice(steam_url,free_on_steam,unavailable_on_steam)

epic_price_number,free_on_epic,unavailable_on_epic = EpicPrice(epic_url,free_on_epic,unavailable_on_epic)
if unavailable_on_steam and unavailable_on_epic :
    print("The game you requested is unavailable in both market places")
elif unavailable_on_steam :
    print("the game you requested is unavailable on steam")
elif unavailable_on_epic :
    print("The game you requested is unavaialble on epic")
else : 
    if free_on_steam and free_on_epic :
        print("The game is free on both marketplaces")
    elif free_on_steam :
        print("The game is free on steam so buy there")
    elif free_on_epic :
        print("the game is free on epic so buy there")
    else :
        if steam_price_number > epic_price_number :
            print("buy on epic")
        elif steam_price_number == epic_price_number :
            print("buy on either")
        else :
            print("buy on steam")

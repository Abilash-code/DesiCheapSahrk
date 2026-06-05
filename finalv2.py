import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import playwright
import sys
from types import NoneType

sys.stdout.reconfigure(encoding='utf-8')

unavailable_on_steam = False
unavailable_on_epic = False
free_on_steam = False
free_on_epic = False

client_id = "5gtq0ml1qcjpy56bh7engi1qiwkmiy"
access_token = "vz61epwja2wwizko955xb8z3epj63u"

url = "https://api.igdb.com/v4/games"

headers = {
    "Client-ID": client_id,
    "Authorization": f"Bearer {access_token}"
}

try :
    game_name = input("Enter game name : ")
    query = f"""
    search "{game_name}";
    fields name;
    """


    response_1 = requests.post(url, headers=headers, data=query)

    output = response_1.json()

    list_of_game_names  = []


    i = 1

    for game in output :
        list_of_game_names.append(game["name"])
        print(f"{i}. {game["name"]}")
        i+=1

    if not list_of_game_names :
        print("the game you searched for does notnexist in IGDB")
        sys.exit()

    game_id = int(input(" From the list of games displayed on the terminal \n select the serial No of the game you want the details of : "))-1
    if game_id < 0 or game_id > (len(list_of_game_names)-1) :
        sys.exit() 

    final_game_id = output[game_id]["id"]


    final_query = f"""
        fields name,websites.category,websites.url;
        where id = {final_game_id};
        """

    response_2 = requests.post(url,headers=headers,data=final_query)

    final_IDGB_output = response_2.json()

    websites = final_IDGB_output[0]["websites"]

    steam_url = ""
    for site in websites :
        url = site["url"]
        if "store.steampowered.com/app/" in url :
            steam_url = url

    epic_url = ""
    for site in websites :
        url = site["url"]
        if "https://www.epicgames.com/store/p/" in url or "https://store.epicgames.com/en-US/p/" in url or "https://store.epicgames.com/p/" in url or "https://www.epicgames.com/store/en-US/product/" in url:
            epic_url = url

    try : 
        steam_response = requests.get(steam_url)
        steam_content = steam_response.text
        steam_soup = BeautifulSoup(steam_content,"html.parser")
        steam_discount_div = steam_soup.find("div",class_=lambda c : c and c.split() == "discount_final_price")
        if steam_discount_div is not None :
            steam_price = steam_discount_div.text.strip()
            if steam_price == "Free To Play" :
                free_on_steam = True
            else :
                steam_price_number = int("".join(char for char in steam_price if char.isdigit()))
                print(steam_price_number)
        else : 
            steam_div = steam_soup.find("div",class_ = "game_purchase_price price")
            if isinstance(steam_div,NoneType) :
                unavailable_on_steam = True 
            else :
                steam_price = steam_div.text.strip()
                if steam_price == "Free To Play" :
                    free_on_steam = True
                else :
                    steam_price_number = int("".join(char for char in steam_price if char.isdigit()))
                    print(steam_price_number)

    except requests.exceptions.MissingSchema as e :
        print("The game is not availabe on steam")
        unavailable_on_steam = True

    epic_price_number = 0

    if epic_url == "" :
        unavailable_on_epic = True
    else : 
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
                if not free_on_epic :
                    for price in strong :
                        e_price = strong[i].text_content().strip()
                        if "₹" in e_price : 
                            epic_price = e_price
                            break
                        i+=1
                    try:
                        epic_price_number = int("".join(char for char in epic_price if char.isdigit()))
                        print(epic_price_number)
                    except ValueError :
                        unavailable_on_epic = True
                browser.close()
        except playwright._impl._errors.TimeoutError as e :
            print("browser timeout , you might wanna check your internet connection")



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
except requests.exceptions.ConnectionError as e :
    print("Internet issues")
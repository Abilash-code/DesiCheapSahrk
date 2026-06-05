from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import sys

sys.stdout.reconfigure(encoding='utf-8')
with sync_playwright() as p :
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    )
    stealth = Stealth()
    stealth.apply_stealth_sync(context)
    page = context.new_page()
    url = "https://store.epicgames.com/en-US/p/grand-theft-auto-v"
    page.goto(url)
    strong = page.locator("strong").all()
    print(strong[0].text_content())
    browser.close()
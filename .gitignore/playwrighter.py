from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Launch browser so you can see it
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    print("Go to the site and MANUALLY pass the age verification now...")
    page.goto("https://store.steampowered.com/app/870780/Control_Ultimate_Edition/")
    
    # Wait for you to click the 'I am 18' button manually
    page.wait_for_timeout(10000) # Gives you 10 seconds to click it
    
    # Now, let's see what the site actually saved
    storage_state = context.storage_state()
    print(storage_state)
    
    browser.close()
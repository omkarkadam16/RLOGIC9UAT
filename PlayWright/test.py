from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://win-8tcj8ivog5i:7265/")
    print(page.title())
    browser.close()
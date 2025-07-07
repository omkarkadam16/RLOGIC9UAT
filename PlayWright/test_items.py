from playwright.sync_api import sync_playwright # 👈 import sync_playwright

def test_playwright(): # 👈 define the test
    with sync_playwright() as p:  # 👈 creates a Playwright object
        browser = p.chromium.launch(headless=False) # 👈 launch the browser in headless mode
        context = browser.new_context(ignore_https_errors=True)  # 👈 ignore SSL cert errors here
        page = context.new_page() # 👈 create a new page

        page.goto("url") # 👈 navigate to the page
        print(page.title()) # 👈 print the page title

        #Login Page
        page.fill('id="EmailId', "demo123@gmail.com")
        print("Email Enter Successfully")
        page.locator('input[id="Password"]').fill("Demo@123")
        print("Text entered")
        page.locator('button#loginButton').click()
        print("Clicked on Login Page")

        #Masters
        page.locator("text = Master").click()
        print("Clicked on Master")
        page.locator("text = Item Or Product").click()
        print("Clicked on  Item Or Product ")

        #Add items
        page.locator('#btnAddProduct').click()
        print("Clicked on Add item")
        page.locator("#txtItemName").fill("Chemicals")
        print("Text entered")
        page.locator("#btnSaveProduct").click()
        print("Clicked on Save")

        #Closed
        browser.close()
        print("Browser closed")



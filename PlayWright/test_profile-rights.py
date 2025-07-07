from playwright.sync_api import sync_playwright

def select_dropdown(page, container_selector: str, option_text: str):
    page.locator(container_selector).click()
    page.locator(".select2-search__field").fill(option_text)
    page.locator(".select2-results__option", has_text=option_text).click()
    print(f"Selected '{option_text}' from dropdown")

def test_profile_rights():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        page.goto("https://win-8tcj8ivog5i:7265/")  # 👈 navigate to the page
        print(page.title())  # 👈 print the page title

        # Login Page
        page.fill("#EmailId", "demo123@gmail.com")
        print("Email Enter Successfully")
        page.locator('input[id="Password"]').fill("Demo@123")
        print("Text entered")
        page.locator('button#loginButton').click()
        print("Clicked on Login Page")

        # Masters
        page.locator("text = Master").click()
        print("Clicked on Master")
        page.locator("text = Profile Rights").click()
        print("Clicked on  Profile Rights ")

        # Use custom dropdown function
        select_dropdown(page, "#select2-txtName-container", "Admin")
        select_dropdown(page, "#select2-txtMenu-container", "Master")

        #Check Box
        page.locator("#view1").uncheck()
        print("Checkbox checked")

        page.locator("#btnSaveForm").click()
        print("Clicked on Save")
        page.wait_for_timeout(2000) # ✅ Waits for 2 seconds (2000 milliseconds)

        browser.close()



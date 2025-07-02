
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-web-security')
        options.add_argument('--start-maximized')
        options.add_argument('--incognito')

        # Disable password manager & credential services
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2,
        }
        options.add_experimental_option("prefs", prefs)

        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver,15)

    def click_element(self,by,value,retry = 3):
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by,value))).click()
                print("Clicked on",value)
                return True
            except(ex.StaleElementReferenceException,ex.ElementClickInterceptedException,ex.ElementNotInteractableException):
                print(f"Attempt{i+1}/{retry}")
        try:
            a = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();",a)
            print("Clicked using JS")
            return True
        except ex.JavascriptException:
            return False


    def send_keys(self,by,value,text):
        try:
            i = self.wait.until(EC.visibility_of_element_located((by,value)))
            i.clear()
            i.send_keys(text)
            print("Enter text:",text)
            return True
        except (ex.ElementClickInterceptedException,ex.StaleElementReferenceException,ex.InvalidElementStateException):
            return False

    def switch_frames(self,element_id):
        driver = self.driver
        driver.switch_to.default_content()
        iframes = driver.find_elements(By.TAG_NAME,"iframe")
        for i in iframes:
            driver.switch_to.frame(i)
            try:
                if driver.find_element(By.ID,element_id):
                    return True
            except ex.TimeoutException:
                driver.switch_to.default_content()
        return False

    def select_dropdown(self,by,value,text):
        try:
            self.click_element(by,value)

            i = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"select2-search__field")))
            i.clear()
            i.send_keys(text)
            print("Enter Text",text)

            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,"select2-selection__rendered")))

            options = self.driver.find_elements(By.CLASS_NAME,"select2-selection__rendered")
            for option in options:
                if text.lower() in option.text.strip().lower():
                    option.click()
                    print("Selected autocomplete option:", option.text.strip())
                    return True

            # Fallback: select first with keyboard
            i.send_keys(Keys.DOWN)
            i.send_keys(Keys.ENTER)
            print("Fallback: selected autocomplete option with keyboard")
            return True

        except ex.StaleElementReferenceException:
            print(f"[ERROR] Autocomplete selection failed for '{text}':", ex)
            return False


    def test_user(self):
        driver = self.driver
        driver.get("https://win-8tcj8ivog5i:7265/")

        print("Logging in...")
        self.send_keys(By.ID, "EmailId", "demo123@gmail.com")
        self.send_keys(By.ID, "Password", "Demo@123")
        self.click_element(By.ID, "loginButton")
        print("Login successful.")

        time.sleep(2)
        self.click_element(By.LINK_TEXT, "Company")
        self.click_element(By.LINK_TEXT,"User")

        self.switch_frames("btnAddUser")
        self.click_element(By.ID,"btnAddUser")
        self.switch_frames("userbodyform")
        time.sleep(2)
        self.click_element(By.ID,"txtName")
        self.send_keys(By.ID,"txtName","Omkar Kadam")
        self.send_keys(By.ID, "txtLoginName", "Omkar1610")
        self.click_element(By.ID, "txtPassword")
        self.send_keys(By.ID,"txtPassword","Demo@123")
        self.send_keys(By.ID, "txtEmailid", "Demo@gmail.com")
        self.select_dropdown(By.ID, "select2-ddlCompanyAndFranchise-container", "Ducati")
        self.select_dropdown(By.ID, "select2-ddlLocation-container", "Mumbai")
        self.send_keys(By.ID,"txtMobileNo","9284326684")

        self.click_element(By.ID,"btnSaveForm")
        time.sleep(1)


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()








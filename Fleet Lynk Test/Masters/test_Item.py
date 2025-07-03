
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager

class TestCompany(unittest.TestCase):
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

        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver,15)

    def click_element(self, by, value, retry=3):
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by, value))).click()
                print("Clicked On :", value)
                return True
            except(
                    ex.ElementClickInterceptedException,
                    ex.StaleElementReferenceException,
                    ex.TimeoutException,
            ):
                print(f"Attempt{i + 1}/{retry}")

        try:
            a = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", a)
            return True
        except ex.JavascriptException:
            return False

    def switch_frames(self,value):
        driver = self.driver
        driver.switch_to.default_content()
        iframes = driver.find_elements(By.TAG_NAME,"iframe")
        for i in iframes:
            driver.switch_to.frame(i)
            try:
                if driver.find_element(By.ID,value):
                    return True
            except ex.TimeoutException:
                driver.switch_to.default_content()
        return False

    def send_keys(self, by, value, text):
        try:
            self.click_element(by, value)
            element = self.wait.until(EC.visibility_of_element_located((by, value)))
            element.is_enabled()
            element.clear()
            element.send_keys(text)
            print("Sent keys", text)
            return True
        except ex.NoSuchElementException:
            print(f"Element not found: {value}")
            return False


    def test_items(self):
        driver = self.driver
        driver.get("https://win-8tcj8ivog5i:7265/")

        print("Logging in...")
        self.send_keys(By.ID, "EmailId", "demo123@gmail.com")
        self.send_keys(By.ID, "Password", "Demo@123")
        self.click_element(By.ID, "loginButton")
        print("Login successful.")

        time.sleep(2)
        self.click_element(By.LINK_TEXT, "Master")
        self.click_element(By.LINK_TEXT, "Item Or Product")

        self.switch_frames("btnAddProduct")
        self.click_element(By.ID, "btnAddProduct")
        time.sleep(2)

        self.send_keys(By.ID,"txtItemName","Chemicals")

        self.click_element(By.ID,"btnSaveProduct")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()




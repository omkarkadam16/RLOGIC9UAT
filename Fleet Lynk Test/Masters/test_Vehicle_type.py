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

class VehicleType(unittest.TestCase):
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
        cls.wait = WebDriverWait(cls.driver, 15)

    def click_element(self,by,value,retry = 2):
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by,value))).click()
                return True
            except(ex.ElementClickInterceptedException,ex.StaleElementReferenceException,ex.TimeoutException):
                print(f"Attempt{i+1}/{retry}")
                time.sleep(1)
        try:
            a = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();",a)
            return True
        except ex.JavascriptException:
            return False

    def send_keys(self,by,value,text):
        try:
            i = self.wait.until(EC.element_to_be_clickable((by,value)))
            i.clear()
            i.send_keys(text)
            return True
        except(ex.ElementClickInterceptedException,ex.StaleElementReferenceException,ex.TimeoutException):
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

    def select_dropdown(self, by, value, text):
        try:
            # Click the dropdown to activate the input (if necessary)
            self.click_element(by, value)
            # Send input text (Search field Class Name)
            input_box = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-search__field")))
            input_box.clear()
            input_box.send_keys(text)
            print(f"Typed '{text}' in autocomplete input")
            # Wait for the results to appear (List Class name)
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "select2-selection__rendered"))
            )
            # Get all matching options
            options = self.driver.find_elements(By.CLASS_NAME, "select2-selection__rendered")
            for option in options:
                if text.lower() in option.text.strip().lower():
                    option.click()
                    print("Selected autocomplete option:", option.text.strip())
                    return True
            # Fallback: select first with keyboard
            input_box.send_keys(Keys.DOWN)
            input_box.send_keys(Keys.ENTER)
            print("Fallback: selected autocomplete option with keyboard")
            return True

        except Exception as e:
            print(f"[ERROR] Autocomplete selection failed for '{text}':", e)
            return False

    def test_vehicle_type(self):
        driver = self.driver
        driver.get("https://win-8tcj8ivog5i:7265/")

        print("Logging in...")
        self.send_keys(By.ID, "EmailId", "demo123@gmail.com")
        self.send_keys(By.ID, "Password", "Demo@123")
        self.click_element(By.ID, "loginButton")
        print("Login successful.")

        self.click_element(By.LINK_TEXT, "Master")
        self.click_element(By.LINK_TEXT, "Vehicle Type")

        self.switch_frames("btnAddVehicleType")
        self.click_element(By.ID, "btnAddVehicleType")
        self.switch_frames("txtVehicleType")
        time.sleep(2)
        self.send_keys(By.ID,"txtVehicleType","Sedan")
        self.send_keys(By.ID,"txtminKmsPerDay","200")

        self.click_element(By.ID,"btnSaveVehicleType")
        time.sleep(1)
        print("Vehicle type added successfully")

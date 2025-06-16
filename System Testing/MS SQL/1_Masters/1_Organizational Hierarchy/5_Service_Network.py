from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager


class ServiceNetwork(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

    def click_element(self, by, value, retry=2):
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by, value))).click()
                print("Clicked on element", value)
                return True
            except (
                ex.ElementClickInterceptedException,
                ex.StaleElementReferenceException,
                ex.TimeoutException,
            ):
                print(
                    f"Retrying click on {by} with value {value}, attempt {i+1}/{retry}"
                )
                time.sleep(1)
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
            print("Clicked on element using JavaScript")
            return True
        except:
            return False

    def switch_frames(self, element_id):
        driver = self.driver
        driver.switch_to.default_content()
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            driver.switch_to.frame(iframe)
            try:
                if driver.find_element(By.ID, element_id):
                    return True
            except ex.NoSuchElementException:
                driver.switch_to.default_content()
        return False

    def send_keys(self, by, value, text):
        try:
            element = self.wait.until(EC.visibility_of_element_located((by, value)))
            element.is_enabled()
            element.clear()
            element.send_keys(text)
            print("Sent keys", text)
            return True
        except ex.NoSuchElementException:
            print(f"Element not found: {value}")
            return False

    def select_dropdown(self, by, value, text):
        try:
            e = self.wait.until(EC.element_to_be_clickable((by, value)))
            e.is_enabled()
            e.click()
            self.wait.until(EC.visibility_of_element_located((by, value)))
            element = Select(self.driver.find_element(by, value))
            element.select_by_visible_text(text)
            return True
        except (
            ex.NoSuchElementException,
            ex.ElementClickInterceptedException,
            ex.TimeoutException,
        ):
            return False

    def autocomplete_select(self, by, value, text):
        input_text = self.wait.until(EC.visibility_of_element_located((by, value)))
        input_text.clear()
        input_text.send_keys(text)
        time.sleep(1)
        suggest = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-menu-item"))
        )
        for i in suggest:
            if text.upper() in i.text.upper():
                i.click()
                time.sleep(1)
                print("Selected autocomplete option:", text)
                return
        input_text.send_keys(Keys.DOWN)
        input_text.send_keys(Keys.ENTER)
        print("Selected autocomplete option using keyboard:", text)

    def test_ServiceNetwork(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        for i in (
            "Common",
            "Organisational Hierarchy »",
            "Service Network",
        ):
            self.click_element(By.LINK_TEXT, i)
            print(f"Navigated to {i}.")

            # List of multiple locations
            locations = [
                {
                    "Code": "MUM",
                    "ServiceNetwork": "MUMBAI",
                    "ServiceNetworkType": "Service Area",
                    "CityId": "MUMBAI",
                    "PinCode": "411001",
                    "DefaultLocationId": "MUMBAI",
                },
                {
                    "Code": "BWD",
                    "ServiceNetwork": "BHIWANDI",
                    "ServiceNetworkType": "Service Area",
                    "CityId": "THANE",
                    "PinCode": "411001",
                    "DefaultLocationId": "BHIWANDI",
                },
                {
                    "Code": "PUN",
                    "ServiceNetwork": "PUNE",
                    "ServiceNetworkType": "Service Area",
                    "CityId": "PUNE",
                    "PinCode": "411001",
                    "DefaultLocationId": "PUNE",
                },
                {
                    "Code": "JPR",
                    "ServiceNetwork": "JAIPUR",
                    "ServiceNetworkType": "Service Area",
                    "CityId": "JAIPUR",
                    "PinCode": "411001",
                    "DefaultLocationId": "JAIPUR",
                },
                {
                    "Code": "AHM",
                    "ServiceNetwork": "AHMEDABAD",
                    "ServiceNetworkType": "Service Area",
                    "CityId": "AHMEDABAD",
                    "PinCode": "411001",
                    "DefaultLocationId": "AHMEDABAD",
                },
                {
                    "Code": "HYD",
                    "ServiceNetwork": "HYDERABAD",
                    "ServiceNetworkType": "Service Area",
                    "CityId": "HYDERABAD",
                    "PinCode": "411001",
                    "DefaultLocationId": "HYDERABAD",
                },
                {
                    "Code": "NAM",
                    "ServiceNetwork": "NAMPALLI",
                    "ServiceNetworkType": "Service Area",
                    "CityId": "HYDERABAD",
                    "PinCode": "411001",
                    "DefaultLocationId": "NAMPALLI",
                },
                {
                    "Code": "SED",
                    "ServiceNetwork": "SECUNDERABAD",
                    "ServiceNetworkType": "Service Area",
                    "CityId": "HYDERABAD",
                    "PinCode": "411001",
                    "DefaultLocationId": "SECUNDERABAD",
                },
                {
                    "Code": "DEL",
                    "ServiceNetwork": "DELHI",
                    "ServiceNetworkType": "Service Area",
                    "CityId": "DELHI",
                    "PinCode": "411001",
                    "DefaultLocationId": "DELHI",
                },
            ]

            # Iterate over each location and create it
            for location in locations:
                if self.switch_frames("btn_NewRecord"):
                    self.click_element(By.ID, "btn_NewRecord")

                # Fill out the form
                if self.switch_frames("Code"):
                    self.send_keys(By.ID, "Code", location["Code"])
                    self.send_keys(
                        By.ID, "ServiceNetworkName", location["ServiceNetwork"]
                    )
                    self.select_dropdown(
                        By.ID, "ServiceNetworkTypeId", location["ServiceNetworkType"]
                    )
                    self.autocomplete_select(By.ID, "CityId-select", location["CityId"])
                    self.send_keys(By.ID, "PinCode", location["PinCode"])
                    self.autocomplete_select(
                        By.ID, "DefaultLocationId-select", location["DefaultLocationId"]
                    )
                    print(f"Details entered for {location['ServiceNetwork']}")

                    # Submit the form
                    if self.switch_frames("mysubmit"):
                        self.click_element(By.ID, "mysubmit")
                        print(
                            f"ServiceNetwork {location['ServiceNetwork']} created successfully."
                        )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

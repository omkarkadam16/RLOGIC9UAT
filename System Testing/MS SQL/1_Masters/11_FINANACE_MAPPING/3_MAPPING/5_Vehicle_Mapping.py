import unittest
import time
import selenium.common.exceptions as ex
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class VehicleMapping(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

    def click_element(self, by, value, retry=2):
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by, value))).click()
                return True
            except (
                ex.ElementClickInterceptedException,
                ex.StaleElementReferenceException,
                ex.TimeoutException,
            ):
                time.sleep(1)
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
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
        """Send keys after checking visibility"""
        for attempt in range(3):
            try:
                print(f"[INFO] Attempt {attempt + 1}: Entering text...")
                element = self.wait.until(EC.visibility_of_element_located((by, value)))
                element.is_enabled()
                element.clear()
                element.send_keys(text)
                print("Sent keys", text)
                return True
            except (
                ex.NoSuchElementException,
                ex.UnexpectedAlertPresentException,
                ex.TimeoutException,
                ex.StaleElementReferenceException,
            ) as e:
                print(f"[WARNING]Error : {type(e)} occurred. Retrying...")
                time.sleep(1)
        return False

    def select_dropdown(self, by, value, text):
        try:
            e = self.wait.until(EC.element_to_be_clickable((by, value)))
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
                return
        input_text.send_keys(Keys.DOWN)
        input_text.send_keys(Keys.ENTER)

    def test_Vehicle_Mapping(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        menus = ["Finance", "Mapping »", "Vehicle Mapping"]
        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)

        series = [
            {"LedgerName": "MH12XB2005", "LedgerAlias": "MH12XB2005"},
            {"LedgerName": "MH04AA7007", "LedgerAlias": "MH04AA7007"},
            {"LedgerName": "MH04AA0099", "LedgerAlias": "MH04AA0099"},
            {"LedgerName": "MH04TT9008", "LedgerAlias": "MH04TT9008"},
            {"LedgerName": "MH06RR1006", "LedgerAlias": "MH06RR1006"},
        ]

        for i in series:

            # General Information
            if self.switch_frames("MappingType"):
                self.select_dropdown(By.ID, "MappingType", "General Mapping")
                self.send_keys(By.ID, "txt_search", i["LedgerName"])
                self.click_element(By.ID, "btn_Seach")
                self.click_element(By.ID, "LedgerMappingGridSession777-1")
                self.autocomplete_select(
                    By.ID, "SubLedgerLedgerMappingSession-select", i["LedgerAlias"]
                )
                # Save after each selection
                self.click_element(By.ID, "btnSave-LedgerMappingGridSession777")
                time.sleep(2)
                self.click_element(By.ID, "LedgerMappingGridSession777-1")
                time.sleep(2)
                self.click_element(By.ID, "btnSave-LedgerMappingGridSession777")

                # Switch back to default content after submission
                driver.switch_to.default_content()
                time.sleep(2)

                menus = ["Finance", "Mapping »", "Vehicle Mapping"]
                for link_test in menus:
                    self.click_element(By.LINK_TEXT, link_test)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

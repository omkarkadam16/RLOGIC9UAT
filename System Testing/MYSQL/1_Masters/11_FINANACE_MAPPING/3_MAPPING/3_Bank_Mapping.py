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


class BankMapping(unittest.TestCase):
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
        try:
            element = self.wait.until(EC.visibility_of_element_located((by, value)))
            element.clear()
            element.send_keys(text)
            return True
        except ex.NoSuchElementException:
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

    def autocomplete_select(self, by, value, text, retries=3):
        for attempt in range(retries):
            try:
                # Wait for input field to appear
                input_text = self.wait.until(EC.element_to_be_clickable((by, value)))
                input_text.clear()
                input_text.send_keys(text)

                # Wait for suggestions to load
                self.wait.until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-menu-item"))
                )
                time.sleep(0.5)  # slight pause for dropdown animation

                suggestions = self.driver.find_elements(By.CLASS_NAME, "ui-menu-item")

                for item in suggestions:
                    try:
                        if text.upper() in item.text.upper():
                            item.click()
                            return
                    except ex.StaleElementReferenceException:
                        continue  # if a suggestion becomes stale, skip to next

                # If no match, try navigating with keyboard
                input_text.send_keys(Keys.DOWN)
                input_text.send_keys(Keys.ENTER)
                return

            except (ex.StaleElementReferenceException, ex.TimeoutException):
                print(f"Attempt {attempt + 1} failed due to stale element. Retrying...")
                time.sleep(1)
                continue

        raise Exception(
            f"Failed to select '{text}' from autocomplete after {retries} attempts."
        )

    def test_Bank_Mapping(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript?ccode=UATASCRIPT")

        self.send_keys(By.ID, "Login", "admin")
        self.send_keys(By.ID, "Password", "Omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        menus = ["Finance", "Ledger Mapping »", "Bank Mapping"]
        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)

        series = [
            {"Name": "SBI Bank", "SubLedger": "SBI Bank"},
            {"Name": "HDFC Bank", "SubLedger": "HDFC Bank"},
        ]

        for i in series:

            # General Information
            if self.switch_frames("MappingType"):
                self.select_dropdown(By.ID, "MappingType", "General Mapping")
                self.send_keys(By.ID, "txt_search", i["Name"])
                self.click_element(By.ID, "btn_Seach")
                self.click_element(By.ID, "LedgerMappingGridSession351-1")
                self.autocomplete_select(
                    By.ID, "LedgerLedgerMappingSession-select", i["SubLedger"]
                )
                # Save after each selection
                self.click_element(By.ID, "btnSave-LedgerMappingGridSession351")
                time.sleep(2)

                # Switch back to default content after submission
                driver.switch_to.default_content()
                time.sleep(2)

                menus = ["Finance", "Ledger Mapping »", "Bank Mapping"]
                for link_test in menus:
                    self.click_element(By.LINK_TEXT, link_test)

        print("All data created successfully.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

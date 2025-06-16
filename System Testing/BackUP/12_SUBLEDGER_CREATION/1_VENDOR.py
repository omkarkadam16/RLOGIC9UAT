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


class SubLedgerMaster(unittest.TestCase):
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

    def test_customer(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript?ccode=UATASCRIPT")

        self.send_keys(By.ID, "Login", "admin")
        self.send_keys(By.ID, "Password", "Omsgn9")
        self.click_element(By.ID, "btnLogin")

        menus = [
            "Finance",
            "Finance Master »",
            "Account Master »",
            "Account Sub Ledger",
        ]
        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)

        series = [
            {
                "LedgerName": "BHORUKA LOGISTICS PVT LTD",
                "LedgerAlias": "BHORUKA LOGISTICS PVT LTD",
            },
            {
                "LedgerName": "BAJAJ CORPORATION PVT LTD",
                "LedgerAlias": "BAJAJ CORPORATION PVT LTD",
            },
            {
                "LedgerName": "INTER INDIA ROADWAYS LTD",
                "LedgerAlias": "INTER INDIA ROADWAYS LTD",
            },
            {"LedgerName": "VIJAY ENTERPRISES", "LedgerAlias": "VIJAY ENTERPRISES"},
            {
                "LedgerName": "SHAKTI FREIGHT CARRIERS",
                "LedgerAlias": "SHAKTI FREIGHT CARRIERS",
            },
            {
                "LedgerName": "AKIL KHAN SO HABIB KHAN",
                "LedgerAlias": "AKIL KHAN SO HABIB KHAN",
            },
            {"LedgerName": "BHAGAT SINGH", "LedgerAlias": "BHAGAT SINGH"},
            {"LedgerName": "DARSHAN SINGH", "LedgerAlias": "DARSHAN SINGH"},
            {"LedgerName": "IOCL FUEL PUMP", "LedgerAlias": "IOCL FUEL PUMP"},
        ]

        for i in series:
            if self.switch_frames("btn_NewRecord"):
                self.click_element(By.ID, "btn_NewRecord")
                time.sleep(2)

            # General Information
            if self.switch_frames("LedgerName"):
                self.send_keys(By.ID, "LedgerName", i["LedgerName"])
                self.send_keys(By.ID, "LedgerAlias", i["LedgerAlias"])
                self.select_dropdown(
                    By.ID, "ControlLedgerId", "Sundry Creditors (Market)"
                )
                time.sleep(2)

            if self.switch_frames("mysubmit"):
                self.click_element(By.ID, "mysubmit")
                print("Successfully submitted", i["LedgerName"])
                time.sleep(2)

        print("All BankName created successfully.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

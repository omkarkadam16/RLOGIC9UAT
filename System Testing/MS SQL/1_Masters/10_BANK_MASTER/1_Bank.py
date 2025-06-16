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


class BankMaster(unittest.TestCase):
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

    def test_Bank(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        menus = ["Finance", "Finance Master »", "Bank Master »", "Bank"]
        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)

        series = [
            {
                "BankAccountNo": "123456789012",
                "BankName": "SBI Bank",
                "City": "MUMBAI",
                "IFSCCode": "SBIN0001234",
            },
            {
                "BankAccountNo": "987654321098",
                "BankName": "HDFC Bank",
                "City": "MUMBAI",
                "IFSCCode": "HDFC0005678",
            },
        ]

        for i in series:
            if self.switch_frames("btn_NewRecord"):
                self.click_element(By.ID, "btn_NewRecord")
                time.sleep(2)

            # Driver Info
            if self.switch_frames("BankAccountNo"):
                self.send_keys(By.ID, "BankAccountNo", i["BankAccountNo"])
                self.send_keys(By.ID, "BankName", i["BankName"])
                self.select_dropdown(By.ID, "AddressTypeId", "Office")
                self.send_keys(By.ID, "AddressLine", "123 Main St")
                self.autocomplete_select(By.ID, "CityId-select", i["City"])

                # Generate Branch Name as combination of Bank Name and City
                branch_name = f"{i['BankName']},{i['City'].title()}"
                # Send keys for Branch Name
                self.send_keys(By.ID, "BranchName", branch_name)

                self.send_keys(By.ID, "PinCode", "123456")
                self.send_keys(By.ID, "ContactNo", "8543216789")
                self.send_keys(By.ID, "Mob", "9543216789")
                self.send_keys(By.ID, "IFSCCode", i["IFSCCode"])
                self.select_dropdown(By.ID, "BankAccountTypeId", "Current Account")

            if self.switch_frames("mysubmit"):
                self.click_element(By.ID, "mysubmit")
                print("Successfully submitted", i["BankName"])
                time.sleep(2)

        print("All Banks created successfully.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

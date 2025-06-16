from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import pandas as pd


class LoginPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.implicitly_wait(3)
        cls.driver.maximize_window()

    def click_element(self, by, value, timeout=2):
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        ).click()

    def send_keys(self, by, value, text, timeout=2):
        AB = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        AB.clear()
        AB.send_keys(text)

    def dropdown_selection(self, by, value, option_text, timeout=2):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        dropdown = Select(self.driver.find_element(by, value))
        dropdown.select_by_visible_text(option_text)

    def switch_iframes(self, element_id):
        """Switches to the correct iframe containing the specified element."""
        driver = self.driver
        driver.switch_to.default_content()

        for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
            driver.switch_to.frame(iframe)
            if driver.find_elements(By.ID, element_id):
                return True
            driver.switch_to.default_content()
        return False

    def test_login(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")

        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "OMSGN9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful")

        menus = [
            "Transportation",
            "Transportation Master »",
            "Common Masters »",
            "Item Master",
        ]

        for link_text in menus:
            self.click_element(By.LINK_TEXT, link_text)

        if self.switch_iframes("btn_NewRecord"):
            self.click_element(By.ID, "btn_NewRecord")

        df = pd.read_excel("items.xlsx", engine="openpyxl")

        for index, row in df.iterrows():
            try:
                if self.switch_iframes("TransportProductName"):
                    self.send_keys(By.ID, "TransportProductName", str(row["Item Name"]))
                if self.switch_iframes("CommodityTypeId"):
                    self.dropdown_selection(By.ID, "CommodityTypeId", row["Commodity"])
                    self.click_element(By.ID, "mysubmitNew")

                    df.at[index, "Status"] = "Passed"
            except:
                df.at[index, "Status"] = "Failed"

        df.to_excel("items.xlsx", index=True, engine="openpyxl")

    @classmethod
    def tearDownClass(cls):
        """Closes the browser after tests are complete."""
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

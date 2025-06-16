import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time


class CustomerMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize WebDriver with Headless Mode"""
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe"),
        )
        cls.driver.implicitly_wait(2)
        cls.driver.maximize_window()

    def click_element(self, by, value, timeout=2):
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        ).click()
        # print(f"{value} clicked successfully")

    def send_keys(self, by, value, text, timeout=2):
        CE = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        CE.clear()
        CE.send_keys(text)
        # print(f"{value} updated with {text}")

    def switch_frames(self, element_id):
        driver = self.driver
        driver.switch_to.default_content()
        for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
            driver.switch_to.frame(iframe)
            try:
                if driver.find_element(By.ID, element_id):
                    # print(f"Switched to iframe containing {element_id}")
                    return True
            except:
                driver.switch_to.default_content()
        # print(f"Unable to locate {element_id} in any iframe!")
        return False

    def test_customer(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript/Login")

        self.send_keys(By.ID, "Login", "Admin")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful")

        menus = [
            "Transportation",
            "Transportation Master »",
            "Customer »",
            "Customer",
        ]

        for link_text in menus:
            self.click_element(By.LINK_TEXT, link_text)
            # print(f"{link_text} link clicked successfully")

        df = pd.read_excel("UID.xlsx", engine="openpyxl")

        for index, row in df.iterrows():
            try:
                if self.switch_frames("txt_Extrasearch"):
                    self.send_keys(By.ID, "txt_Extrasearch", str(row["UID"]))
                    self.click_element(By.ID, "btn_Seach")
                    time.sleep(1)

                    self.click_element(By.ID, row["DD"])
                edit_button = driver.find_element(By.PARTIAL_LINK_TEXT, "Edit")
                edit_button.click()

                if self.switch_frames("acaretdowndivGstEkyc"):
                    self.click_element(By.ID, "acaretdowndivGstEkyc")
                    self.click_element(By.ID, "btn_SearchGSTNo")

                if self.switch_frames("mysubmit"):
                    self.click_element(By.ID, "mysubmit")
                    print(f"Customer UID {row['UID']} KYC Updated successfully")
                    # time.sleep(2)
                    df.at[index, "Status"] = "Success"  # Update status in DataFrame

            except Exception as e:
                print(f"Failed to process UID {row['UID']}: {str(e)}")
                df.at[index, "Status"] = "Failed"

            df.to_excel(
                "UID.xlsx", index=False, engine="openpyxl"
            )  # Save after each entry

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

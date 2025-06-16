from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import unittest
import time
from selenium.common import exceptions as ex
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class CustomerMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Initializing WebDriver...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            "--disable-software-rasterizer"
        )  # Prevents WebGL issues
        chrome_options.add_argument("--enable-unsafe-swiftshader")
        chrome_options.add_argument("--disable-accelerated-2d-canvas")

        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, timeout=5)

    def send_keys(self, by, value, text):
        """Send text to an input field when it becomes visible."""
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        if element.is_enabled():
            element.clear()
            element.send_keys(text)
        else:
            raise Exception(f"Element located by ({by}, {value}) is not enabled.")

    def click_element(self, by, value, retries=2):
        """Click an element, retrying if necessary."""
        for attempt in range(retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
                return True
            except (
                ex.ElementClickInterceptedException,
                ex.StaleElementReferenceException,
                ex.TimeoutException,
            ):
                print(f"[WARNING] Attempt {attempt + 1} failed, retrying...")
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except:
            return False

    def switch_frames(self, element_id):
        """Switch to the iframe that contains a specific element."""
        self.driver.switch_to.default_content()
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            self.driver.switch_to.frame(iframe)
            try:
                if self.driver.find_element(By.ID, element_id):
                    return True
            except NoSuchElementException:
                self.driver.switch_to.default_content()
        return False

    def close_popups(self):
        """Close any popups if present."""
        try:
            close_button = self.driver.find_element(By.CLASS_NAME, "close")
            close_button.click()
        except:
            pass  # No popup found

    def test_customer(self):
        """Automates KYC update and stores timestamps in Excel"""
        driver = self.driver
        driver.get("http://r-logic9.com/RlogicDemoFtl/")

        # Login
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "OMSGN9")
        self.click_element(By.ID, "btnLogin")

        # Navigate to required page
        for link_text in [
            "Transportation",
            "Transportation Master »",
            "Consignor/Consignee »",
            "Consignor / Consignee",
        ]:
            self.click_element(By.LINK_TEXT, link_text)

        # Read Excel data
        df = pd.read_excel("UID 1.xlsx", engine="openpyxl")

        for index, row in df.iterrows():
            try:
                print(f"Processing UID: {row['UID']}")
                self.close_popups()

                if self.switch_frames("txt_Extrasearch"):
                    self.send_keys(By.ID, "txt_Extrasearch", str(row["UID"]))
                    self.click_element(By.ID, "btn_Seach")
                    self.click_element(By.ID, row["DD"])

                self.click_element(By.PARTIAL_LINK_TEXT, "Edit")
                time.sleep(2)

                if self.switch_frames("acaretdowndivGstEkyc"):
                    self.click_element(By.ID, "acaretdowndivGstEkyc")
                time.sleep(1)

                if self.switch_frames("btn_SearchGSTNo"):
                    if self.click_element(
                        By.ID, "btn_SearchGSTNo"
                    ):  # Status depends on this click

                        df.at[index, "Status"] = (
                            "Updated successfully"  # Update status immediately after button click
                        )

                        # Wait for ekycTradeName field and extract value
                        time.sleep(1)
                        consignee_name = self.wait.until(
                            EC.presence_of_element_located((By.ID, "ekycTradeName"))
                        )
                        consignee_value = consignee_name.get_attribute(
                            "value"
                        ).strip()  # Get updated timestamp
                        df.at[index, "Consignor/Consignee"] = (
                            consignee_value  # Store timestamp
                        )
                        # Wait for KYC update field and extract value
                        time.sleep(1)
                        ekyc_element = self.wait.until(
                            EC.presence_of_element_located((By.ID, "ekycLogDateTime"))
                        )
                        ekyc_value = ekyc_element.get_attribute(
                            "value"
                        ).strip()  # Get updated timestamp
                        df.at[index, "GST Verified On"] = ekyc_value  # Store timestamp
                    else:
                        df.at[index, "Status"] = "Not Updated (Button Click Failed)"
                        driver.execute_script("window.scrollTo(0, 1000);")

                if self.switch_frames("mysubmit"):
                    self.click_element(By.ID, "mysubmit")

            except Exception as e:
                print(f"Failed to process UID {row['UID']}: {str(e)}")

            df.to_excel("UID 1.xlsx", index=False, engine="openpyxl")
        print("✅ KYC Update Completed! Check UID 1.xlsx for results.")
        input("Press Enter to exit...")

    @classmethod
    def tearDownClass(cls):
        print("Closing WebDriver...")
        cls.driver.quit()
        print("WebDriver closed.")


if __name__ == "__main__":
    unittest.main()

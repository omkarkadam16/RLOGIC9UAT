from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
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
        """Initialize WebDriver"""
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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
                    print(f"Switched to iframe containing element: {element_id}")
                    return True
            except NoSuchElementException:
                self.driver.switch_to.default_content()

        print(f"Element with ID '{element_id}' not found in any iframe.")
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
                        driver.execute_script("window.scrollTo(0, 1000);")
                        df.at[index, "Status"] = (
                            "Updated successfully"  # Update status immediately after button click
                        )

                        # Wait for timestamp field and extract value
                        time.sleep(1)
                        consignee_name = self.wait.until(
                            EC.presence_of_element_located((By.ID, "ekycLegalName"))
                        )
                        consignee_value = consignee_name.get_attribute(
                            "value"
                        ).strip()  # Get updated timestamp
                        df.at[index, "Consignor/Consignee"] = (
                            consignee_value  # Store timestamp
                        )
                        # Wait for KYC update field and extract value
                        time.sleep(2)
                        ekyc_element = self.wait.until(
                            EC.presence_of_element_located((By.ID, "ekycLogDateTime"))
                        )
                        ekyc_value = ekyc_element.get_attribute(
                            "value"
                        ).strip()  # Get updated timestamp
                        print(
                            f"KYC Update Timestamp for UID {row['UID']}: {ekyc_value}"
                        )
                        df.at[index, "GST Verified On"] = ekyc_value  # Store timestamp
                    else:
                        df.at[index, "Status"] = "Not Updated (Button Click Failed)"

                if self.switch_frames("mysubmit"):
                    self.click_element(By.ID, "mysubmit")
                    print(
                        f"Consignor / Consignee UID {row['UID']} Data saved successfully"
                    )

            except Exception as e:
                print(f"Failed to process UID {row['UID']}: {str(e)}")

            df.to_excel("UID 1.xlsx", index=False, engine="openpyxl")
        print("✅ KYC Update Completed! Check UID 1.xlsx for results.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

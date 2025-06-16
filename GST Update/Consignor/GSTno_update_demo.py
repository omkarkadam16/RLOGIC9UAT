import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import unittest
import time
from selenium_helper import SeleniumHelper
from datetime import datetime


class CustomerMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize WebDriver"""
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe"),
        )
        cls.driver.maximize_window()
        cls.Helper = SeleniumHelper(cls.driver)

    def test_customer(self):
        driver = self.driver
        driver.get("http://r-logic9.com/RlogicDemoFtl/")

        # Login
        self.Helper.send_keys(By.ID, "Login", "Riddhi")
        self.Helper.send_keys(By.ID, "Password", "OMSGN9")
        self.Helper.click_element(By.ID, "btnLogin")
        print("Login successful")

        # Navigate to required page
        for link_text in [
            "Transportation",
            "Transportation Master »",
            "Consignor/Consignee »",
            "Consignor / Consignee",
        ]:
            self.Helper.click_element(By.LINK_TEXT, link_text)

        if self.Helper.switch_frames("tgladdnclm"):
            self.Helper.click_element(By.ID, "tgladdnclm")

        # Read Excel data
        df = pd.read_excel("GST 1.xlsx", engine="openpyxl")

        for index, row in df.iterrows():
            try:
                print(f"Processing UID: {row['UID']}")

                # Search for UID
                if self.Helper.switch_frames("txt_Extrasearch"):
                    self.Helper.send_keys(By.ID, "txt_Extrasearch", str(row["UID"]))
                    self.Helper.click_element(By.ID, "btn_Seach")

                max_attempts = 5  # Limit attempts to prevent infinite loops
                attempts = 0

                while attempts < max_attempts:
                    # Try clicking DD element
                    if self.Helper.click_element(By.ID, row["DD"]):
                        print(f"[INFO] Found and clicked DD: {row['DD']}")
                        self.Helper.click_element(By.PARTIAL_LINK_TEXT, "Edit")
                        break  # Exit while loop if successful

                    # Click "Next" to load more results if DD is not found
                    if not self.Helper.click_element(By.LINK_TEXT, "Next"):
                        print(
                            "[ERROR] 'Next' button not found. No more pages available."
                        )
                        break  # Exit while loop if there are no more results

                    attempts += 1

                self.Helper.click_element(By.PARTIAL_LINK_TEXT, "Edit")
                time.sleep(2)

                if self.Helper.switch_frames("acaretdowndivGstEkyc"):
                    self.Helper.click_element(By.ID, "acaretdowndivGstEkyc")

                self.Helper.send_keys(By.ID, "ekycGSTNo", row["GST"])
                print(f"Successfully entered GST No: {row['GST']}")
                self.Helper.click_element(By.ID, "btn_SearchGSTNo")

                if self.Helper.switch_frames("mysubmit"):
                    self.Helper.click_element(By.ID, "mysubmit")
                    print(
                        f"Consignor / Consignee UID {row['UID']} KYC Updated successfully"
                    )
                    df.at[index, "Status"] = "Passed"
                else:
                    print(
                        f"Consignor / Consignee UID {row['UID']} Failed to update KYC"
                    )
                    df.at[index, "Status"] = "Failed"
                df.at[index, "Execution Time"] = datetime.now().strftime(
                    "%Y-%m-%d  %H:%M:%S"
                )

            except Exception as e:
                print(f"Failed to process UID {row['UID']}: {str(e)}")
                df.at[index, "Status"] = "Failed"
            df.at[index, "Execution Time"] = datetime.now().strftime(
                "%Y-%m-%d  %H:%M:%S"
            )

            # Save after each entry
            df.to_excel("GST 1.xlsx", index=False, engine="openpyxl")
        print("All GST entries successfully saved")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

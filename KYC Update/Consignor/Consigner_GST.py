from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import unittest
import time
from selenium_helper import SeleniumHelper


class CustomerMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize WebDriver"""
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe"),
        )
        cls.driver.maximize_window()
        cls.helper = SeleniumHelper(cls.driver)

    def test_customer(self):
        driver = self.driver
        driver.get("http://r-logic9.com/RlogicDemoFtl/")

        # Login
        self.helper.send_keys(By.ID, "Login", "Riddhi")
        self.helper.send_keys(By.ID, "Password", "OMSGN9")
        self.helper.click_element(By.ID, "btnLogin")

        # Navigate to required page
        for link_text in [
            "Transportation",
            "Transportation Master »",
            "Consignor/Consignee »",
            "Consignor / Consignee",
        ]:
            self.helper.click_element(By.LINK_TEXT, link_text)

        # Read Excel data
        df = pd.read_excel("UID.xlsx", engine="openpyxl")

        for index, row in df.iterrows():
            try:
                print(f"Processing UID: {row['UID']}")
                self.helper.close_popups()  # Close popups before proceeding

                if self.helper.switch_frames("txt_Extrasearch"):
                    self.helper.send_keys(By.ID, "txt_Extrasearch", str(row["UID"]))
                    self.helper.click_element(By.ID, "btn_Seach")

                    self.helper.click_element(By.ID, row["DD"])

                self.helper.click_element(By.PARTIAL_LINK_TEXT, "Edit")
                time.sleep(2)

                if self.helper.switch_frames("acaretdowndivGstEkyc"):
                    self.helper.click_element(By.ID, "acaretdowndivGstEkyc")
                time.sleep(1)
                if self.helper.switch_frames("btn_SearchGSTNo"):
                    self.helper.click_element(By.ID, "btn_SearchGSTNo")
                    driver.execute_script("window.scrollTo(0, 1000);")
                    print(f"Customer UID {row['UID']} KYC Updated successfully")
                    df.at[index, "Status"] = "Updated successfully"
                    df.at[index, "Execution Time"] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                else:
                    print(f"Customer UID {row['UID']} Failed to update KYC")
                    df.at[index, "Status"] = "Not Updated"
                df.at[index, "Execution Time"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                if self.helper.switch_frames("mysubmit"):
                    self.helper.click_element(By.ID, "mysubmit")
                    # print(f"Customer UID {row['UID']} Data saved successfully")
                    # df.at[index, "Status"] = "Passed"
                # else:
                # print(f"Customer UID {row['UID']} Failed to save data")
                # df.at[index, "Status"] = "Failed"
                # df.at[index, "Execution Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            except Exception as e:
                print(f"Failed to process UID {row['UID']}: {str(e)}")
                # df.at[index, "Status"] = "Failed"
            # df.at[index, "Execution Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            df.to_excel(
                "UID.xlsx", index=False, engine="openpyxl"
            )  # Save only once at the end

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

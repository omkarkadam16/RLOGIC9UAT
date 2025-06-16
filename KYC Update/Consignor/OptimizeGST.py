from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import unittest
from selenium_helper import SeleniumHelper


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

        # Read Excel data
        df = pd.read_excel("UID.xlsx", engine="openpyxl")

        for index, row in df.iterrows():
            try:
                print(f"Processing UID: {row['UID']}")
                self.Helper.close_popups()  # Close popups before proceeding

                if self.Helper.switch_frames("txt_Extrasearch"):
                    self.Helper.send_keys(By.ID, "txt_Extrasearch", str(row["UID"]))
                    self.Helper.click_element(By.ID, "btn_Seach")
                    # time.sleep(1)

                    self.Helper.click_element(By.ID, row["DD"])

                self.Helper.click_element(By.PARTIAL_LINK_TEXT, "Edit")

                if self.Helper.switch_frames("acaretdowndivGstEkyc"):
                    self.Helper.click_element(By.ID, "acaretdowndivGstEkyc")
                    self.Helper.click_element(By.ID, "btn_SearchGSTNo")
                    # time.sleep(1)
                    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    driver.execute_script(
                        "window.scrollTo(0, 1000);"
                    )  # Scroll to bottom

                if self.Helper.switch_frames("mysubmit"):
                    self.Helper.click_element(By.ID, "mysubmit")
                    print(f"Customer UID {row['UID']} KYC Updated successfully")
                    df.at[index, "Status"] = "Passed"
                    df.at[index, "Execution Time"] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                else:
                    print(f"Customer UID {row['UID']} KYC update failed")
                    df.at[index, "Status"] = "Failed"

            except Exception as e:
                print(f"Failed to process UID {row['UID']}: {str(e)}")
                df.at[index, "Status"] = "Failed"
                df.at[index, "Execution Time"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

            # Save after each entry
            df.to_excel("UID.xlsx", index=False, engine="openpyxl")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

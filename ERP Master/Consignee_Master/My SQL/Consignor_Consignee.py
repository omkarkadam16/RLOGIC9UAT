from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import unittest
import time
from selenium_helper import SeleniumHelper


class ConsignorMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.maximize_window()
        cls.Helper = SeleniumHelper(cls.driver)

    def test_consignor(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript/#")

        self.Helper.send_keys(By.ID, "Login", "admin")
        self.Helper.send_keys(By.ID, "Password", "omsgn9")
        self.Helper.click_element(By.ID, "btnLogin")
        print("Login successful")

        for link_text in [
            "Transportation",
            "Transportation Master »",
            "Consignor/Consignee »",
            "Consignor / Consignee",
        ]:
            self.Helper.click_element(By.LINK_TEXT, link_text)
            print(f"{link_text} link clicked successfully")

        if self.Helper.switch_frames("btn_NewRecord"):
            self.Helper.click_element(By.ID, "btn_NewRecord")

        df = pd.read_excel("consignor_data.xlsx")
        for index, row in df.iterrows():
            try:
                # Basic Information
                if self.Helper.switch_frames("Party_PartyName"):
                    self.Helper.send_keys(By.ID, "Party_PartyName", row["PartyName"])
                    self.Helper.select_dropdown(
                        By.ID, "Party_PartyIndustryTypeId", row["PartyIndustryType"]
                    )

                if self.Helper.switch_frames("EffectiveFromDate"):
                    self.Helper.send_keys(
                        By.ID, "EffectiveFromDate", row["EffectiveFromDate"]
                    )
                    self.Helper.send_keys(By.ID, "PANNo", row["PANNo"])
                    print("Basic Information saved successfully")

                # Address Details
                if self.Helper.switch_frames("AddressTypeId"):
                    self.Helper.select_dropdown(
                        By.ID, "AddressTypeId", row["AddressType"]
                    )
                    self.Helper.send_keys(By.ID, "AddressLine", row["AddressLine"])
                    self.Helper.autocomplete_select(By.ID, "CityId-select", row["City"])
                    self.Helper.send_keys(By.ID, "PinCode", str(row["PinCode"]))
                    self.Helper.send_keys(By.ID, "ContactNo", str(row["ContactNo"]))
                    self.Helper.send_keys(By.ID, "Mob", str(row["Mob"]))
                    self.Helper.click_element(By.ID, "btnSave-AddressSession748")
                    print("Address Details saved successfully")
                    driver.save_screenshot("Address_Details.png")

                # Registration Number Details
                if self.Helper.switch_frames("RegistrationHeadId"):
                    self.Helper.select_dropdown(
                        By.ID, "RegistrationHeadId", row["RegistrationHead"]
                    )
                    self.Helper.send_keys(
                        By.ID, "Number", str(row["RegistrationNumber"])
                    )
                    self.Helper.click_element(By.ID, "btnSave-RegistrationSession748")

                # GST Registration
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(2)  # Small delay before clicking
                if self.Helper.switch_frames("liTab5"):
                    self.Helper.click_element(By.ID, "liTab5")

                if self.Helper.switch_frames("StateId"):
                    self.Helper.select_dropdown(By.ID, "StateId", row["State"])
                    self.Helper.select_dropdown(
                        By.ID, "BusinessVerticalId", row["BusinessVertical"]
                    )
                    self.Helper.send_keys(By.ID, "GSTNumber", str(row["GSTNumber"]))
                    self.Helper.click_element(
                        By.ID, "btnSave-CustGSTRegistrationSession748"
                    )
                    driver.save_screenshot("GST_Registration.png")

                # Submit Form
                if self.Helper.switch_frames("mysubmitNew"):
                    self.Helper.click_element(By.ID, "mysubmitNew")
                    time.sleep(1)
                    print(
                        f"Consignor/Consignee {row['PartyName']} record created successfully"
                    )
                else:
                    print(f"Customer UID {row['UID']} Failed to update record")
                    df.at[index, "Status"] = "Failed"
                df.at[index, "Execution Time"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

            except Exception as e:
                print(f"Failed to process UID {row['UID']}: {str(e)}")
                df.at[index, "Status"] = "Failed"
            df.at[index, "Execution Time"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            # ✅ Save the updated DataFrame after each iteration
            df.to_excel("consignor_data.xlsx", index=False, engine="openpyxl")

    @classmethod
    def tearDownClass(cls):
        """Closes the browser after tests are complete."""
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

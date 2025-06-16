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
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.maximize_window()
        cls.Helper=SeleniumHelper(cls.driver)


    def test_customer(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")

        self.Helper.send_keys(By.ID, "Login", "Riddhi")
        self.Helper.send_keys(By.ID, "Password", "OMSGN9")
        self.Helper.click_element(By.ID, "btnLogin")
        print("Login successful")

        menus = [
            "Transportation",
            "Transportation Master »",
            "Customer »",
            "Customer",
        ]

        for link_test in menus:
            self.Helper.click_element(By.LINK_TEXT, link_test)
            print(f"{link_test} link clicked successfully")

        if self.Helper.switch_frames("btn_NewRecord"):
            self.Helper.click_element(By.ID, "btn_NewRecord")

        df = pd.read_excel("customer_data.xlsx")
        for _, row in df.iterrows():

            # Basic Information
            if self.Helper.switch_frames("Party_PartyName"):
                self.Helper.send_keys(By.ID, "Party_PartyName", row["PartyName"])

                self.Helper.select_dropdown(
                    By.ID, "Party_PartyCategoryId", row["PartyCategory"]
                )

                self.Helper.select_dropdown(
                    By.ID, "Party_PartyIndustryTypeId", row["PartyIndustryType"]
                )

                self.Helper.select_dropdown(By.ID, "Party_PartyGradeId", row["PartyGrade"])

                self.Helper.select_dropdown(By.ID, "Party_PartyGroupId", row["PartyGroup"])
            if self.Helper.switch_frames("EffectiveFromDate"):
                self.Helper.send_keys(By.ID, "EffectiveFromDate", row["EffectiveFromDate"])

                self.Helper.send_keys(By.ID, "PANNo", row["PANNo"])

                driver.save_screenshot("Basic Details.png")

            # Address Details
            if self.Helper.switch_frames("AddressTypeId"):
                self.Helper.select_dropdown(By.ID, "AddressTypeId", row["AddressType"])
                self.Helper.send_keys(By.ID, "AddressLine", row["AddressLine"])
                self.Helper.autocomplete_select(By.ID, "CityId-select", row["City"])
                self.Helper.send_keys(By.ID, "PinCode", str(row["PinCode"]))
                self.Helper.send_keys(By.ID, "ContactNo", str(row["ContactNo"]))
                self.Helper.send_keys(By.ID, "Mob", str(row["Mob"]))
                self.Helper.click_element(By.ID, "btnSave-AddressSession77")

                driver.save_screenshot("Address Details.png")

            # Registation Number Details

            if self.Helper.switch_frames("RegistrationHeadId"):
                self.Helper.select_dropdown(
                    By.ID, "RegistrationHeadId", row["RegistrationHead"]
                )

                self.Helper.send_keys(By.ID, "Number", str(row["RegistrationNumber"]))

                self.Helper.click_element(By.ID, "btnSave-RegistrationSession77")

                driver.save_screenshot("Registration Number Details.png")

            # Account Information
            driver.execute_script(
                "window.scrollTo(0, 0);"
            )  # Scroll up before switching to "liTab2"
            time.sleep(3)  # Add a small delay before clicking
            if self.Helper.switch_frames("liTab2"):
                self.Helper.click_element(By.ID, "liTab2")

            # Payment Types (No Loop, Three Columns)
            if self.Helper.switch_frames("PaymentTypeId"):
                self.Helper.select_dropdown(By.ID, "PaymentTypeId", row["PaymentType1"])
                self.Helper.click_element(By.ID, "btnSave-PaymentTypeConfigSession77")
                time.sleep(2)

                self.Helper.select_dropdown(By.ID, "PaymentTypeId", row["PaymentType2"])
                self.Helper.click_element(By.ID, "btnSave-PaymentTypeConfigSession77")
                time.sleep(2)

                self.Helper.select_dropdown(By.ID, "PaymentTypeId", row["PaymentType3"])
                self.Helper.click_element(By.ID, "btnSave-PaymentTypeConfigSession77")

            # Billing Details
            if self.Helper.switch_frames("BillingOn"):
                self.Helper.select_dropdown(By.ID, "BillingOn", "Booking")
                self.Helper.select_dropdown(By.ID, "BillingLocationTypeId", "Booking Branch")
                self.Helper.autocomplete_select(
                    By.ID, "CollectionLocationId-select", "AHMEDABAD"
                )
            if self.Helper.switch_frames("SubmissionLocationId-select"):
                self.Helper.autocomplete_select(By.ID, "SubmissionLocationId-select", "MUMBAI")
                self.Helper.send_keys(By.ID, "CreditDays", "20")
                self.Helper.send_keys(By.ID, "Party_CreditLimit", "20000")
                driver.save_screenshot("Account Information.png")

            # GST Registration
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)  # Add a small delay before clicking
            if self.Helper.switch_frames("liTab5"):
                self.Helper.click_element(By.ID, "liTab5")

            if self.Helper.switch_frames("StateId"):
                self.Helper.select_dropdown(By.ID, "StateId", row["State"])
                self.Helper.select_dropdown(
                    By.ID, "BusinessVerticalId", row["BusinessVertical"]
                )
                self.Helper.send_keys(By.ID, "GSTNumber", str(row["GSTNumber"]))
                self.Helper.click_element(By.ID, "btnSave-CustGSTRegistrationSession77")
                driver.save_screenshot("GST Registration.png")

            # Submit Form
            if self.Helper.switch_frames("mysubmitNew"):
                self.Helper.click_element(By.ID, "mysubmitNew")
                print(f"Customer {row['PartyName']} record created successfully")
                time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        """Closes the browser after tests are complete."""
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

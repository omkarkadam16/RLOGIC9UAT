from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import unittest
import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as ex
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ConsignorMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

    def click_element(self, by, value, max_attempts=3):
        attempt = 0
        element = None

        while attempt < max_attempts:
            try:
                element = self.wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
                print(f"[SUCCESS] Clicked element: {value}")
                return True
            except (
                ex.ElementClickInterceptedException,
                ex.StaleElementReferenceException,
                ex.TimeoutException,
            ) as e:
                print(
                    f"[WARNING] Attempt {attempt + 1}: {type(e).__name__} occurred. Retrying..."
                )
                time.sleep(1)

            # JavaScript Click Fallback
            if element:
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    print(f"[SUCCESS] Clicked element using JavaScript: {value}")
                    return True
                except ex.JavascriptException as js_error:
                    print(
                        f"[ERROR] JavaScript click failed due to {type(js_error).__name__}"
                    )

            attempt += 1
            time.sleep(1)

        print(f"[ERROR] Failed to click element {value} after {max_attempts} attempts.")
        return False

    def send_keys(self, by, value, text):
        """
        Send text to an input field when it becomes visible.
        :param by: Locator strategy
        :param value: Locator value
        :param text: Text to be entered
        """
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        if element.is_enabled():
            element.clear()
            element.send_keys(text)
        else:
            raise Exception(f"Element located by ({by}, {value}) is not enabled.")

    def select_dropdown(self, by, value, option_text):
        """
        Select an option from a dropdown by visible text.
        :param by: Locator strategy
        :param value: Locator value
        :param option_text: Option text to select
        """
        self.wait.until(EC.visibility_of_element_located((by, value)))
        dropdown = Select(self.driver.find_element(by, value))
        dropdown.select_by_visible_text(option_text)

    def autocomplete_select(self, by, value, text):
        """
        Select an autocomplete suggestion based on input text.
        :param by: Locator strategy
        :param value: Locator value
        :param text: Text to input and search in suggestions
        """
        input_field = self.wait.until(EC.visibility_of_element_located((by, value)))
        input_field.clear()
        input_field.send_keys(text)
        time.sleep(2)  # Allow time for suggestions to appear
        suggestions = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-menu-item"))
        )
        for suggestion in suggestions:
            if text.upper() in suggestion.text.upper():
                suggestion.click()
                return
        input_field.send_keys(Keys.DOWN)
        input_field.send_keys(Keys.ENTER)

    def switch_frames(self, element_id):
        driver = self.driver
        driver.switch_to.default_content()
        frames = driver.find_elements(By.TAG_NAME, "iframe")

        for frame in frames:
            driver.switch_to.frame(frame)
            try:
                driver.find_element(By.ID, element_id)
                print(f"Switched to iframe containing element: {element_id}")
                return True
            except NoSuchElementException:
                driver.switch_to.default_content()

        print(f"[ERROR] Element with ID '{element_id}' not found in any iframe.")
        return False

    def test_consignor(self):
        driver = self.driver
        driver.get("http://r-logic9.com/RlogicDemoFtl/")
        df = pd.read_excel("consignor_data.xlsx")

        # Login
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "OMSGN9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful")

        self.click_element(By.LINK_TEXT, "Transportation")
        self.click_element(By.LINK_TEXT, "Transportation Master »")
        self.click_element(By.LINK_TEXT, "Consignor/Consignee »")
        self.click_element(By.LINK_TEXT, "Consignor / Consignee")
        for index, row in df.iterrows():
            try:

                if self.switch_frames("btn_NewRecord"):
                    self.click_element(By.ID, "btn_NewRecord")

                    # Basic Information
                    if self.switch_frames("Party_PartyName"):
                        self.send_keys(By.ID, "Party_PartyName", row["PartyName"])
                        self.select_dropdown(
                            By.ID, "Party_PartyIndustryTypeId", row["PartyIndustryType"]
                        )

                    if self.switch_frames("EffectiveFromDate"):
                        self.send_keys(
                            By.ID, "EffectiveFromDate", row["EffectiveFromDate"]
                        )
                        self.send_keys(By.ID, "PANNo", row["PANNo"])
                        print("Basic Information saved successfully")
                    time.sleep(2)

                    # Address Details
                    # if self.switch_frames("AddressLine"):
                    self.send_keys(By.ID, "AddressLine", row["AddressLine"])
                    self.autocomplete_select(By.ID, "CityId-select", row["City"])
                    self.send_keys(By.ID, "PinCode", str(row["PinCode"]))
                    self.send_keys(By.ID, "ContactNo", str(row["ContactNo"]))
                    self.send_keys(By.ID, "Mob", str(row["Mob"]))
                    self.click_element(By.ID, "btnSave-AddressSession748")
                    print("Address Details saved successfully")
                    driver.save_screenshot("Address_Details.png")
                    time.sleep(2)

                    # Registration Number Details
                    if self.switch_frames("RegistrationHeadId"):
                        self.select_dropdown(
                            By.ID, "RegistrationHeadId", row["RegistrationHead"]
                        )
                        self.send_keys(By.ID, "Number", str(row["RegistrationNumber"]))
                        self.click_element(By.ID, "btnSave-RegistrationSession748")

                        # GST Registration
                    driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(2)  # Small delay before clicking
                    if self.switch_frames("liTab5"):
                        self.click_element(By.ID, "liTab5")

                    if self.switch_frames("StateId"):
                        self.select_dropdown(By.ID, "StateId", row["State"])
                        self.select_dropdown(
                            By.ID, "BusinessVerticalId", row["BusinessVertical"]
                        )
                        self.send_keys(By.ID, "GSTNumber", str(row["GSTNumber"]))
                        self.click_element(
                            By.ID, "btnSave-CustGSTRegistrationSession748"
                        )
                        driver.save_screenshot("GST_Registration.png")

                        # Submit Form
                    if self.switch_frames("mysubmit"):
                        self.click_element(By.ID, "mysubmit")
                        time.sleep(1)
                        print(
                            f"Consignor/Consignee {row['PartyName']} record created successfully"
                        )
                        df.at[index, "Status"] = "Passed"
                        df.at[index, "Execution Time"] = datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )

            except Exception as e:
                print(f"Failed to process UID {row['PartyName']}: {str(e)}")
                df.at[index, "Status"] = "Failed"
            df.at[index, "Execution Time"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            df.to_excel("consignor_data.xlsx", index=False, engine="openpyxl")

    @classmethod
    def tearDownClass(cls):
        """Closes the browser after tests are complete."""
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

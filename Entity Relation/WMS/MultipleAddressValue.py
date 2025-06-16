from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import unittest
import time
from selenium.common import exceptions as ex
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


class EntityRelation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

    def send_keys(self, by, value, text):
        """Send text to an input field when it becomes visible."""
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        if element.is_enabled():
            element.clear()
            element.send_keys(text)
        else:
            raise Exception(f"Element located by ({by}, {value}) is not enabled.")

    def switch_frames(self, element_id):
        self.driver.switch_to.default_content()
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            self.driver.switch_to.frame(iframe)
            try:
                if self.driver.find_element(By.ID, element_id):
                    return True
            except ex.NoSuchElementException:
                self.driver.switch_to.default_content()
        return False

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

    def test_master(self):
        self.driver.get("http://124.123.122.23:83/RlogicGtc")
        self.driver.find_element(By.ID, "Login").send_keys("RIDDHI")
        self.driver.find_element(By.ID, "Password").send_keys("omsgn9")
        self.driver.find_element(By.ID, "btnLogin").click()
        print("Login successful")

        for links in [
            "Administration",
            "Implementation »",
            "Entity Relation",
        ]:
            self.driver.find_element(By.LINK_TEXT, links).click()

            series = [
                {
                    "Property": "AddressTypeId",
                    "Column": "AddressType",
                    "Entity": "AddressType",
                    "Key": "Uid",
                    "Display": "AddressTypeName",
                },
                {
                    "Property": "AddressLine",
                    "Column": "AddressLine",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Property": "CityId",
                    "Column": "City",
                    "Entity": "City",
                    "Key": "Uid",
                    "Display": "CityName",
                },
                {
                    "Property": "PinCode",
                    "Column": "PinCode",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Property": "ContactNo",
                    "Column": "ContactNos",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Property": "Fax",
                    "Column": "FaxNo",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Property": "Mob",
                    "Column": "Mobile",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Property": "ReferenceLinkId",
                    "Column": "LinkId",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Property": "TransactionId",
                    "Column": "PartyName",
                    "Entity": "Party",
                    "Key": "Uid",
                    "Display": "PartyName",
                },
                {
                    "Property": "AdditionalKey",
                    "Column": "AdditionalKey",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Property": "StdCode",
                    "Column": "StdCode",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Property": "Email",
                    "Column": "Email",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Property": "Code",
                    "Column": "Code",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
            ]

            # Wait and switch frame if needed
            if self.switch_frames("LinkId-select"):
                input_box = self.driver.find_element(By.ID, "LinkId-select")
                input_box.clear()
                input_box.send_keys("Multiple Address Value")

                # Wait for the suggestion box to appear
                wait = WebDriverWait(self.driver, 10)
                suggestion = wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            "//ul[@id='ui-id-1']//li//a[text()='Multiple Address Value']",
                        )
                    )
                )

                # Click the suggestion
                suggestion.click()
                print("Multiple Address Value selected")

                # Move to AsmQualifiedName input
                asm_input = self.driver.find_element(By.ID, "AsmQualifiedName")
                asm_input.click()

                if self.switch_frames("AsmQualifiedName"):
                    self.send_keys(
                        By.ID,
                        "AsmQualifiedName",
                        "RSuite.Domain.Common.Geography.AddressValue,RSuite.Domain.Common",
                    )
                    self.send_keys(By.ID, "EntityCode", "ADS")
                    self.send_keys(By.ID, "EntityName", "AddressValue")
                    self.send_keys(By.ID, "PrimaryGroupColumns", "Code")
                    self.click_element(
                        By.ID, "btnSave-ImportEntityColumnSessionName782"
                    )
                    time.sleep(2)

                for row in series:
                    self.send_keys(By.XPATH, "(//input[@name='EntityCode'])[2]", "ADS")

                    if pd.notna(row["Property"]):
                        self.send_keys(By.ID, "EntityProperty", row["Property"])

                    if pd.notna(row["Column"]):
                        self.send_keys(By.ID, "ImportColumnName", row["Column"])

                    if pd.notna(row["Entity"]) and row["Entity"] != "None":
                        self.send_keys(By.ID, "ForeignEntityName", row["Entity"])

                    if pd.notna(row["Key"]) and row["Key"] != "None":
                        self.send_keys(By.ID, "ForeignKeyName", row["Key"])

                    if pd.notna(row["Display"]) and row["Display"] != "None":
                        self.send_keys(By.ID, "ForeignDisplayName", row["Display"])

                        # Save button click for Sheet2
                    if self.switch_frames(
                        "btnSave-ImportEntityColumnMapSessionName782"
                    ):
                        self.click_element(
                            By.ID, "btnSave-ImportEntityColumnMapSessionName782"
                        )
                        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

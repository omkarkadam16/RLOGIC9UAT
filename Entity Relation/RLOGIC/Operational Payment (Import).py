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

    def autocomplete_select(self, by, value, text):
        input_field = self.wait.until(EC.visibility_of_element_located((by, value)))
        input_field.clear()
        input_field.send_keys(text)
        time.sleep(2)  # Allow time for suggestions to appear
        suggestions = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-menu-item"))
        )
        for i in suggestions:
            if text.upper() in i.text.upper():
                i.click()
                print("Selected autocomplete option:", text)
                return
        input_field.send_keys(Keys.DOWN)
        input_field.send_keys(Keys.ENTER)
        print("Selected autocomplete option using keyboard:", text)

    def test_master(self):
        self.driver.get("http://103.30.74.234/RLogicspg")
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
                    "Code": "IMPVP",
                    "Property": "BankId",
                    "Column": "BankName",
                    "Entity": "Bank",
                    "Key": "Uid",
                    "Display": "BankName",
                },
                {
                    "Code": "IMPVP",
                    "Property": "CashLedgerId",
                    "Column": "CashLedger",
                    "Entity": "Ledger",
                    "Key": "Uid",
                    "Display": "LedgerName",
                },
                {
                    "Code": "IMPVP",
                    "Property": "ChequeDate",
                    "Column": "ChequeDate",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVP",
                    "Property": "ChequeNo",
                    "Column": "ChequeNo",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVP",
                    "Property": "DocumentDate",
                    "Column": "DocumentDate",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVP",
                    "Property": "LocationId",
                    "Column": "Location",
                    "Entity": "OrganizationLocation",
                    "Key": "Uid",
                    "Display": "OrganizationLocationName",
                },
                {
                    "Code": "IMPVP",
                    "Property": "OperationalPaymentTypeId",
                    "Column": "OperationalPaymentTypeId",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVP",
                    "Property": "PaidTo",
                    "Column": "PaidTo",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVP",
                    "Property": "PayAmount",
                    "Column": "PayAmount",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVP",
                    "Property": "PaymentModeId",
                    "Column": "PaymentMode",
                    "Entity": "PaymentMode",
                    "Key": "Uid",
                    "Display": "PaymentModeName",
                },
                {
                    "Code": "IMPVP",
                    "Property": "ReferenceNo",
                    "Column": "ReferenceNo",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVP",
                    "Property": "RTGSDate",
                    "Column": "RTGSDate",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVP",
                    "Property": "RTGSNo",
                    "Column": "RTGSNo",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVPFC",
                    "Property": "FuelAmount",
                    "Column": "FuelAmount",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVPFC",
                    "Property": "FuelCardNo",
                    "Column": "FuelCardNo",
                    "Entity": "DigiCard",
                    "Key": "Uid",
                    "Display": "DigiCardNo",
                },
                {
                    "Code": "IMPVPFC",
                    "Property": "FuelSlipTypeId",
                    "Column": "FuelSlipType",
                    "Entity": "TrpMasterInternal",
                    "Key": "Uid",
                    "Display": "MasterName",
                },
                {
                    "Code": "IMPVPFC",
                    "Property": "FuelVendorId",
                    "Column": "FuelVendor",
                    "Entity": "Party",
                    "Key": "Uid",
                    "Display": "PartyName",
                },
                {
                    "Code": "IMPVPFC",
                    "Property": "Qty",
                    "Column": "Qty",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVPFC",
                    "Property": "Value",
                    "Column": "Value",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVPTRIP",
                    "Property": "BillRefNo",
                    "Column": "TripNo",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVPTRIP",
                    "Property": "IsATH",
                    "Column": "IsATH",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVPTRIP",
                    "Property": "PaidAmount",
                    "Column": "PaidAmount",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVPFC",
                    "Property": "SlipNo",
                    "Column": "SlipNo",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVPOBAR",
                    "Property": "LedgerMappingTypeId",
                    "Column": "LedgerMappingTypeId",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVPOBAR",
                    "Property": "BillRefTypeId",
                    "Column": "BillRefTypeId",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVPOBAR",
                    "Property": "Sign",
                    "Column": "Sign",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVPOBAR",
                    "Property": "PaidAmount",
                    "Column": "IPaidAmount",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVP",
                    "Property": "SeriesId",
                    "Column": "SeriesName",
                    "Entity": "Series",
                    "Key": "Uid",
                    "Display": "SeriesName",
                },
                {
                    "Code": "IMPVPFC",
                    "Property": "FuelTypeId",
                    "Column": "FuelType",
                    "Entity": "TransportMaster",
                    "Key": "Uid",
                    "Display": "MasterName",
                },
                {
                    "Code": "IMPVP",
                    "Property": "Code",
                    "Column": "Code",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVPOBAR",
                    "Property": "BillRefNo",
                    "Column": "BillRefNo",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
                {
                    "Code": "IMPVPOBAR",
                    "Property": "OrganizationalLocationId",
                    "Column": "OprLocation",
                    "Entity": "OrganizationLocation",
                    "Key": "Uid",
                    "Display": "OrganizationLocationName",
                },
                {
                    "Code": "IMPVP",
                    "Property": "VehicleId",
                    "Column": "VehicleNo",
                    "Entity": "Vehicle",
                    "Key": "Uid",
                    "Display": "VehicleNo",
                },
                {
                    "Code": "IMPVPFC",
                    "Property": "Code",
                    "Column": "Code",
                    "Entity": "None",
                    "Key": "None",
                    "Display": "None",
                },
            ]

            # Wait and switch frame if needed
            if self.switch_frames("LinkId-select"):
                self.autocomplete_select(
                    By.ID, "LinkId-select", "Operational Payment (Import)"
                )

                # Move to AsmQualifiedName input
                asm_input = self.driver.find_element(By.ID, "AsmQualifiedName")
                asm_input.click()

                # D1
                if self.switch_frames("AsmQualifiedName"):
                    self.send_keys(
                        By.ID,
                        "AsmQualifiedName",
                        "RSuite.Custom.Domains.Imports.ImportVendorPayment,RSuite.Custom",
                    )
                    self.send_keys(By.ID, "EntityCode", "IMPVP")
                    self.send_keys(By.ID, "EntityName", "ImportVendorPayment")
                    self.send_keys(By.ID, "PrimaryGroupColumns", "Code")
                    self.click_element(
                        By.ID, "btnSave-ImportEntityColumnSessionName782"
                    )
                    time.sleep(2)

                # D2
                if self.switch_frames("AsmQualifiedName"):
                    self.send_keys(
                        By.ID,
                        "AsmQualifiedName",
                        "RSuite.Custom.Domains.Imports.ImportVendorPaymentTrip,RSuite.Custom",
                    )
                    self.send_keys(By.ID, "EntityCode", "IMPVPTRIP")
                    self.send_keys(By.ID, "EntityName", "ImportVendorPaymentTrip")
                    self.send_keys(By.ID, "ParentEntityCode", "IMPVP")
                    self.send_keys(By.ID, "PrimaryGroupColumns", "TripNo")
                    self.send_keys(
                        By.ID, "PropertyName", "ImportVendorPaymentTripCollection"
                    )
                    self.click_element(
                        By.ID, "btnSave-ImportEntityColumnSessionName782"
                    )
                    time.sleep(2)

                    # D3
                    if self.switch_frames("AsmQualifiedName"):
                        self.send_keys(
                            By.ID,
                            "AsmQualifiedName",
                            "RSuite.Custom.Domains.Imports.ImportVendorPaymentFuelConsumption,RSuite.Custom",
                        )
                        self.send_keys(By.ID, "EntityCode", "IMPVPFC")
                        self.send_keys(
                            By.ID, "EntityName", "ImportVendorPaymentFuelConsumption"
                        )
                        self.send_keys(By.ID, "ParentEntityCode", "IMPVP")
                        self.send_keys(By.ID, "PrimaryGroupColumns", "Code")
                        self.send_keys(
                            By.ID,
                            "PropertyName",
                            "ImportVendorPaymentFuelConsumptionCollection",
                        )
                        self.click_element(
                            By.ID, "btnSave-ImportEntityColumnSessionName782"
                        )
                        time.sleep(2)

                        # D4
                        if self.switch_frames("AsmQualifiedName"):
                            self.send_keys(
                                By.ID,
                                "AsmQualifiedName",
                                "RSuite.Domain.Transport.Control.OperationalBillReference,RSuite.Domain.Transport",
                            )
                            self.send_keys(By.ID, "EntityCode", "IMPVPOBAR")
                            self.send_keys(
                                By.ID, "EntityName", "OperationalBillReference"
                            )
                            self.send_keys(By.ID, "ParentEntityCode", "IMPVP")
                            self.send_keys(By.ID, "PrimaryGroupColumns", "BillRefNo")
                            self.send_keys(
                                By.ID,
                                "PropertyName",
                                "ImportVendorPaymentOperationalBillAdvanceReferenceCollection",
                            )
                            self.click_element(
                                By.ID, "btnSave-ImportEntityColumnSessionName782"
                            )
                            time.sleep(2)

                for row in series:
                    self.send_keys(
                        By.XPATH, "(//input[@name='EntityCode'])[2]", row["Code"]
                    )

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

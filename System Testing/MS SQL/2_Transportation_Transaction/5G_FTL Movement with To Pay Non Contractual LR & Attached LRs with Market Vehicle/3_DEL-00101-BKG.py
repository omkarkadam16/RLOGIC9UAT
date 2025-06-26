from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager

# To Pay Recoverable Document Mapping error = Add Cr and Dr for Booking(Sundry Debtors)


class Booking(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 15)

    def click_element(self, by, value, retry=2):
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by, value))).click()
                print("Clicked on element", value)
                return True
            except (
                ex.ElementClickInterceptedException,
                ex.StaleElementReferenceException,
                ex.TimeoutException,
            ):
                print(
                    f"Retrying click on {by} with value {value}, attempt {i+1}/{retry}"
                )
                time.sleep(1)
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except:
            return False

    def switch_frames(self, element_id):
        driver = self.driver
        driver.switch_to.default_content()
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            driver.switch_to.frame(iframe)
            try:
                if driver.find_element(By.ID, element_id):
                    return True
            except ex.NoSuchElementException:
                driver.switch_to.default_content()
        return False

    def send_keys(self, by, value, text):
        try:
            element = self.wait.until(EC.visibility_of_element_located((by, value)))
            element.clear()
            element.send_keys(text)
            print(f"Sent keys {text} to {by} with value {value}")
            return True
        except ex.NoSuchElementException:
            print(f"Element not found: {value}")
            return False

    def select_dropdown(self, by, value, text):
        try:
            e = self.wait.until(EC.element_to_be_clickable((by, value)))
            e.is_enabled()
            e.click()
            print("[SUCCESS] Clicked dropdown")
            self.wait.until(EC.visibility_of_element_located((by, value)))
            element = Select(self.driver.find_element(by, value))
            element.select_by_visible_text(text)
            print(f"[SUCCESS] Selected dropdown option: {text}")
            return True
        except (
            ex.NoSuchElementException,
            ex.ElementClickInterceptedException,
            ex.TimeoutException,
        ):
            return False

    def autocomplete_select(self, by, value, text):
        input_text = self.wait.until(EC.visibility_of_element_located((by, value)))
        input_text.clear()
        input_text.send_keys(text)
        time.sleep(1)
        suggest = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-menu-item"))
        )
        for i in suggest:
            if text.upper() in i.text.upper():
                i.click()
                time.sleep(1)
                print("Selected autocomplete option:", text)
                return
        input_text.send_keys(Keys.DOWN)
        input_text.send_keys(Keys.ENTER)
        print("Selected autocomplete option using keyboard:", text)

    def test_booking(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        for i in (
            "Transportation",
            "Transportation Transaction »",
            "Booking »",
            "Consignment Note",
        ):
            self.click_element(By.LINK_TEXT, i)
            print(f"Navigated to {i}.")

        if self.switch_frames("btn_NewRecord"):
            self.click_element(By.ID, "btn_NewRecord")

        # Document Details
        if self.switch_frames("OrganizationId"):
            self.select_dropdown(By.ID, "OrganizationId", "DELHI")
            self.select_dropdown(By.ID, "SeriesId", "DELHI - 101 To 500")
            # Calendar
            self.click_element(By.CLASS_NAME, "ui-datepicker-trigger")
            self.select_dropdown(By.CLASS_NAME, "ui-datepicker-month", "Apr")
            self.select_dropdown(By.CLASS_NAME, "ui-datepicker-year", "2025")
            self.click_element(By.XPATH, "//a[text()='5']")

        # Booking Details
        self.select_dropdown(By.ID, "FreightOnId", "Fixed")
        self.select_dropdown(By.ID, "PaymentTypeId", "To Pay")
        self.select_dropdown(By.ID, "BookingTypeId", "FTL")
        self.select_dropdown(By.ID, "BookingModeId", "Road")
        self.select_dropdown(By.ID, "DeliveryTypeId", "Door")
        self.select_dropdown(By.ID, "PickupTypeId", "Door")
        self.select_dropdown(By.ID, "RiskTypeId", "Owners Risk")
        self.select_dropdown(By.ID, "ConsigneeCopyWithId", "Consignor")
        self.click_element(By.ID, "IsPOD")

        # Route Details
        self.autocomplete_select(By.ID, "FromServiceNetworkId-select", "DELHI")
        self.autocomplete_select(By.ID, "ToServiceNetworkId-select", "BHIWANDI")
        self.autocomplete_select(By.ID, "VehicleId-select", "MH18AC0358")

        # Consignor/Consignee Details
        self.autocomplete_select(By.ID, "ConsignorId-select", "Adani Wilmar")
        self.autocomplete_select(By.ID, "ConsigneeId-select", "Food Corp")

        # Item Details
        self.autocomplete_select(By.ID, "ItemId-select", "Food Products")
        self.select_dropdown(By.ID, "PackingTypeId", "BAGS")
        self.send_keys(By.ID, "Packets", "1500")
        self.send_keys(By.ID, "UnitWeight", "6")
        self.send_keys(By.ID, "BasicFreight", "17000")
        self.click_element(By.ID, "btnSave-BookingItemSession633")
        time.sleep(1)
        self.click_element(By.ID, "RFRSGSTDetails")

        # Invoice Details
        self.send_keys(By.ID, "InvoiceNo", "1")
        self.send_keys(By.ID, "InvoiceDate", "02-06-2024")
        self.send_keys(By.ID, "InvoiceValue", "1")
        self.click_element(By.ID, "btnSave-BookingInvoiceSession633")
        time.sleep(1)

        # Submit Details
        self.click_element(By.ID, "mysubmit")
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

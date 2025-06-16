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

# Paid Freight Receivable Document Mapping error = Add Cr and Dr for Booking(Sundry Debtors)


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
        """Send keys after checking visibility"""
        for attempt in range(3):
            try:
                print(f"[INFO] Attempt {attempt + 1}: Entering text...")
                element = self.wait.until(EC.visibility_of_element_located((by, value)))
                element.clear()
                element.send_keys(text)
                print("Sent keys", text)
                return True
            except (
                ex.NoSuchElementException,
                ex.UnexpectedAlertPresentException,
                ex.TimeoutException,
                ex.StaleElementReferenceException,
            ) as e:
                print(f"[WARNING]Error : {type(e)} occurred. Retrying...")
                time.sleep(1)
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

    def auto_select(self, by, value, text):
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

    def handle_alert(self):
        """Check for an alert and handle it if present."""
        try:
            time.sleep(2)  # Small delay to allow alert to appear
            alert = self.driver.switch_to.alert
            print(f"[ALERT] Detected: {alert.text}")
            alert.accept()
            print("[ALERT] Alert accepted.")
            return True
        except ex.NoAlertPresentException:
            print("[INFO] No alert found. Continuing execution...")
            return False

    def test_booking(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript?ccode=UATASCRIPT")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "admin")
        self.send_keys(By.ID, "Password", "Omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        for i in (
            "Transportation",
            "Transportation Transaction »",
            "Booking »",
            "Local Collection Voucher (PRS)",
        ):
            self.click_element(By.LINK_TEXT, i)
            print(f"Navigated to {i}.")

        if self.switch_frames("btn_NewRecord"):
            self.click_element(By.ID, "btn_NewRecord")

        # Document Details
        if self.switch_frames("OrganizationId"):
            self.select_dropdown(By.ID, "OrganizationId", "AHMEDABAD")
            self.select_dropdown(By.ID, "SeriesId", "AHMEDABAD - 101 To 500")
            # Calendor
            self.click_element(By.CLASS_NAME, "ui-datepicker-trigger")
            self.select_dropdown(By.CLASS_NAME, "ui-datepicker-month", "Jun")
            self.select_dropdown(By.CLASS_NAME, "ui-datepicker-year", "2024")
            self.click_element(By.XPATH, "//a[text()='11']")

        # Booking Details
        self.auto_select(By.ID, "VehicleId-select", "MHO4ER9009")
        self.auto_select(By.ID, "StartLocationId-select", "MUMBAI")
        self.auto_select(By.ID, "EndLocationId-select", "AHMEDABAD")
        time.sleep(2)

        # Hire Details
        self.send_keys(By.ID, "DriverName", "Ram")
        self.send_keys(By.ID, "LicenseExpDate", "31-12-2027")
        self.send_keys(By.ID, "LicenseNo", "98765")
        self.send_keys(By.ID, "ContactNo", "9863575754")

        # Pick Booking
        self.select_dropdown(By.ID, "ddlSearchOn", "Document Print No")
        self.send_keys(By.ID, "DocumentSearchSession665DocumentNo", "AHM-000107-BKG")
        self.click_element(By.ID, "btn_Search")

        # Hire Charges Details
        self.select_dropdown(By.ID, "FreightUnitId", "Fixed")
        time.sleep(2)
        self.send_keys(By.ID, "FreightRate", "240")
        self.click_element(By.ID, "FreightUnitId")
        time.sleep(2)
        self.handle_alert()

        if self.switch_frames("OrganizationalLocationId-select"):
            self.auto_select(By.ID, "OrganizationalLocationId-select", "AHMEDABAD")
            self.send_keys(By.ID, "AdvanceAmount", "240")
            self.click_element(
                By.ID, "btnSave-VehicleTripAdvanceVehicleTripSessionName665"
            )
            time.sleep(1)

        # Submit Details
        self.click_element(By.ID, "mysubmit")
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

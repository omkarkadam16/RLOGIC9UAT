from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import unittest, time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager


class Contract(unittest.TestCase):
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
                    f"Retrying click on {by} with value {value}, attempt {i + 1}/{retry}"
                )
                time.sleep(1)
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except ex.ElementClickInterceptedException:
            return False

    def send_keys(self, by, value, text):
        try:
            element = self.wait.until(EC.visibility_of_element_located((by, value)))
            element.clear()
            element.send_keys(text)
            print("Sent keys", text)
            return True
        except ex.NoSuchElementException:
            print(f"Element not found: {value}")
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

    def test_Contract_Master(self):
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
            "Contract »",
            "Customer Contract",
        ):
            self.click_element(By.LINK_TEXT, i)
            print(f"Navigated to {i}.")

        if self.switch_frames("btn_NewRecord"):
            self.click_element(By.ID, "btn_NewRecord")

            # Document Details
            if self.switch_frames("OrganizationId"):
                self.select_dropdown(By.ID, "OrganizationId", "DELHI")
                # Calendar
                self.click_element(By.CLASS_NAME, "ui-datepicker-trigger")
                self.select_dropdown(By.CLASS_NAME, "ui-datepicker-month", "Apr")
                self.select_dropdown(By.CLASS_NAME, "ui-datepicker-year", "2025")
                self.click_element(By.XPATH, "//a[text()='6']")

                # Basic Information
                self.send_keys(By.ID, "ContractNo", "Bharat - 001")
                self.autocomplete_select(By.ID, "ClientId-select", "Bharat Earth")
                self.autocomplete_select(
                    By.ID, "ContractLocationId-select", "Head Office"
                )
                self.send_keys(By.ID, "FromDate", "06-04-2025")
                self.send_keys(By.ID, "ToDate", "06-04-2025")

                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(2)
                if self.switch_frames("ui-id-2"):
                    self.click_element(By.ID, "ui-id-2")

                # Freight Details
                if self.switch_frames("FreightOnId"):
                    self.select_dropdown(By.ID, "FreightOnId", "Fixed")
                    self.send_keys(By.ID, "Rate", "10000")
                    self.send_keys(By.ID, "MinimumValue", "10000")
                    self.send_keys(By.ID, "TransitDays", "3")

                # Charged Head Config
                if self.switch_frames("FormBookingType"):
                    self.select_dropdown(By.ID, "FormBookingType", "FTL")
                    self.select_dropdown(By.ID, "FormBookingMode", "Road")
                    self.select_dropdown(By.ID, "FormPaymentType", "To Be Billed")
                    self.autocomplete_select(By.ID, "FormFromLocation-select", "DELHI")
                    self.autocomplete_select(
                        By.ID, "FormToLocation-select", "AHMEDABAD"
                    )
                    self.select_dropdown(By.ID, "FormDeliveryType", "Door")
                    self.click_element(By.ID, "btnSave-ContractChargeHeadSession674")
                    time.sleep(2)

                if self.switch_frames("mysubmit"):
                    self.click_element(By.ID, "mysubmit")
                    print("Successfully submitted")
                    time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

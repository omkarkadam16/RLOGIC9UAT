import unittest
import time
import selenium.common.exceptions as ex
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class PurchaseOrder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

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
            print("Sent keys", text)
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

    def test_purchase_order(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        menus = ["Fleet", "Fleet Master »", "Tyre Movement »", "Tyre Inspection"]
        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)

            if self.switch_frames("btn_NewRecord"):
                self.click_element(By.ID, "btn_NewRecord")
                time.sleep(2)

                if self.switch_frames("OrganizationId"):
                    self.select_dropdown(By.ID, "OrganizationId", "HYDERABAD")
                    # Calendar
                    self.click_element(By.CLASS_NAME, "ui-datepicker-trigger")
                    self.select_dropdown(By.CLASS_NAME, "ui-datepicker-month", "Feb")
                    self.select_dropdown(By.CLASS_NAME, "ui-datepicker-year", "2025")
                    self.click_element(By.XPATH, "//a[text()='1']")

                # Vehicle Info
                if self.switch_frames("VehicleId-select"):
                    self.autocomplete_select(By.ID, "VehicleId-select", "MH04TT9008")
                    self.autocomplete_select(
                        By.ID, "InspectLocationId-select", "HYDERABAD"
                    )
                    self.send_keys(By.ID, "VehicleOdometer", "1000")
                    time.sleep(1)
                    self.select_dropdown(By.ID, "PlaceOfSupplyId", "MAHARASHTRA")
                    time.sleep(1)

                # Endu-001 Tyre Details
                if self.switch_frames("NsdValue1TyreInspectionSession1"):
                    self.send_keys(By.ID, "NsdValue1TyreInspectionSession1", "14.9")
                    self.send_keys(By.ID, "NsdValue2TyreInspectionSession1", "14.3")
                    self.send_keys(By.ID, "NsdValue3TyreInspectionSession1", "13.5")
                    self.send_keys(By.ID, "NsdValue4TyreInspectionSession1", "13.7")

                # Endu-002 Tyre Details
                if self.switch_frames("NsdValue1TyreInspectionSession2"):
                    self.send_keys(By.ID, "NsdValue1TyreInspectionSession2", "14.2")
                    self.send_keys(By.ID, "NsdValue2TyreInspectionSession2", "14.4")
                    self.send_keys(By.ID, "NsdValue3TyreInspectionSession2", "13.7")
                    self.send_keys(By.ID, "NsdValue4TyreInspectionSession2", "13.3")

                # Endu-003 Tyre Details
                if self.switch_frames("NsdValue1TyreInspectionSession3"):
                    self.send_keys(By.ID, "NsdValue1TyreInspectionSession3", "14.4")
                    self.send_keys(By.ID, "NsdValue2TyreInspectionSession3", "14.6")
                    self.send_keys(By.ID, "NsdValue3TyreInspectionSession3", "13.7")
                    self.send_keys(By.ID, "NsdValue4TyreInspectionSession3", "13.3")

                # Endu-004 Tyre Details
                if self.switch_frames("NsdValue1TyreInspectionSession4"):
                    self.send_keys(By.ID, "NsdValue1TyreInspectionSession4", "14.9")
                    self.send_keys(By.ID, "NsdValue2TyreInspectionSession4", "14.4")
                    self.send_keys(By.ID, "NsdValue3TyreInspectionSession4", "13.6")
                    self.send_keys(By.ID, "NsdValue4TyreInspectionSession4", "13.5")

                # Endu-005 Tyre Details
                if self.switch_frames("NsdValue1TyreInspectionSession5"):
                    self.send_keys(By.ID, "NsdValue1TyreInspectionSession5", "14.4")
                    self.send_keys(By.ID, "NsdValue2TyreInspectionSession5", "14.6")
                    self.send_keys(By.ID, "NsdValue3TyreInspectionSession5", "13.4")
                    self.send_keys(By.ID, "NsdValue4TyreInspectionSession5", "13.7")

                # Endu-006 Tyre Details
                if self.switch_frames("NsdValue1TyreInspectionSession6"):
                    self.send_keys(By.ID, "NsdValue1TyreInspectionSession6", "14.2")
                    self.send_keys(By.ID, "NsdValue2TyreInspectionSession6", "14.6")
                    self.send_keys(By.ID, "NsdValue3TyreInspectionSession6", "13.4")
                    self.send_keys(By.ID, "NsdValue4TyreInspectionSession6", "13.8")

                if self.switch_frames("mysubmit"):
                    self.click_element(By.ID, "mysubmit")
                    time.sleep(2)
                    time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

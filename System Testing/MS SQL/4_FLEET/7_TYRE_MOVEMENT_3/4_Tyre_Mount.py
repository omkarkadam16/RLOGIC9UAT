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


class ProductParameter(unittest.TestCase):
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
            element.is_enabled()
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

    def autocomplete_select(self, by, value, text, retries=2):
        input_text = self.wait.until(EC.visibility_of_element_located((by, value)))
        input_text.clear()
        input_text.send_keys(text)
        time.sleep(1)
        for attempt in range(retries + 1):
            try:
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
                break  # Exit loop if suggestions loaded but no match found
            except ex.StaleElementReferenceException:
                print(f"Retrying autocomplete fetch (attempt {attempt + 1})...")
                input_text.clear()
                input_text.send_keys(text)

        input_text.send_keys(Keys.DOWN)
        input_text.send_keys(Keys.ENTER)
        print("Selected autocomplete option using keyboard:", text)

    def tyre_mount(self,value,tyre):
        self.click_element(By.XPATH, value)
        time.sleep(1)
        if self.switch_frames("FromStorageHouseId"):
            self.select_dropdown(By.ID, "FromStorageHouseId", "AHMEDABAD")
            self.autocomplete_select(
                By.ID, "TyreSerialNo-select", tyre
            )
            self.click_element(By.ID, "Remarks")
            time.sleep(2)
            self.click_element(By.ID, "btnSave-TyreMountSession")
        time.sleep(1)

    def test_product_parameter(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        menus = ["Fleet", "Fleet Master »", "Tyre Movement »", "Tyre Mount"]
        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)

            if self.switch_frames("btn_NewRecord"):
                self.click_element(By.ID, "btn_NewRecord")
                time.sleep(2)

            if self.switch_frames("OrganizationId"):
                self.select_dropdown(By.ID, "OrganizationId", "AHMEDABAD")

                # Driver Info
                if self.switch_frames("VehicleId-select"):
                    self.autocomplete_select(By.ID, "VehicleId-select", "MH12XB2005")
                    self.click_element(By.ID, "WorkDoneBy")

                    # Tyre RO1
                    self.tyre_mount('//*[@id="SUR1"]/img', "MRF-001")

                    # Tyre RO2
                    self.tyre_mount('/html/body/div[2]/div[2]/form/div/div[1]/table[2]/tbody/tr/td[1]/table[3]/tbody/tr/td/table/tbody/tr/td[3]/a/img', "MRF-002")

                    # Tyre RO3
                    self.tyre_mount('//*[@id="DUR1"]/img', "MRF-003")

                    # Tyre RI3
                    self.tyre_mount('//*[@id="DUR2"]/img', "MRF-004")

                    # Tyre LO1
                    self.tyre_mount('//*[@id="SUL1"]/img', "MRF-005")

                    # Tyre LO2
                    self.tyre_mount('/html/body/div[2]/div[2]/form/div/div[1]/table[2]/tbody/tr/td[1]/table[3]/tbody/tr/td/table/tbody/tr/td[1]/a/img', "MRF-006")

                    # Tyre LO3
                    self.tyre_mount('//*[@id="DUL1"]/img', "MRF-007")

                    # Tyre LI3
                    self.tyre_mount('//*[@id="DUL2"]/img', "MRF-008")

            if self.switch_frames("mysubmit"):
                self.click_element(By.ID, "mysubmit")
                time.sleep(2)


if __name__ == "__main__":
    unittest.main()

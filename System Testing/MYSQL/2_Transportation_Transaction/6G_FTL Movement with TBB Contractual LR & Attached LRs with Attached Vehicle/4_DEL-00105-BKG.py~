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


class Booking2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait=WebDriverWait(cls.driver,15)

    def click_element(self,by,value,retry=2):
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by,value))).click()
                print("Clicked on element",value)
                return True
            except(ex.ElementClickInterceptedException,ex.StaleElementReferenceException,ex.TimeoutException):
                print(f'Retrying click on {by} with value {value}, attempt {i+1}/{retry}')
                time.sleep(1)
        try:
            element=self.driver.find_element(by,value)
            self.driver.execute_script("arguments[0].click();",element)
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

    def send_keys(self,by,value,text):
        try:
            element = self.wait.until(EC.visibility_of_element_located((by, value)))
            element.clear()
            element.send_keys(text)
            print(f'Sent keys {text} to {by} with value {value}')
            return True
        except ex.NoSuchElementException:
            print(f'Element not found: {value}')
            return False

    def select_dropdown(self,by,value,text):
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
        except (ex.NoSuchElementException, ex.ElementClickInterceptedException, ex.TimeoutException):
            return False

    def autocomplete_select(self,by,value,text):
        input_text=self.wait.until(EC.visibility_of_element_located((by,value)))
        input_text.clear()
        input_text.send_keys(text)
        time.sleep(1)
        suggest=self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"ui-menu-item")))
        for i in suggest:
            if text.upper() in i .text.upper():
                i.click()
                time.sleep(1)
                print("Selected autocomplete option:", text)
                return
        input_text.send_keys(Keys.DOWN)
        input_text.send_keys(Keys.ENTER)
        print("Selected autocomplete option using keyboard:", text)

    def test_booking2(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript?ccode=UATASCRIPT")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "admin")
        self.send_keys(By.ID, "Password", "Omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        for i in ("Transportation",
            "Transportation Transaction »",
            "Booking »",
            "Attach LR",):
            self.click_element(By.LINK_TEXT, i)
            print(f"Navigated to {i}.")

    #Attach LR
        if self.switch_frames("LocationId-select"):
            self.autocomplete_select(By.ID,"LocationId-select","DELHI")
            self.autocomplete_select(By.ID,"BookingId-select","DEL-000104-BKG")
            self.select_dropdown(By.ID,"SeriesId","DELHI - 101 To 500")
            self.click_element(By.ID,"btn_GetDocumentNoSearch")
            time.sleep(1)

            # Calendar
        if self.switch_frames("DocumentDate"):
            self.click_element(By.CLASS_NAME, "ui-datepicker-trigger")
            self.select_dropdown(By.CLASS_NAME, "ui-datepicker-month", "Jun")
            self.select_dropdown(By.CLASS_NAME, "ui-datepicker-year", "2024")
            self.click_element(By.XPATH, "//a[text()='1']")

        #Item Details
            self.autocomplete_select(By.ID, "ItemId-select", "Cotton")
            self.select_dropdown(By.ID, "PackingTypeId", "BOX")
            self.autocomplete_select(By.ID, "Packets", "1000")
            self.send_keys(By.ID, "UnitWeight", "7")
            self.click_element(By.ID, "btnSave-BookingItemSession633")
            time.sleep(1)
            self.click_element(By.ID, "RFRSGSTDetails")

        #Invoice Details
            self.send_keys(By.ID, "InvoiceNo", "1")
            self.send_keys(By.ID, "InvoiceDate", "01-06-2024")
            self.send_keys(By.ID, "InvoiceValue", "1")
            self.click_element(By.ID,"btnSave-BookingInvoiceSession633")
            time.sleep(1)

        #Submit Details
            self.click_element(By.ID, "mysubmit")
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()


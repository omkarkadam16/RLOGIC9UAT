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


class CustomerMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

    def click_element(self, by, value, retry=2):
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by, value))).click()
                return True
            except (
                ex.ElementClickInterceptedException,
                ex.StaleElementReferenceException,
                ex.TimeoutException,
            ):
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
            return True
        except ex.NoSuchElementException:
            return False

    def select_dropdown(self, by, value, text):
        try:
            e = self.wait.until(EC.element_to_be_clickable((by, value)))
            e.is_enabled()
            e.click()
            self.wait.until(EC.visibility_of_element_located((by, value)))
            element = Select(self.driver.find_element(by, value))
            element.select_by_visible_text(text)
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
                return
        input_text.send_keys(Keys.DOWN)
        input_text.send_keys(Keys.ENTER)

    def test_customer(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript?ccode=UATASCRIPT")

        self.send_keys(By.ID, "Login", "admin")
        self.send_keys(By.ID, "Password", "Omsgn9")
        self.click_element(By.ID, "btnLogin")

        menus = ["Transportation", "Transportation Master »", "Customer »", "Customer"]
        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)

        customers = [
            {
                "name": "Tata Steel Ltd",
                "pan": "AACCK5599T",
                "Executive": "Omkar Kadam",
                "city": "CHENNAI",
                "pincode": "400001",
                "phone": "1234567890",
                "state": "TAMIL NADU",
                "gst": "33AACCK5599TFZV",
            },
            {
                "name": "Tata Motors Ltd",
                "Executive": "Parth Patil",
                "pan": "AACCK9966T",
                "city": "Jaipur",
                "pincode": "380001",
                "phone": "8543216789",
                "state": "RAJASTHAN",
                "gst": "08AACCK9966TPZC",
            },
        ]

        for customer in customers:
            if self.switch_frames("btn_NewRecord"):
                self.click_element(By.ID, "btn_NewRecord")
                time.sleep(2)

            # Basic Information
            if self.switch_frames("Party_PartyName"):
                self.send_keys(By.ID, "Party_PartyName", customer["name"])
                self.select_dropdown(By.ID, "Party_PartyCategoryId", "GENERAL")
                self.select_dropdown(By.ID, "Party_PartyIndustryTypeId", "GENERAL")
                self.select_dropdown(By.ID, "Party_PartyGradeId", "A Class")
                self.select_dropdown(By.ID, "Party_PartyGroupId", "Tata Group")
                self.select_dropdown(
                    By.ID, "CollectionExecutiveId", customer["Executive"]
                )
            if self.switch_frames("EffectiveFromDate"):
                self.send_keys(By.ID, "EffectiveFromDate", "27-01-2025")
                self.send_keys(By.ID, "PANNo", customer["pan"])

            # Address Details
            if self.switch_frames("AddressTypeId"):
                self.select_dropdown(By.ID, "AddressTypeId", "Office")
                self.send_keys(By.ID, "AddressLine", "123 Main St")
                self.autocomplete_select(By.ID, "CityId-select", customer["city"])
                self.send_keys(By.ID, "PinCode", customer["pincode"])
                self.send_keys(By.ID, "ContactNo", customer["phone"])
                self.send_keys(By.ID, "Mob", "5564567890")
                self.click_element(By.ID, "btnSave-AddressSession77")

            # Registation Number Details
            if self.switch_frames("RegistrationHeadId"):
                self.select_dropdown(By.ID, "RegistrationHeadId", "PAN No.")
                self.send_keys(By.ID, "Number", customer["pan"])
                self.click_element(By.ID, "btnSave-RegistrationSession77")

            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            if self.switch_frames("liTab2"):
                self.click_element(By.ID, "liTab2")

            # Applicable Payment Types
            if self.switch_frames("PaymentTypeId"):
                for payment_type in ["Paid", "To Pay", "To Be Billed"]:
                    self.select_dropdown(By.ID, "PaymentTypeId", payment_type)
                    self.click_element(By.ID, "btnSave-PaymentTypeConfigSession77")
                    time.sleep(2)

            # Billing Details
            if self.switch_frames("BillingOn"):
                self.select_dropdown(By.ID, "BillingOn", "Booking")
                self.select_dropdown(By.ID, "BillingLocationTypeId", "Booking Branch")
                self.autocomplete_select(
                    By.ID, "CollectionLocationId-select", "AHMEDABAD"
                )
            if self.switch_frames("SubmissionLocationId-select"):
                self.autocomplete_select(By.ID, "SubmissionLocationId-select", "MUMBAI")
                self.send_keys(By.ID, "CreditDays", "20")
                self.send_keys(By.ID, "Party_CreditLimit", "20000000")

            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            if self.switch_frames("liTab5"):
                self.click_element(By.ID, "liTab5")

            # GST Registration
            if self.switch_frames("StateId"):
                self.select_dropdown(By.ID, "StateId", customer["state"])
                self.select_dropdown(By.ID, "BusinessVerticalId", "TRANSPORTATION")
                self.send_keys(By.ID, "GSTNumber", customer["gst"])
                self.click_element(By.ID, "btnSave-CustGSTRegistrationSession77")

            if self.switch_frames("mysubmit"):
                self.click_element(By.ID, "mysubmit")
                print("Successfully submitted", customer["name"])
                time.sleep(2)

        print("All customers created successfully.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

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


class VendorMaster(unittest.TestCase):
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

    def dropdown_select(self, by, value, text):
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
            ex.StaleElementReferenceException,
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

    def test_vendor(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript?ccode=UATASCRIPT")

        self.send_keys(By.ID, "Login", "admin")
        self.send_keys(By.ID, "Password", "Omsgn9")
        self.click_element(By.ID, "btnLogin")

        menus = ["Transportation", "Transportation Master »", "Vendor »", "Vendor"]
        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)

        Vendor = [
            {
                "name": "BHORUKA LOGISTICS PVT LTD",
                "category": "VEHICLE OWNER",
                "pan": "DDCCK5575Y",
                "city": "Delhi",
                "pincode": "400001",
                "phone": "1234567890",
                "state": "DELHI",
                "gst": "07DDCCK5575YPZD",
            },
            {
                "name": "BAJAJ CORPORATION PVT LTD",
                "category": "VEHICLE OWNER",
                "pan": "DDCCK5575P",
                "city": "Delhi",
                "pincode": "400001",
                "phone": "1234567890",
                "state": "DELHI",
                "gst": "07DDCCK5575PUZD",
            },
            {
                "name": "INTER INDIA ROADWAYS LTD",
                "category": "VEHICLE OWNER",
                "pan": "AACCK5599U",
                "city": "THANE",
                "pincode": "380001",
                "phone": "8543216789",
                "state": "MAHARASHTRA",
                "gst": "27AACCK5599UPZH",
            },
            {
                "name": "VIJAY ENTERPRISES",
                "category": "VEHICLE BROKER",
                "pan": "AACCK5599M",
                "city": "MUMBAI",
                "pincode": "380001",
                "phone": "8543216789",
                "state": "MAHARASHTRA",
                "gst": "27AACCK5599MUZF",
            },
            {
                "name": "IOCL FUEL PUMP",
                "category": "FUEL PUMP VENDOR",
                "pan": "AACCK5597F",
                "city": "NASHIK",
                "pincode": "400001",
                "phone": "1234567890",
                "state": "MAHARASHTRA",
                "gst": "27AACCK5597F6ZF",
            },
            {
                "name": "AKIL KHAN SO HABIB KHAN",
                "category": "VEHICLE BROKER",
                "pan": "BLCPK9405R",
                "city": "VIJAYAWADA",
                "pincode": "380001",
                "phone": "8543216789",
                "state": "ANDHRA PRADESH",
                "gst": "37BLCPK9405R6ZS",
            },
            {
                "name": "BHAGAT SINGH",
                "category": "VEHICLE OWNER",
                "pan": "CGTPS9629G",
                "city": "LUDHIANA",
                "pincode": "380001",
                "phone": "8543216789",
                "state": "PUNJAB",
                "gst": "03CGTPS9629G9ZV",
            },
            {
                "name": "DARSHAN SINGH",
                "category": "VEHICLE OWNER",
                "pan": "CETPS9996J",
                "city": "JALGAON",
                "pincode": "380001",
                "phone": "8543216789",
                "state": "MAHARASHTRA",
                "gst": "27CETPS9996J6ZU",
            },
        ]

        for i in Vendor:
            if self.switch_frames("btn_NewRecord"):
                self.click_element(By.ID, "btn_NewRecord")
                time.sleep(2)

            # Basic Information
            if self.switch_frames("Party_PartyName"):
                self.send_keys(By.ID, "Party_PartyName", i["name"])
                self.dropdown_select(By.ID, "Party_PartyCategoryId", i["category"])
                self.dropdown_select(By.ID, "Party_TdsDeducteeTypeId", "Person")
            if self.switch_frames("EffectiveFromDate"):
                self.send_keys(By.ID, "EffectiveFromDate", "27-01-2025")
                self.send_keys(By.ID, "PANNo", i["pan"])

            # Address Details
            if self.switch_frames("AddressTypeId"):
                self.dropdown_select(By.ID, "AddressTypeId", "Office")
                self.send_keys(By.ID, "AddressLine", "123 Main St")
                self.autocomplete_select(By.ID, "CityId-select", i["city"])
                self.send_keys(By.ID, "PinCode", i["pincode"])
                self.send_keys(By.ID, "ContactNo", i["phone"])
                self.send_keys(By.ID, "Mob", "5564567890")
                self.click_element(By.ID, "btnSave-AddressSession29")

            # Party GST Percent
            if self.switch_frames("GSTStatusId"):
                self.dropdown_select(By.ID, "GSTStatusId", "Registered")
                self.send_keys(By.ID, "GSTFromDate", "27-01-2018")
                self.click_element(By.ID, "btnSave-PartyGSTPercentSession29")

            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            if self.switch_frames("liTab5"):
                self.click_element(By.ID, "liTab5")

            # GST Registration
            if self.switch_frames("StateId"):
                self.dropdown_select(By.ID, "StateId", i["state"])
                self.dropdown_select(By.ID, "BusinessVerticalId", "TRANSPORTATION")
                self.send_keys(By.ID, "GSTNumber", i["gst"])
                self.click_element(By.ID, "btnSave-CustGSTRegistrationSession29")
                time.sleep(2)

            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            if self.switch_frames("liTab6"):
                self.click_element(By.ID, "liTab6")

            if self.switch_frames("VehicleGroupId"):
                self.dropdown_select(By.ID, "VehicleGroupId", "CONTAINER BODY")
                self.click_element(By.ID, "btnSave-VendorRouteConfigVTSession")
                self.dropdown_select(By.ID, "VehicleGroupId", "FULL BODY")
                self.click_element(By.ID, "btnSave-VendorRouteConfigVTSession")
                time.sleep(2)

                self.dropdown_select(By.ID, "FromZoneId", "EAST")
                self.dropdown_select(By.ID, "ToZoneId", "WEST")
                self.click_element(By.ID, "btnSave-VendorRouteConfigVTRouteSession")

            # Route Config

            if self.switch_frames("mysubmit"):
                self.click_element(By.ID, "mysubmit")
                print("Successfully submitted", i["name"])
                time.sleep(2)

        print("All Vendors created successfully.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

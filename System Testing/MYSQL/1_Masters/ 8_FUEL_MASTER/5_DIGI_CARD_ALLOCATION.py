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


class DigiCardAllocation(unittest.TestCase):
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

    def test_DigiCardAllocation(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript?ccode=UATASCRIPT")

        self.send_keys(By.ID, "Login", "admin")
        self.send_keys(By.ID, "Password", "Omsgn9")
        self.click_element(By.ID, "btnLogin")

        menus = ["Fleet", "Fleet Master »", "Fuel »", "DigiCard Allocation"]
        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)

        Series = [
            {
                "DigiCardNo": "F-9211",
                "DigiCardAllocationType": "Vehicle",
                "VehicleId": "MH04AA7007",
            },
            {
                "DigiCardNo": "F-9212",
                "DigiCardAllocationType": "Vendor",
                "VendorId": "IOCL FUEL PUMP",
            },
            {
                "DigiCardNo": "F-9213",
                "DigiCardAllocationType": "Location",
                "LocationId": "HYDERABAD",
            },
            {
                "DigiCardNo": "T-9214",
                "DigiCardAllocationType": "Vehicle",
                "VehicleId": "MH04AA7007",
            },
            {
                "DigiCardNo": "T-9215",
                "DigiCardAllocationType": "Vehicle",
                "VehicleId": "MH04TT9008",
            },
            {
                "DigiCardNo": "T-9216",
                "DigiCardAllocationType": "Vehicle",
                "VehicleId": "MH04AA0099",
            },
            {
                "DigiCardNo": "D-9217",
                "DigiCardAllocationType": "Vehicle",
                "VehicleId": "MH06RR1006",
            },
            {
                "DigiCardNo": "D-9218",
                "DigiCardAllocationType": "Location",
                "LocationId": "PUNE",
            },
            {
                "DigiCardNo": "D-9219",
                "DigiCardAllocationType": "Location",
                "LocationId": "DELHI",
            },
        ]

        # Iterate over each location and create it
        for i in Series:
            if self.switch_frames("btn_NewRecord"):
                self.click_element(By.ID, "btn_NewRecord")

            # General Details
            if self.switch_frames("DigiCardId-select"):
                self.autocomplete_select(By.ID, "DigiCardId-select", i["DigiCardNo"])
                self.select_dropdown(
                    By.ID, "DigiCardAllocationTypeId", i["DigiCardAllocationType"]
                )

                # Handle fields dynamically based on allocation type
                if i["DigiCardAllocationType"] == "Vehicle":
                    vehicle = i.get("VehicleId")
                    if vehicle:
                        self.autocomplete_select(By.ID, "VehicleId-select", vehicle)

                elif i["DigiCardAllocationType"] == "Vendor":
                    vendor = i.get("VendorId")
                    if vendor:
                        self.autocomplete_select(By.ID, "VendorId-select", vendor)

                elif i["DigiCardAllocationType"] == "Location":
                    location = i.get("LocationId")
                    if location:
                        self.autocomplete_select(By.ID, "LocationId-select", location)

                self.send_keys(By.ID, "EffectiveFrom", "01-04-2018")

            if self.switch_frames("mysubmit"):
                self.click_element(By.ID, "mysubmit")
                print("DigiCardNo Successfully submitted", i["DigiCardNo"])
                time.sleep(2)
        print("All data created successfully.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

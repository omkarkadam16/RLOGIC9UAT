import logging
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


class OrgLocation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("OrgLocation_log.log"),
                logging.StreamHandler(),
            ],
        )

        logging.info("Setting up the WebDriver.")
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)
        logging.info("WebDriver setup completed.")

    def click_element(self, by, value, retry=2):
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by, value))).click()
                logging.info(f"Clicked on element: {value}")
                return True
            except (
                ex.ElementClickInterceptedException,
                ex.StaleElementReferenceException,
                ex.TimeoutException,
            ):
                logging.error(f"Error clicking element: {value}. Error: {str(ex)}")
                time.sleep(1)
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
            logging.info(f"JS clicked on element: {value}")
            return True
        except ex.StaleElementReferenceException:
            logging.error(f"Error JS clicking element: {value}. Error: {str(ex)}")
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
                logging.error(f"Error finding element: {element_id}. Error: {str(ex)}")
                driver.switch_to.default_content()
        return False

    def send_keys(self, by, value, text):
        try:
            element = self.wait.until(EC.visibility_of_element_located((by, value)))
            element.is_enabled()
            element.clear()
            element.send_keys(text)
            logging.info(f"Sent keys to element: {value}")
            return True
        except ex.NoSuchElementException:
            logging.error(f"Error sending keys to element: {value}. Error: {str(ex)}")
            return False

    def select_dropdown(self, by, value, text):
        try:
            e = self.wait.until(EC.element_to_be_clickable((by, value)))
            e.is_enabled()
            e.click()
            self.wait.until(EC.visibility_of_element_located((by, value)))
            element = Select(self.driver.find_element(by, value))
            element.select_by_visible_text(text)
            logging.info(f"Selected dropdown option: {text}")
            return True
        except (
            ex.NoSuchElementException,
            ex.ElementClickInterceptedException,
            ex.TimeoutException,
        ):
            logging.error(f"Error selecting dropdown option: {text}. Error: {str(ex)}")
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
                logging.info(f"Selected autocomplete option: {text}")
                return
        input_text.send_keys(Keys.DOWN)
        input_text.send_keys(Keys.ENTER)
        logging.info(f"Selected autocomplete option: {text}")

    def test_OrgLocation(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript?ccode=UATASCRIPT")

        logging.info("Logging in...")
        self.send_keys(By.ID, "Login", "admin")
        self.send_keys(By.ID, "Password", "Omsgn9")
        self.click_element(By.ID, "btnLogin")
        logging.info("Logged in.")

        for i in (
            "Common",
            "Organisational Hierarchy »",
            "Organisation Location",
        ):
            self.click_element(By.LINK_TEXT, i)
            logging.info(f"Navigated to {i}.")

            # List of multiple locations
            locations = [
                {
                    "Code": "MUM",
                    "OrganizationLocationName": "MUMBAI",
                    "LocationType": "BRANCH OFFICE",
                    "ParentLocation": "Head Office",
                    "AddressType": "Office",
                    "AddressLine": "ABC Street 1",
                    "City": "MUMBAI",
                    "PinCode": "411001",
                    "ContactNo": "1234567891",
                    "Mobile": "9876543211",
                },
                {
                    "Code": "BWD",
                    "OrganizationLocationName": "BHIWANDI",
                    "LocationType": "BRANCH OFFICE",
                    "ParentLocation": "Head Office",
                    "AddressType": "Office",
                    "AddressLine": "ABC Street 1",
                    "City": "THANE",
                    "PinCode": "422001",
                    "ContactNo": "1234567892",
                    "Mobile": "9876543212",
                },
                {
                    "Code": "PUN",
                    "OrganizationLocationName": "PUNE",
                    "LocationType": "BRANCH OFFICE",
                    "ParentLocation": "Head Office",
                    "AddressType": "Office",
                    "AddressLine": "ABC Street 1",
                    "City": "PUNE",
                    "PinCode": "400001",
                    "ContactNo": "1234567893",
                    "Mobile": "9876543213",
                },
                {
                    "Code": "JPR",
                    "OrganizationLocationName": "JAIPUR",
                    "LocationType": "BRANCH OFFICE",
                    "ParentLocation": "Head Office",
                    "AddressType": "Office",
                    "AddressLine": "ABC Street 1",
                    "City": "Jaipur",
                    "PinCode": "400001",
                    "ContactNo": "1234567893",
                    "Mobile": "9876543213",
                },
                {
                    "Code": "AHM",
                    "OrganizationLocationName": "AHMEDABAD",
                    "LocationType": "BRANCH OFFICE",
                    "ParentLocation": "Head Office",
                    "AddressType": "Office",
                    "AddressLine": "ABC Street 1",
                    "City": "AHMEDABAD",
                    "PinCode": "400001",
                    "ContactNo": "1234567893",
                    "Mobile": "9876543213",
                },
                {
                    "Code": "HYD",
                    "OrganizationLocationName": "HYDERABAD",
                    "LocationType": "BRANCH OFFICE",
                    "ParentLocation": "Head Office",
                    "AddressType": "Office",
                    "AddressLine": "ABC Street 1",
                    "City": "HYDERABAD",
                    "PinCode": "400001",
                    "ContactNo": "1234567893",
                    "Mobile": "9876543213",
                },
                {
                    "Code": "DEL",
                    "OrganizationLocationName": "DELHI",
                    "LocationType": "BRANCH OFFICE",
                    "ParentLocation": "Head Office",
                    "AddressType": "Office",
                    "AddressLine": "ABC Street 1",
                    "City": "DELHI",
                    "PinCode": "400001",
                    "ContactNo": "1234567893",
                    "Mobile": "9876543213",
                },
            ]

            # Iterate over each location and create it
            for location in locations:
                if self.switch_frames("btn_NewRecord"):
                    self.click_element(By.ID, "btn_NewRecord")

                # Fill out the form
                if self.switch_frames("Code"):
                    self.send_keys(By.ID, "Code", location["Code"])
                    self.send_keys(
                        By.ID,
                        "OrganizationLocationName",
                        location["OrganizationLocationName"],
                    )
                    self.select_dropdown(
                        By.ID, "LocationTypeId", location["LocationType"]
                    )
                    if location["ParentLocation"] != "None":
                        self.select_dropdown(
                            By.ID,
                            "ParentOrganizationLocationId",
                            location["ParentLocation"],
                        )
                    self.select_dropdown(
                        By.ID, "AddressTypeId", location["AddressType"]
                    )
                    self.send_keys(By.ID, "AddressLine", location["AddressLine"])
                    self.autocomplete_select(By.ID, "CityId-select", location["City"])
                    self.send_keys(By.ID, "PinCode", location["PinCode"])
                    self.send_keys(By.ID, "ContactNo", location["ContactNo"])
                    self.send_keys(By.ID, "Mob", location["Mobile"])

                # Submit the form
                if self.switch_frames("mysubmit"):
                    self.click_element(By.ID, "mysubmit")
                    logging.info(
                        f"Location {location['OrganizationLocationName']} created successfully."
                    )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=False)

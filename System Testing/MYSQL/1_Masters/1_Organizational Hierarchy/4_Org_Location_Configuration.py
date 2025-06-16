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


class Location(unittest.TestCase):
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
                    f"Retrying click on {by} with value {value}, attempt {i+1}/{retry}"
                )
                time.sleep(1)
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
            print("Clicked on element using JavaScript")
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
                time.sleep(1)
                print("Selected autocomplete option:", text)
                return
        input_text.send_keys(Keys.DOWN)
        input_text.send_keys(Keys.ENTER)
        print("Selected autocomplete option using keyboard:", text)

    def test_Location(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript?ccode=UATASCRIPT")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "admin")
        self.send_keys(By.ID, "Password", "Omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        for i in (
            "Common",
            "Organisational Hierarchy »",
            "Org Location Configuration",
        ):
            self.click_element(By.LINK_TEXT, i)
            print(f"Navigated to {i}.")

            # List of multiple locations
            locations = [
                {
                    "OrganizationLocation": "MUMBAI",
                    "B1": "Booking",
                    "B2": "01-01-2020",
                    "B3": "31-03-2030",
                    "D1": "Delivery",
                    "D2": "01-01-2020",
                    "D3": "31-03-2030",
                    "T1": "Transhipment",
                    "T2": "01-01-2020",
                    "T3": "31-03-2030",
                    "P1": "Paid",
                    "P2": "To Pay",
                    "P3": "To Be Billed",
                    "P4": "FOC",
                },
                {
                    "OrganizationLocation": "BHIWANDI",
                    "B1": "Booking",
                    "B2": "01-01-2020",
                    "B3": "31-03-2030",
                    "D1": "Delivery",
                    "D2": "01-01-2020",
                    "D3": "31-03-2030",
                    "T1": "Transhipment",
                    "T2": "01-01-2020",
                    "T3": "31-03-2030",
                    "P1": "Paid",
                    "P2": "To Pay",
                    "P3": "To Be Billed",
                    "P4": "FOC",
                },
                {
                    "OrganizationLocation": "PUNE",
                    "B1": "Booking",
                    "B2": "01-01-2020",
                    "B3": "31-03-2030",
                    "D1": "Delivery",
                    "D2": "01-01-2020",
                    "D3": "31-03-2030",
                    "T1": "Transhipment",
                    "T2": "01-01-2020",
                    "T3": "31-03-2030",
                    "P1": "Paid",
                    "P2": "To Pay",
                    "P3": "To Be Billed",
                    "P4": "FOC",
                },
                {
                    "OrganizationLocation": "JAIPUR",
                    "B1": "Booking",
                    "B2": "01-01-2020",
                    "B3": "31-03-2030",
                    "D1": "Delivery",
                    "D2": "01-01-2020",
                    "D3": "31-03-2030",
                    "T1": "Transhipment",
                    "T2": "01-01-2020",
                    "T3": "31-03-2030",
                    "P1": "Paid",
                    "P2": "To Pay",
                    "P3": "To Be Billed",
                    "P4": "FOC",
                },
                {
                    "OrganizationLocation": "AHMEDABAD",
                    "B1": "Booking",
                    "B2": "01-01-2020",
                    "B3": "31-03-2030",
                    "D1": "Delivery",
                    "D2": "01-01-2020",
                    "D3": "31-03-2030",
                    "T1": "Transhipment",
                    "T2": "01-01-2020",
                    "T3": "31-03-2030",
                    "P1": "Paid",
                    "P2": "To Pay",
                    "P3": "To Be Billed",
                    "P4": "FOC",
                },
                {
                    "OrganizationLocation": "HYDERABAD",
                    "B1": "Booking",
                    "B2": "01-01-2020",
                    "B3": "31-03-2030",
                    "D1": "Delivery",
                    "D2": "01-01-2020",
                    "D3": "31-03-2030",
                    "T1": "Transhipment",
                    "T2": "01-01-2020",
                    "T3": "31-03-2030",
                    "P1": "Paid",
                    "P2": "To Pay",
                    "P3": "To Be Billed",
                    "P4": "FOC",
                },
                {
                    "OrganizationLocation": "NAMPALLI",
                    "B1": "Booking",
                    "B2": "01-01-2020",
                    "B3": "31-03-2030",
                    "D1": "Delivery",
                    "D2": "01-01-2020",
                    "D3": "31-03-2030",
                    "T1": "Transhipment",
                    "T2": "01-01-2020",
                    "T3": "31-03-2030",
                    "P1": "Paid",
                    "P2": "To Pay",
                    "P3": "To Be Billed",
                    "P4": "FOC",
                },
                {
                    "OrganizationLocation": "SECUNDERABAD",
                    "B1": "Booking",
                    "B2": "01-01-2020",
                    "B3": "31-03-2030",
                    "D1": "Delivery",
                    "D2": "01-01-2020",
                    "D3": "31-03-2030",
                    "T1": "Transhipment",
                    "T2": "01-01-2020",
                    "T3": "31-03-2030",
                    "P1": "Paid",
                    "P2": "To Pay",
                    "P3": "To Be Billed",
                    "P4": "FOC",
                },
                {
                    "OrganizationLocation": "DELHI",
                    "B1": "Booking",
                    "B2": "01-01-2020",
                    "B3": "31-03-2030",
                    "D1": "Delivery",
                    "D2": "01-01-2020",
                    "D3": "31-03-2030",
                    "T1": "Transhipment",
                    "T2": "01-01-2020",
                    "T3": "31-03-2030",
                    "P1": "Paid",
                    "P2": "To Pay",
                    "P3": "To Be Billed",
                    "P4": "FOC",
                },
            ]

            # Iterate over each location and create it
            for location in locations:
                if self.switch_frames("btn_NewRecord"):
                    self.click_element(By.ID, "btn_NewRecord")

                # Fill out the form
                if self.switch_frames("OrganizationLocationId-select"):
                    self.autocomplete_select(
                        By.ID,
                        "OrganizationLocationId-select",
                        location["OrganizationLocation"],
                    )

                    # Applicable Service Head Type = Booking
                    self.select_dropdown(By.ID, "ServiceHeadId", location["B1"])
                    self.send_keys(By.ID, "EffectiveFromDate", location["B2"])
                    self.send_keys(By.ID, "ExpiryDate", location["B3"])
                    self.click_element(
                        By.ID, "btnSave-OrgLocationServiceHeadSession744"
                    )
                    time.sleep(1)

                    # Applicable Service Head Type = Delivery
                    self.select_dropdown(By.ID, "ServiceHeadId", location["D1"])
                    self.send_keys(By.ID, "EffectiveFromDate", location["D2"])
                    self.send_keys(By.ID, "ExpiryDate", location["D3"])
                    self.click_element(
                        By.ID, "btnSave-OrgLocationServiceHeadSession744"
                    )
                    time.sleep(1)

                    # Applicable Service Head Type = Transhipment
                    self.select_dropdown(By.ID, "ServiceHeadId", location["T1"])
                    self.send_keys(By.ID, "EffectiveFromDate", location["T2"])
                    self.send_keys(By.ID, "ExpiryDate", location["T3"])
                    self.click_element(
                        By.ID, "btnSave-OrgLocationServiceHeadSession744"
                    )
                    time.sleep(1)

                    # Payment Type Configuration = Paid
                    self.select_dropdown(By.ID, "PaymentTypeId", location["P1"])
                    self.click_element(By.ID, "btnSave-PaymentTypeConfigSession744")
                    time.sleep(1)
                    # Payment Type Configuration = To Pay
                    self.select_dropdown(By.ID, "PaymentTypeId", location["P2"])
                    self.click_element(By.ID, "btnSave-PaymentTypeConfigSession744")
                    time.sleep(1)
                    # Payment Type Configuration = To Be Billed
                    self.select_dropdown(By.ID, "PaymentTypeId", location["P3"])
                    self.click_element(By.ID, "btnSave-PaymentTypeConfigSession744")
                    time.sleep(1)
                    # Payment Type Configuration = FOC
                    self.select_dropdown(By.ID, "PaymentTypeId", location["P4"])
                    self.click_element(By.ID, "btnSave-PaymentTypeConfigSession744")
                    time.sleep(1)

                    # Submit the form
                    if self.switch_frames("mysubmit"):
                        self.click_element(By.ID, "mysubmit")
                        print(
                            f"Location {location['OrganizationLocation']} created successfully."
                        )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

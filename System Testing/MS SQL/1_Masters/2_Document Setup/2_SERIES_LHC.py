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


class SeriesLHC(unittest.TestCase):
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

    def test_SeriesLHC(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        for i in (
            "Common",
            "Document Setup »",
            "Series",
        ):
            self.click_element(By.LINK_TEXT, i)
            print(f"Navigated to {i}.")

        Series = [
            {
                "Document": "VehicleTrip",
                "OrganizationLocation": "MUMBAI",
                "StartNo": "101",
                "EndNo": "500",
                "Prefix": "MUM",
                "Suffix": "LHC",
                "SeriesName": "MUMBAI - 101 To 500 - LHC",
                "Seperator": "-",
                "DocumentNoLength": "6",
                "YearCode": "2025 - 2025",
            },
            {
                "Document": "VehicleTrip",
                "OrganizationLocation": "MUMBAI",
                "StartNo": "501",
                "EndNo": "1000",
                "Prefix": "MUM",
                "Suffix": "LHC",
                "SeriesName": "MUMBAI - 501 To 1000 - LHC",
                "Seperator": "-",
                "DocumentNoLength": "6",
                "YearCode": "2025 - 2025",
            },
            {
                "Document": "VehicleTrip",
                "OrganizationLocation": "BHIWANDI",
                "StartNo": "101",
                "EndNo": "500",
                "Prefix": "BWD",
                "Suffix": "LHC",
                "SeriesName": "BHIWANDI - 101 To 500 - LHC",
                "Seperator": "-",
                "DocumentNoLength": "6",
                "YearCode": "2025 - 2025",
            },
            {
                "Document": "VehicleTrip",
                "OrganizationLocation": "BHIWANDI",
                "StartNo": "501",
                "EndNo": "1000",
                "Prefix": "BWD",
                "Suffix": "LHC",
                "SeriesName": "BHIWANDI - 501 To 1000 - LHC",
                "Seperator": "-",
                "DocumentNoLength": "6",
                "YearCode": "2025 - 2025",
            },
            {
                "Document": "VehicleTrip",
                "OrganizationLocation": "PUNE",
                "StartNo": "101",
                "EndNo": "500",
                "Prefix": "PUN",
                "Suffix": "LHC",
                "SeriesName": "PUNE - 101 To 500 - LHC",
                "Seperator": "-",
                "DocumentNoLength": "6",
                "YearCode": "2025 - 2025",
            },
            {
                "Document": "VehicleTrip",
                "OrganizationLocation": "PUNE",
                "StartNo": "501",
                "EndNo": "1000",
                "Prefix": "PUN",
                "Suffix": "LHC",
                "SeriesName": "PUNE - 501 To 1000 - LHC",
                "Seperator": "-",
                "DocumentNoLength": "6",
                "YearCode": "2025 - 2025",
            },
            {
                "Document": "VehicleTrip",
                "OrganizationLocation": "JAIPUR",
                "StartNo": "101",
                "EndNo": "500",
                "Prefix": "JPR",
                "Suffix": "LHC",
                "SeriesName": "JAIPUR - 101 To 500 - LHC",
                "Seperator": "-",
                "DocumentNoLength": "6",
                "YearCode": "2025 - 2025",
            },
            {
                "Document": "VehicleTrip",
                "OrganizationLocation": "JAIPUR",
                "StartNo": "501",
                "EndNo": "1000",
                "Prefix": "JPR",
                "Suffix": "LHC",
                "SeriesName": "JAIPUR - 501 To 1000 - LHC",
                "Seperator": "-",
                "DocumentNoLength": "6",
                "YearCode": "2025 - 2025",
            },
            {
                "Document": "VehicleTrip",
                "OrganizationLocation": "AHMEDABAD",
                "StartNo": "101",
                "EndNo": "500",
                "Prefix": "AHM",
                "Suffix": "LHC",
                "SeriesName": "AHMEDABAD - 101 To 500 - LHC",
                "Seperator": "-",
                "DocumentNoLength": "6",
                "YearCode": "2025 - 2025",
            },
            {
                "Document": "VehicleTrip",
                "OrganizationLocation": "AHMEDABAD",
                "StartNo": "501",
                "EndNo": "1000",
                "Prefix": "AHM",
                "Suffix": "LHC",
                "SeriesName": "AHMEDABAD - 501 To 1000 - LHC",
                "Seperator": "-",
                "DocumentNoLength": "6",
                "YearCode": "2025 - 2025",
            },
            {
                "Document": "VehicleTrip",
                "OrganizationLocation": "HYDERABAD",
                "StartNo": "101",
                "EndNo": "500",
                "Prefix": "HYD",
                "Suffix": "LHC",
                "SeriesName": "HYDERABAD - 101 To 500 - LHC",
                "Seperator": "-",
                "DocumentNoLength": "6",
                "YearCode": "2025 - 2025",
            },
            {
                "Document": "VehicleTrip",
                "OrganizationLocation": "HYDERABAD",
                "StartNo": "501",
                "EndNo": "1000",
                "Prefix": "HYD",
                "Suffix": "LHC",
                "SeriesName": "HYDERABAD - 501 To 1000 - LHC",
                "Seperator": "-",
                "DocumentNoLength": "6",
                "YearCode": "2025 - 2025",
            },
            {
                "Document": "VehicleTrip",
                "OrganizationLocation": "DELHI",
                "StartNo": "101",
                "EndNo": "500",
                "Prefix": "DEL",
                "Suffix": "LHC",
                "SeriesName": "DELHI - 101 To 500 - LHC",
                "Seperator": "-",
                "DocumentNoLength": "6",
                "YearCode": "2025 - 2025",
            },
            {
                "Document": "VehicleTrip",
                "OrganizationLocation": "DELHI",
                "StartNo": "501",
                "EndNo": "1000",
                "Prefix": "DEL",
                "Suffix": "LHC",
                "SeriesName": "DELHI - 501 To 1000 - LHC",
                "Seperator": "-",
                "DocumentNoLength": "6",
                "YearCode": "2025 - 2025",
            },
        ]

        # Iterate over each location and create it
        for i in Series:
            if self.switch_frames("btn_NewRecord"):
                self.click_element(By.ID, "btn_NewRecord")

            # Fill out the form
            if self.switch_frames("DocumentId"):
                self.select_dropdown(By.ID, "DocumentId", i["Document"])
                self.select_dropdown(
                    By.ID, "OrganizationLocationId", i["OrganizationLocation"]
                )
                self.send_keys(By.ID, "StartNo", i["StartNo"])
                self.send_keys(By.ID, "EndNo", i["EndNo"])
                self.send_keys(By.ID, "Prefix", i["Prefix"])
                self.send_keys(By.ID, "Suffix", i["Suffix"])
                self.send_keys(By.ID, "SeriesName", i["SeriesName"])
                self.send_keys(By.ID, "Seperator", i["Seperator"])
                self.send_keys(By.ID, "DocumentNoLength", i["DocumentNoLength"])
                self.select_dropdown(By.ID, "YearCode", i["YearCode"])
                print(f"Details entered for {i['OrganizationLocation']}")

            # Submit the form
            if self.switch_frames("mysubmit"):
                self.click_element(By.ID, "mysubmit")
                print(f"Series {i['OrganizationLocation']} created successfully.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

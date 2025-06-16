from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select, WebDriverWait
from openpyxl import Workbook

# How to get all dropdown values inside dropdown


class Test1(unittest.TestCase):
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
                ex.NoSuchElementException,
            ):
                print(f"[WARNING] Attempt {retry + 1} failed, retrying...")
                time.sleep(2)
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
            print("Clicked using JavaScript", value)
            return True
        except:
            print("Unable to click using JavaScript", value)
            return False

    def send_keys(self, by, value, text):
        try:
            i = self.wait.until(EC.element_to_be_clickable((by, value)))
            i.clear()
            i.send_keys(text)
            print("Sent keys to element", value)
            return True
        except (
            ex.StaleElementReferenceException,
            ex.TimeoutException,
            ex.NoSuchElementException,
        ):
            print("Unable to send keys to element", value)
            return False

    def switch_frames(self, element_id):
        driver = self.driver
        driver.switch_to.default_content()
        i = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in i:
            driver.switch_to.frame(iframe)
            try:
                if driver.find_element(By.ID, element_id):
                    return True
            except ex.NoSuchElementException:
                driver.switch_to.default_content()
        return False

    def return_dropdown_options(self, by, value):
        element = self.wait.until(EC.presence_of_element_located((by, value)))
        i = Select(element)  # Create a Select object
        all_options = i.options  # Get all options

        # Create a new Excel workbook and sheet
        wb = Workbook()  # Create a new workbook
        ws = wb.active  # Get the active sheet
        ws.title = "DropdownOptions"  # Set the sheet title
        ws.append(["Option Text"])  # Header

        print("All dropdown options for", value + ":")
        for option in all_options:  # Loop through each option
            text = option.text.strip()  # Get the text of the option
            print(f"option: {text}")  # Print the text
            ws.append([text])  # Write each option to Excel

        # Save the workbook
        wb.save("dropdown_options.xlsx")
        print("Dropdown options saved to dropdown_options.xlsx")

    def test_1(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript?ccode=UATASCRIPT")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "admin")
        self.send_keys(By.ID, "Password", "Omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        for i in ("Administration", "User Config »", "User Rights"):
            self.click_element(By.LINK_TEXT, i)

        if self.switch_frames("GroupId"):
            self.return_dropdown_options(By.ID, "GroupId")

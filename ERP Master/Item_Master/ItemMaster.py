from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class ItemMasterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up Chrome WebDriver
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()

    def click_element(self, by, value, timeout=2):
        """Waits for an element to be clickable and clicks it."""
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        ).click()

    def send_keys(self, by, value, text, timeout=2):
        """Waits for an element to be present and sends text to it."""
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        ).send_keys(text)

    def select_dropdown(self, by, value, option_text, timeout=2):
        """Waits for a dropdown to be present and selects an option by visible text."""
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        dropdown = Select(self.driver.find_element(by, value))
        dropdown.select_by_visible_text(option_text)

    def switch_to_iframe(self, element_id):
        """Switches to the correct iframe containing the specified element."""
        driver = self.driver
        driver.switch_to.default_content()

        for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
            driver.switch_to.frame(iframe)
            if driver.find_elements(By.ID, element_id):
                return True
            print(f"Switched to iframe containing {element_id}")

            driver.switch_to.default_content()
        print(f"Unable to locate {element_id} in any iframe!")
        return False

    # If you're using unittest, make sure your test methods start with test_
    def test_item_master(self):
        """Test case for interacting with the Item Master form."""
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")

        # Perform login
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "OMSGN9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful")

        # Navigate through menu items
        menu_items = [
            "Transportation",
            "Transportation Master »",
            "Common Masters »",
            "Item Master",
        ]

        for link_text in menu_items:
            self.click_element(By.LINK_TEXT, link_text)
            print(f"{link_text} link clicked successfully")

        # Interact with the form fields
        if self.switch_to_iframe("btn_NewRecord"):
            self.click_element(By.ID, "btn_NewRecord")

        if self.switch_to_iframe("TransportProductName"):
            self.send_keys(By.ID, "TransportProductName", "TEST11")

        if self.switch_to_iframe("CommodityTypeId"):
            self.select_dropdown(By.ID, "CommodityTypeId", "TEST1")

        if self.switch_to_iframe("mysubmit"):
            self.click_element(By.ID, "mysubmit")
            print("Form submitted successfully")

    @classmethod
    def tearDownClass(cls):
        """Closes the browser after tests are complete."""
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

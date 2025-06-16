from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Keys

"""
On completion of this exercise, you can learn the following concepts.
sendKeys()
Keyboard TAB
getAttribute()
clear()
isEnabled()
"""


class InputDemo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 15)

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
                print(
                    f"Retrying click on {by} with value {value}, attempt {i + 1}/{retry}"
                )
                time.sleep(1)
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except ex.TimeoutException:
            return False

    def send_keys(self, by, value, text):
        try:
            i = self.wait.until(EC.visibility_of_element_located((by, value)))
            i.clear()
            i.send_keys(text)
            return True
        except (
            ex.StaleElementReferenceException,
            ex.TimeoutException,
            ex.NoSuchElementException,
        ):
            return False

    def test_input_demo(self):
        driver = self.driver
        driver.get("https://letcode.in/edit")
        print("Page open Successfully")

        # Enter your full Name
        self.send_keys(By.ID, "fullName", "Omkar Kadam")
        print(f"Name entered")

        # Append a text and press keyboard tab
        i = self.wait.until(EC.visibility_of_element_located((By.ID, "join")))
        i.send_keys(" Playing Football")
        time.sleep(3)

        # What is inside the text box
        i = driver.find_element(By.ID, "getMe")
        attribute_value = i.get_attribute("value")
        print(attribute_value)

        # Confirm edit field is disabled(True / False)
        i = driver.find_element(By.ID, "noEdit")
        confirmation = i.is_enabled()
        print(confirmation)

        # Confirm text in readonly
        i = driver.find_element(By.ID, "dontwrite")
        confirmation = i.get_attribute("readonly")
        print(f"text field is readonly:{confirmation}")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager


class RegisterUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 5)

    def click_element(self, by, value, retry=2):
        for attempt in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by, value))).click()
                print(f"[SUCCESS] Clicked element: {value}")
                return True
            except (
                ex.ElementClickInterceptedException,
                ex.StaleElementReferenceException,
                ex.TimeoutException,
            ):
                print(f"[WARNING] Attempt {attempt + 1} failed, retrying...")
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
            print(f"[SUCCESS] Clicked element using JavaScript: {value}")
            return True
        except:
            return False

    def send_keys(self, by, value, text):
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        element.clear()
        element.send_keys(text)

    def test_login(self):
        driver = self.driver
        driver.get("http://192.168.0.50:82/")
        self.send_keys(By.ID, "TextBox1", "omkar")
        self.send_keys(By.ID, "Password1", "omkar9")
        self.click_element(By.ID, "Button1")
        print("Login successful")

        self.click_element(By.ID, "ctl00_ContentPlaceHolder1_ImageButton1")
        print("LogIn successful")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

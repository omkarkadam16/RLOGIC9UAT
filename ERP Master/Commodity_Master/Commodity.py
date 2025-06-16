from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class LoginPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def click_element(self, by, value, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        ).click()
        print(f"Clicked on {value}")

    def send_keys(self, by, value, text, timeout=5):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        ).send_keys(text)
        print(f"Sent keys to {value}")

    def switch_frames(self, element_id):
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

    def test_Commodity_Master(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS?RLS")

        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "OMSGN9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful")

        menus = [
            "Transportation",
            "Transportation Master »",
            "Common Masters »",
            "Commodity",
        ]

        for links in menus:
            self.click_element(By.LINK_TEXT, links)
            print(f"{links} link clicked successfully")

        if self.switch_frames("btn_NewRecord"):
            self.click_element(By.ID, "btn_NewRecord")

        if self.switch_frames("MasterName"):
            self.send_keys(By.ID, "MasterName", "T3")

        if self.switch_frames("Code"):
            self.send_keys(By.ID, "Code", "T3")

        if self.switch_frames("mysubmit"):
            self.click_element(By.ID, "mysubmit")
            print("Form submitted successfully")

    @classmethod
    def tearDownClass(cls):
        """Closes the browser after tests are complete."""
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

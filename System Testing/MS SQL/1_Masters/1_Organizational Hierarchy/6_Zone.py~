from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager


class Zones(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait=WebDriverWait(cls.driver,10)

    def click_element(self,by,value,retry=2):
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by,value))).click()
                print("Clicked on element",value)
                return True
            except(ex.ElementClickInterceptedException,ex.StaleElementReferenceException,ex.TimeoutException):
                print(f'Retrying click on {by} with value {value}, attempt {i+1}/{retry}')
                time.sleep(1)
        try:
            element=self.driver.find_element(by,value)
            self.driver.execute_script("arguments[0].click();",element)
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


    def test_Zones(self):
        driver=self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript?ccode=UATASCRIPT")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "admin")
        self.send_keys(By.ID, "Password", "Omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        for i in ("Common",
                  "Geographical Hierarchy »",
                  "Zone",):
            self.click_element(By.LINK_TEXT, i)
            print(f"Navigated to {i}.")

        Series = [
            {
                "Code": "001",
                "ZoneName": "EAST"
            },
            {
                "Code": "002",
                "ZoneName": "WEST"
            },
            {
                "Code": "003",
                "ZoneName": "SOUTH"
            },
            {
                "Code": "004",
                "ZoneName": "NORTH"
            }
        ]

        # Iterate over each location and create it
        for i in Series:
            if self.switch_frames("btn_NewRecord"):
                self.click_element(By.ID, "btn_NewRecord")

            # Fill out the form
            if self.switch_frames("Code"):
                self.send_keys(By.ID, "Code", i["Code"])
                self.send_keys(By.ID, "ZoneName", i["ZoneName"])

            # Submit the form
            if self.switch_frames("mysubmit"):
                self.click_element(By.ID, "mysubmit")
                print(f"Zone = {i['ZoneName']} created successfully.")


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
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


class Railway(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 15)

    def click_element(self, by, value, retry=2):
        driver = self.driver
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by, value))).click()
                print(f"[SUCCESS] Clicked element: {value}")
                return True
            except (
                ex.ElementClickInterceptedException,
                ex.StaleElementReferenceException,
                ex.TimeoutException,
            ):
                print(f"[WARNING] Attempt {i + 1} failed, retrying...")
                time.sleep(1)
        try:
            element = driver.find_element(by, value)
            driver.execute_script("arguments[0].click();", element)
            print(f"[SUCCESS] Clicked element: {value}")
            return True
        except ex.NoSuchElementException:
            print(f"[ERROR] Element not found: {value}")
            return False

    def send_keys(self, by, value, text):
        try:
            element = self.wait.until(EC.visibility_of_element_located((by, value)))
            element.is_enabled()
            element.clear()
            element.send_keys(text)
            print(f"[SUCCESS] Sent keys: {text}")
            return True
        except ex.NoSuchElementException:
            print(f"[ERROR] Element not found: {value}")
            return False

    def switch_frames(self, element_id):
        driver = self.driver
        driver.switch_to.default_content()
        iframe = driver.find_elements(By.TAG_NAME, "iframe")
        for i in iframe:
            driver.switch_to.frame(i)
            try:
                if driver.find_element(By.ID, element_id):
                    return True
            except ex.NoSuchElementException:
                driver.switch_to.default_content()
        return False

    def dropdown_select(self, by, value, text):
        try:
            self.wait.until(EC.visibility_of_element_located((by, value)))
            element = Select(self.driver.find_element(by, value))
            element.select_by_visible_text(text)
            print(f"[SUCCESS] Selected dropdown option: {text}")
            return True
        except ex.NoSuchElementException:
            return False

    def autocomplete(self, by, value, text):
        ip = self.wait.until(EC.visibility_of_element_located((by, value)))
        ip.clear()
        ip.send_keys(text)
        time.sleep(1)

        suggest = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-menu-item"))
        )
        for i in suggest:
            if text.upper() in i.text.upper():
                i.click()
                print(f"[SUCCESS] Selected autocomplete suggestion: {text}")
                return True
        ip.send_keys(Keys.DOWN)
        ip.send_keys(Keys.ENTER)
        print("Selected autocomplete option using keyboard:", text)

    def test_registration(self):
        driver = self.driver
        driver.get("https://www.irctc.co.in/nget/train-search")
        self.click_element(By.ID, "")

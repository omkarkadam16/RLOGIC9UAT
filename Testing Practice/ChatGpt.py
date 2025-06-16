import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager


class ChatGpt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 5)

    def test_GPT(self):
        driver = self.driver
        driver.get("https://chatgpt.com/")
        print("GPT is running")

        self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "placeholder"))
        ).send_keys("how to create AI model ")
        self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "icon-2xl"))
        ).click()
        print("Processing")
        time.sleep(5)

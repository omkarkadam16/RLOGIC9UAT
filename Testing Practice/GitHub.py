from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import unittest
from webdriver_manager.chrome import ChromeDriverManager


class TestSelenium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 5)

    def test_github(self):
        self.driver.get("https://github.com/")
        print("Navigated to GitHub")

        self.driver.find_element(By.LINK_TEXT, "Sign in").click()
        print("""Clicked "Sign in" link""")
        self.driver.find_element(By.ID, "login_field").send_keys(
            "omkarkadam058@gmail.com"
        )
        self.driver.find_element(By.ID, "password").send_keys("Omkar1610")
        self.driver.find_element(By.NAME, "commit").click()
        print("Logged in successfully")

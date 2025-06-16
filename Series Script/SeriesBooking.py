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
import pandas as pd


class SeriesBook(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

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
                    f"Retrying click on {by} with value {value}, attempt {i+1}/{retry}"
                )
                time.sleep(1)
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
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
            return True
        except ex.NoSuchElementException:
            return False

    def select_dropdown(self, by, value, text):
        try:
            self.wait.until(EC.visibility_of_element_located((by, value)))
            dropdown = Select(self.driver.find_element(by, value))
            time.sleep(2)
            dropdown.select_by_visible_text(text)
            return True
        except ex.NoSuchElementException:
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
                return
        input_text.send_keys(Keys.DOWN)
        input_text.send_keys(Keys.ENTER)

    def test_SeriesBook(self):
        driver = self.driver
        driver.get("http://124.123.122.23:83/rlogicglobe")

        print("Logging in...")
        self.select_dropdown(By.ID, "ddl_YearCode", "2021 - 2022")
        self.send_keys(By.ID, "Login", "riddhi")
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

        # Read Excel data
        df = pd.read_excel("series.xlsx", engine="openpyxl")
        df.columns = df.columns.str.strip()

        for index, i in df.iterrows():
            if self.switch_frames("btn_NewRecord"):
                self.click_element(By.ID, "btn_NewRecord")

            # Fill out the form
            if self.switch_frames("DocumentId"):
                self.select_dropdown(By.ID, "DocumentId", i["Document"])
                self.select_dropdown(By.ID, "OrganizationLocationId", i["Location"])
                self.send_keys(By.ID, "StartNo", i["Start"])
                self.send_keys(By.ID, "EndNo", i["End"])
                self.send_keys(By.ID, "Prefix", i["Prefix"])
                self.send_keys(By.ID, "Suffix", i["Suffix"])
                self.send_keys(By.ID, "SeriesName", i["SeriesN"])
                self.send_keys(By.ID, "Seperator", "--")
                self.send_keys(By.ID, "DocumentNoLength", "10")
                self.select_dropdown(By.ID, "YearCode", "2021 - 2022")
                print(f"Details entered for {i['Location']}")

            # Submit the form
            if self.switch_frames("mysubmit"):
                self.click_element(By.ID, "mysubmit")
                print(f"Series {i['Location']} created successfully.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

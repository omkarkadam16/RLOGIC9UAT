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


class LHC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 15)

    def click_element(self, by, value, retry=2):
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by, value))).click()
                print("Clicked on element", value)
                return True
            except (
                ex.ElementClickInterceptedException,
                ex.StaleElementReferenceException,
                ex.TimeoutException,
            ):
                print("Element not clickable. Retrying...")
                time.sleep(1)
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            print(f"[ERROR] JavaScript click failed: {e}")
            return False

    def send_keys(self, by, value, text):
        for attempt in range(3):
            try:
                print(f"[INFO] Attempt {attempt + 1}: Entering text...")
                element = self.wait.until(EC.visibility_of_element_located((by, value)))
                element.is_enabled()
                element.clear()
                element.send_keys(text)
                print("Sent keys", text)
                return True
            except (
                ex.NoSuchElementException,
                ex.UnexpectedAlertPresentException,
                ex.TimeoutException,
                ex.StaleElementReferenceException,
            ) as e:
                print(f"[WARNING] Error : {type(e)} occurred. Retrying...")
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

    def select_dropdown(self, by, value, text):
        try:
            element = self.wait.until(EC.element_to_be_clickable((by, value)))
            element.is_enabled()
            element.click()
            self.wait.until(EC.visibility_of_element_located((by, value)))
            Select(self.driver.find_element(by, value)).select_by_visible_text(text)
            print(f"Selected dropdown option: {text}")
            return True
        except (
            ex.NoSuchElementException,
            ex.ElementClickInterceptedException,
            ex.TimeoutException,
        ):
            return False

    def test_LHC(self):
        driver = self.driver
        driver.get("https://rlogic9.com/rlogicspg?ccode=spg")
        print("Logging in...")
        self.select_dropdown(By.ID, "ddl_YearCode", "2024 - 2025")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "Omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        for i in (
            "Transportation",
            "Transportation Transaction »",
            "Outward »",
            "Vehicle Trip Modification",
        ):
            self.click_element(By.LINK_TEXT, i)
            print(f"Navigated to {i}.")

        df = pd.read_excel("spg1.xlsx", engine="openpyxl")
        df.columns = df.columns.str.strip()
        df["Status"] = ""

        for index, i in df.iterrows():
            try:
                if self.switch_frames("txtvehicletrip"):
                    self.send_keys(By.ID, "txtvehicletrip", i["TripNo"])
                    self.click_element(By.ID, "btnvehtrpmodif")
                    time.sleep(1)

                refresh_clicked = False
                if self.switch_frames("refreshCH"):
                    time.sleep(3)
                    refresh_clicked = self.click_element(By.ID, "refreshCH")
                    time.sleep(5)

                if refresh_clicked:
                    df.at[index, "Status"] = "Success"
                    print(f"[{i['TripNo']}] Refresh button clicked successfully.")
                else:
                    df.at[index, "Status"] = "Failed: Refresh Click Error"
                    print(f"[{i['TripNo']}] Failed to click refresh button.")

                self.click_element(By.ID, "mysubmit")

                try:
                    self.wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, "(//div[@class='LABELSAVEMESSAGE'])[1]")
                        )
                    )
                    print("Record saved confirmation received.")
                except:
                    print("Save confirmation not detected, proceeding anyway...")

            except Exception as e:
                df.at[index, "Status"] = f"Failed: {type(e).__name__}"
                print(f"[ERROR] Row {index} - {i['TripNo']} failed due to: {e}")

            driver.switch_to.default_content()
            for i in (
                "Transportation",
                "Transportation Transaction »",
                "Outward »",
                "Vehicle Trip Modification",
            ):
                try:
                    self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, i)))
                    self.wait.until(
                        EC.element_to_be_clickable((By.LINK_TEXT, i))
                    ).click()
                    print(f"Navigated to {i}.")
                except Exception as e:
                    print(f"[ERROR] Could not click {i} - {e}")

        df.to_excel("spg1.xlsx", index=False, engine="openpyxl")
        print("Excel updated with status based on refresh button click.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

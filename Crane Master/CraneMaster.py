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


class Booking(unittest.TestCase):
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
            print("Sent keys", text)
            return True
        except ex.NoSuchElementException:
            print(f"Element not found: {value}")
            return False

    def select_dropdown(self, by, value, text):
        try:
            e = self.wait.until(EC.element_to_be_clickable((by, value)))
            e.is_enabled()
            e.click()
            print("[SUCCESS] Clicked dropdown")
            self.wait.until(EC.visibility_of_element_located((by, value)))
            element = Select(self.driver.find_element(by, value))
            element.select_by_visible_text(text)
            print(f"[SUCCESS] Selected dropdown option: {text}")
            return True
        except (
            ex.NoSuchElementException,
            ex.ElementClickInterceptedException,
            ex.TimeoutException,
        ):
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
                print("Selected autocomplete option:", text)
                return
        input_text.send_keys(Keys.DOWN)
        input_text.send_keys(Keys.ENTER)
        print("Selected autocomplete option using keyboard:", text)

    def test_Master(self):
        driver = self.driver
        driver.get("https://rlogic9.com/RLogicSumeet?ccode=Sumeet")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "RIDDHI")
        self.send_keys(By.ID, "Password", "OMSGN9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        for i in (
            "Fleet",
            "Fleet Master »",
            "Vehicle »",
            "Crane",
        ):
            self.click_element(By.LINK_TEXT, i)
            print(f"Navigated to {i}.")
        # Read Excel data
        df = pd.read_excel("test.xlsx", engine="openpyxl")

        for index, row in df.iterrows():
            try:
                print(f"Processing Vehicle_Category: {row['Vehicle_Category']}")

                if self.switch_frames("btn_NewRecord"):
                    self.click_element(By.ID, "btn_NewRecord")

                # General Details
                if self.switch_frames("VehicleNo"):
                    self.send_keys(By.ID, "VehicleNo", row["Vehicle_No"])
                    self.select_dropdown(By.ID, "VehicleTypeId", row["Vehicle_Type"])
                    self.select_dropdown(
                        By.ID, "VehicleCategoryId", row["Vehicle_Category"]
                    )
                    self.select_dropdown(By.ID, "VehicleBodyId", row["Vehicle_Body"])
                    # self.select_dropdown(By.ID, "CarrierCategoryId", "VehicleNo")
                    self.send_keys(
                        By.ID, "YearOfManufacturer", row["Year_Of_Manufacture"]
                    )
                    self.select_dropdown(By.ID, "ManufactureId", row["Manufacturer"])
                    self.select_dropdown(By.ID, "VehicleModelId", row["Vehicle_Model"])
                    self.autocomplete_select(
                        By.ID, "ControllingBranchId-select", "MUMBAI"
                    )

                    # Specification Details
                    self.send_keys(By.ID, "ChasisNo", row["Chasis_No"])
                    if pd.notna(row["Engine_No"]):
                        self.send_keys(By.ID, "EngineNo", row["Engine_No"])
                    if pd.notna(row["Trolly_Chasis_No"]):
                        self.send_keys(
                            By.ID, "TrolleyChasisNo", row["Trolly_Chasis_No"]
                        )
                    # self.select_dropdown(By.ID, "FuelTypeId", row["DIESEL"])
                    self.send_keys(By.ID, "GrossWeight", row["Gross_Wt"])
                    self.send_keys(By.ID, "Length", row["Length"])
                    self.send_keys(By.ID, "Breadth", row["Width"])  # Width
                    if pd.notna(row["Fuel_Tank_Capacity"]):
                        self.send_keys(
                            By.ID, "FuelTankCapacity", row["Fuel_Tank_Capacity"]
                        )
                    self.send_keys(By.ID, "UnLadenWeight", row["Unladen_Wt"])
                    self.send_keys(By.ID, "WheelBase", row["Wheel_Base"])
                    self.send_keys(By.ID, "Height", row["Height"])
                    if pd.notna(row["Power_bhp"]):
                        self.send_keys(
                            By.ID, "CustomField1", row["Power_bhp"]
                        )  # Power BHP

                # if self.switch_frames("mysubmit"):
                # self.click_element(By.ID, "mysubmit")
                time.sleep(2)

            except Exception as e:
                print(f"Failed to process Vehicle_No {row['Vehicle_No']}: {str(e)}")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

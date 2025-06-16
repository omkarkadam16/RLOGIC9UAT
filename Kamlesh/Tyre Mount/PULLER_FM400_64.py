import pandas as pd
import unittest
import time
import selenium.common.exceptions as ex
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class ProductParameter(unittest.TestCase):
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
                    f"Retrying click on {by} with value {value}, attempt {i + 1}/{retry}"
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
            print(f"Element not found: {value}")
            return False

    def select_dropdown(self, by, value, text):
        try:
            e = self.wait.until(EC.element_to_be_clickable((by, value)))
            e.is_enabled()
            e.click()
            self.wait.until(EC.visibility_of_element_located((by, value)))
            element = Select(self.driver.find_element(by, value))
            element.select_by_visible_text(text)
            return True
        except (
            ex.NoSuchElementException,
            ex.ElementClickInterceptedException,
            ex.TimeoutException,
        ):
            return False

    def autocomplete_select(self, by, value, text):
        self.wait.until(EC.element_to_be_clickable((by, value))).click()
        input_text = self.wait.until(EC.visibility_of_element_located((by, value)))
        input_text.clear()
        input_text.send_keys(text)
        time.sleep(3)
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

    def tyre_position(self, tyre_selector, location, ro_number):
        self.click_element(By.XPATH, tyre_selector)
        if self.switch_frames("FromStorageHouseId"):
            self.select_dropdown(By.ID, "FromStorageHouseId", location)
            self.autocomplete_select(By.ID, "TyreSerialNo-select", ro_number)
            self.click_element(By.ID, "Remarks")
            self.click_element(By.ID, "btnSave-TyreMountSession")

    def test_product_parameter(self):
        driver = self.driver
        driver.get("https://rlogic9.com/RLogicSumeet/Login")

        self.send_keys(By.ID, "Login", "riddhi")
        self.send_keys(By.ID, "Password", "Omsgn9")
        self.click_element(By.ID, "btnLogin")

        menus = ["Fleet", "Fleet Master »", "Tyre Movement »", "Tyre Mount"]
        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)

            # Read Excel data
            df = pd.read_excel("PULLER FM400 64.xlsx", engine="openpyxl")
            df.columns = df.columns.str.strip()

            for index, i in df.iterrows():

                if self.switch_frames("btn_NewRecord"):
                    self.click_element(By.ID, "btn_NewRecord")
                    time.sleep(2)

                    # Driver Info
                    if self.switch_frames("VehicleId-select"):
                        self.autocomplete_select(
                            By.ID, "VehicleId-select", i["VehicleNo"]
                        )
                        self.click_element(By.ID, "WorkDoneBy")
                        Location = i["StorageHouse"]

                        # Tyre RO1
                        self.tyre_position(
                            "(//img[@class='ImgR'])[1]", Location, i["RO1"]
                        )
                        # self.click_element(By.XPATH, "(//img[@class='ImgR'])[1]")
                        # time.sleep(1)
                        # if self.switch_frames("FromStorageHouseId"):
                        #     self.select_dropdown(By.ID, "FromStorageHouseId", Location)
                        #     self.autocomplete_select(By.ID, "TyreSerialNo-select", i["RO1"])
                        #     self.click_element(By.ID,"Remarks")
                        #     time.sleep(2)
                        #     self.click_element(By.ID,"btnSave-TyreMountSession")
                        # time.sleep(1)

                        # Tyre RO2
                        self.tyre_position(
                            "//table[3]//td[5]//a/img", Location, i["RO2"]
                        )
                        # self.click_element(By.XPATH, "//table[3]//td[5]//a/img")
                        # time.sleep(1)
                        # if self.switch_frames("FromStorageHouseId"):
                        #     self.select_dropdown(By.ID, "FromStorageHouseId", Location)
                        #     self.autocomplete_select(By.ID, "TyreSerialNo-select", i["RO2"])
                        #     self.click_element(By.ID, "Remarks")
                        #     time.sleep(2)
                        #     self.click_element(By.ID, "btnSave-TyreMountSession")
                        #     time.sleep(1)

                        # Tyre RO3
                        self.tyre_position(
                            "//table[5]//td[5]//a/img", Location, i["RO3"]
                        )
                        # self.click_element(By.XPATH, "//table[5]//td[5]//a/img")
                        # time.sleep(1)
                        # if self.switch_frames("FromStorageHouseId"):
                        #     self.select_dropdown(By.ID, "FromStorageHouseId", Location)
                        #     self.autocomplete_select(By.ID, "TyreSerialNo-select", i["RO3"])
                        #     self.click_element(By.ID, "Remarks")
                        #     time.sleep(2)
                        #     self.click_element(By.ID, "btnSave-TyreMountSession")
                        #     time.sleep(1)

                        # Tyre RI2
                        self.tyre_position(
                            "//table[3]//td[4]//a/img", Location, i["RI2"]
                        )
                        # self.click_element(By.XPATH, "//table[3]//td[4]//a/img")
                        # time.sleep(1)
                        # if self.switch_frames("FromStorageHouseId"):
                        #     self.select_dropdown(By.ID, "FromStorageHouseId", Location)
                        #     self.autocomplete_select(By.ID, "TyreSerialNo-select", i["RI2"])
                        #     self.click_element(By.ID, "Remarks")
                        #     time.sleep(2)
                        #     self.click_element(By.ID, "btnSave-TyreMountSession")
                        #     time.sleep(1)

                        # Tyre RI3
                        self.tyre_position(
                            "//table[5]//td[4]//a/img", Location, i["RI3"]
                        )
                        # self.click_element(By.XPATH, "//table[5]//td[4]//a/img")
                        # time.sleep(1)
                        # if self.switch_frames("FromStorageHouseId"):
                        #     self.select_dropdown(By.ID, "FromStorageHouseId", Location)
                        #     self.autocomplete_select(By.ID, "TyreSerialNo-select", i["RI3"])
                        #     self.click_element(By.ID, "Remarks")
                        #     time.sleep(2)
                        #     self.click_element(By.ID, "btnSave-TyreMountSession")
                        #     time.sleep(1)

                        # Tyre LO1
                        self.tyre_position(
                            "//table[1]//td[1]//a/img", Location, i["LO1"]
                        )
                        # self.click_element(By.XPATH, "//table[1]//td[1]//a/img")
                        # time.sleep(1)
                        # if self.switch_frames("FromStorageHouseId"):
                        #     self.select_dropdown(By.ID, "FromStorageHouseId", Location)
                        #     self.autocomplete_select(By.ID, "TyreSerialNo-select", i["LO1"])
                        #     self.click_element(By.ID, "Remarks")
                        #     time.sleep(2)
                        #     self.click_element(By.ID, "btnSave-TyreMountSession")
                        #     time.sleep(1)

                        # Tyre LO2
                        self.tyre_position(
                            "//table[3]//td[1]//a/img", Location, i["LO2"]
                        )
                        # self.click_element(By.XPATH, "//table[3]//td[1]//a/img")
                        # time.sleep(1)
                        # if self.switch_frames("FromStorageHouseId"):
                        #     self.select_dropdown(By.ID, "FromStorageHouseId", Location)
                        #     self.autocomplete_select(By.ID, "TyreSerialNo-select", i["LO2"])
                        #     self.click_element(By.ID, "Remarks")
                        #     time.sleep(2)
                        #     self.click_element(By.ID, "btnSave-TyreMountSession")
                        #     time.sleep(1)

                        # Tyre LO3
                        self.tyre_position(
                            "//table[5]//td[1]//a/img", Location, i["LO3"]
                        )
                        # self.click_element(By.XPATH, "//table[5]//td[1]//a/img")
                        # time.sleep(1)
                        # if self.switch_frames("FromStorageHouseId"):
                        #     self.select_dropdown(By.ID, "FromStorageHouseId",Location)
                        #     self.autocomplete_select(By.ID, "TyreSerialNo-select", i["LO3"])
                        #     self.click_element(By.ID, "Remarks")
                        #     time.sleep(2)
                        #     self.click_element(By.ID, "btnSave-TyreMountSession")
                        #     time.sleep(1)

                        # Tyre LI2
                        self.tyre_position(
                            "//table[3]//td[2]//a/img", Location, i["LI2"]
                        )
                        # self.click_element(By.XPATH, "//table[3]//td[2]//a/img")
                        # time.sleep(1)
                        # if self.switch_frames("FromStorageHouseId"):
                        #     self.select_dropdown(By.ID, "FromStorageHouseId", Location)
                        #     self.autocomplete_select(By.ID, "TyreSerialNo-select", i["LI2"])
                        #     self.click_element(By.ID, "Remarks")
                        #     time.sleep(2)
                        #     self.click_element(By.ID, "btnSave-TyreMountSession")
                        #     time.sleep(1)

                        # Tyre LI3
                        self.tyre_position(
                            "//table[5]//td[2]//a/img", Location, i["LI3"]
                        )
                        # self.click_element(By.XPATH, "//table[5]//td[2]//a/img")
                        # time.sleep(1)
                        # if self.switch_frames("FromStorageHouseId"):
                        #     self.select_dropdown(By.ID, "FromStorageHouseId",Location)
                        #     self.autocomplete_select(By.ID, "TyreSerialNo-select", i["LI3"])
                        #     self.click_element(By.ID, "Remarks")
                        #     time.sleep(2)
                        #     self.click_element(By.ID, "btnSave-TyreMountSession")
                        #     time.sleep(1)

                if self.switch_frames("mysubmit"):
                    self.click_element(By.ID, "mysubmit")
                    time.sleep(2)
                    print(f"[SUCCESS] Saved record:- {i['VehicleNo']}")


if __name__ == "__main__":
    unittest.main()

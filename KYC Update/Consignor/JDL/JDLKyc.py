import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager


class KycUpdate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

    def click_element(self, by, value, retries=2):
        """Click an element, retrying if necessary."""
        for attempt in range(retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
                print("[SUCCESS] Clicked element: " + value)
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
            return True
        except:
            return False

    def switch_frames(self, element_id):
        self.driver.switch_to.default_content()
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            self.driver.switch_to.frame(iframe)
            try:
                if self.driver.find_element(By.ID, element_id):
                    return True
            except ex.NoSuchElementException:
                self.driver.switch_to.default_content()
        return False

    def send_keys(self, by, value, text):
        """Send text to an input field when it becomes visible."""
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        if element.is_enabled():
            element.clear()
            element.send_keys(text)
        else:
            raise Exception(f"Element located by ({by}, {value}) is not enabled.")

    def test_master(self):
        self.driver.get("http://192.168.0.72/Rlogic9JDL/")
        self.driver.find_element(By.ID, "Login").send_keys("Riddhi")
        self.driver.find_element(By.ID, "Password").send_keys("OMSGN9")
        self.driver.find_element(By.ID, "btnLogin").click()
        print("Login successful")

        for links in [
            "Transportation",
            "Transportation Master »",
            "Consignor/Consignee »",
            "Consignor / Consignee",
        ]:
            self.driver.find_element(By.LINK_TEXT, links).click()

        if self.switch_frames("tgladdnclm"):
            self.driver.find_element(By.ID, "tgladdnclm").click()

        df = pd.read_excel("JDL.xlsx", engine="openpyxl")

        for index, row in df.iterrows():
            try:
                print(f"Processing UID: {row['UID']}")

                if self.switch_frames("txt_Extrasearch"):
                    self.send_keys(By.ID, "txt_Extrasearch", str(row["UID"]))
                    self.click_element(By.ID, "btn_Seach")
                    max_attempts = 5
                    attempts = 0
                    while attempts < max_attempts:
                        if self.click_element(By.ID, row["DD"]):
                            self.click_element(By.PARTIAL_LINK_TEXT, "Edit")
                            break
                        if not self.click_element(By.LINK_TEXT, "Next"):
                            break
                        attempts += 1

                self.click_element(By.PARTIAL_LINK_TEXT, "Edit")
                time.sleep(2)

                if self.switch_frames("acaretdowndivGstEkyc"):
                    self.click_element(By.ID, "acaretdowndivGstEkyc")
                time.sleep(1)

                if self.switch_frames("btn_SearchGSTNo"):
                    if self.click_element(
                        By.ID, "btn_SearchGSTNo"
                    ):  # Status depends on this click

                        df.at[index, "Status"] = (
                            "Updated"  # Update status immediately after button click
                        )

                        # Wait for ekycTradeName field and extract Consignor/Consignee value
                        time.sleep(1)
                        consignee_name = self.wait.until(
                            EC.presence_of_element_located((By.ID, "ekycTradeName"))
                        )
                        consignee_value = consignee_name.get_attribute(
                            "value"
                        ).strip()  # Get updated timestamp
                        df.at[index, "Consignor/Consignee"] = (
                            consignee_value  # Store timestamp
                        )

                        # Wait for KYC update field and extract GST Verified On value
                        time.sleep(1)
                        ekyc_element = self.wait.until(
                            EC.presence_of_element_located((By.ID, "ekycLogDateTime"))
                        )
                        ekyc_value = ekyc_element.get_attribute(
                            "value"
                        ).strip()  # Get updated timestamp
                        df.at[index, "GST Verified On"] = ekyc_value  # Store timestamp
                    else:
                        df.at[index, "Status"] = "Not Updated (Button Click Failed)"
                        self.driver.execute_script("window.scrollTo(0, 1000);")

                if self.switch_frames("mysubmit"):
                    self.click_element(By.ID, "mysubmit")

            except Exception as e:
                print(f"Failed to process UID {row['UID']}: {str(e)}")

            df.to_excel("JDL.xlsx", index=False, engine="openpyxl")
        print("✅ KYC Update Completed! Check JDL.xlsx for results.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

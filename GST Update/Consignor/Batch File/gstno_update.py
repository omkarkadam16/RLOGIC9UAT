import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import unittest
import time
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common import exceptions as ex
from selenium.webdriver.support import expected_conditions as EC


class CustomerMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Initializing WebDriver...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            "--disable-software-rasterizer"
        )  # Prevents WebGL issues
        chrome_options.add_argument("--enable-unsafe-swiftshader")

        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 5)
        print("WebDriver initialized successfully.")

    def click_element(self, by, value, max_attempts=3):
        attempt = 0
        element = None

        while attempt < max_attempts:
            try:
                print(f"Attempting to click element: {value} (Attempt {attempt + 1})")
                element = self.wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
                print(f"Successfully clicked element: {value}")
                return True
            except (
                ex.ElementClickInterceptedException,
                ex.StaleElementReferenceException,
                ex.TimeoutException,
            ) as e:
                print(
                    f"[WARNING] Attempt {attempt + 1}: {type(e).__name__} occurred. Retrying..."
                )
                time.sleep(1)

            if element:
                try:
                    print(f"Trying JavaScript click for element: {value}")
                    self.driver.execute_script("arguments[0].click();", element)
                    return True
                except ex.JavascriptException as js_error:
                    print(
                        f"[ERROR] JavaScript click failed due to {type(js_error).__name__}"
                    )
            attempt += 1
        print(f"[ERROR] Could not click element: {value}")
        return False

    def switch_frames(self, element_id):
        print(f"Switching to frame containing element: {element_id}")
        self.driver.switch_to.default_content()

        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            self.driver.switch_to.frame(iframe)
            try:
                if self.driver.find_element(By.ID, element_id):
                    print(f"Switched to correct frame for element: {element_id}")
                    return True
            except NoSuchElementException:
                self.driver.switch_to.default_content()
        print(f"[ERROR] Could not find frame for element: {element_id}")
        return False

    def send_keys(self, by, value, text):
        print(f"Entering text '{text}' into element: {value}")
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        element.clear()
        element.send_keys(text)
        print(f"Successfully entered text into element: {value}")

    def test_customer(self):
        driver = self.driver
        print("Navigating to login page...")
        driver.get("http://192.168.0.72/Rlogic9UataScript/Login")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "admin")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        navigation_links = [
            "Transportation",
            "Transportation Master »",
            "Consignor/Consignee »",
            "Consignor / Consignee",
        ]

        for link_text in navigation_links:
            print(f"Navigating to: {link_text}")
            self.click_element(By.LINK_TEXT, link_text)

        if self.switch_frames("tgladdnclm"):
            self.click_element(By.ID, "tgladdnclm")

        print("Reading Excel file...")
        df = pd.read_excel("GST.xlsx", engine="openpyxl")

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

                self.send_keys(By.ID, "ekycGSTNo", row["GST"])
                self.click_element(By.ID, "btn_SearchGSTNo")

                if self.switch_frames("mysubmit"):
                    self.click_element(By.ID, "mysubmit")
                    df.at[index, "Status"] = "Passed"
                    print(f"✅ UID {row['UID']} processed successfully.")
                else:
                    df.at[index, "Status"] = "Failed"
                    print(f"❌ UID {row['UID']} failed to process.")

                df.at[index, "Execution Time"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

            except Exception as e:
                print(
                    f"[ERROR] Exception occurred while processing UID {row['UID']}: {e}"
                )
                df.at[index, "Status"] = "Failed"
                df.at[index, "Execution Time"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

        df.to_excel("GST.xlsx", index=False, engine="openpyxl")
        print("✅ GST Update Completed! Check GST.xlsx for results.")
        input("Press Enter to exit...")

    @classmethod
    def tearDownClass(cls):
        print("Closing WebDriver...")
        cls.driver.quit()
        print("WebDriver closed.")


if __name__ == "__main__":
    unittest.main()

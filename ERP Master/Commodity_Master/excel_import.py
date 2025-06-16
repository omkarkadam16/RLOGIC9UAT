import unittest
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CommodityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize WebDriver."""
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def switch_to_iframe(self, element_id):
        """Switch to iframe containing the given element."""
        driver = self.driver
        driver.switch_to.default_content()

        for index, iframe in enumerate(driver.find_elements(By.TAG_NAME, "iframe")):
            driver.switch_to.frame(iframe)
            try:
                if driver.find_element(By.ID, element_id):
                    print(
                        f"✅ Switched to iframe containing {element_id} (Index {index})"
                    )
                    return True
            except:
                driver.switch_to.default_content()
        print(f"❌ Unable to locate {element_id} in any iframe!")
        return False

    def login(self):
        """Perform login."""
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")

        driver.find_element(By.ID, "Login").send_keys("Riddhi")
        driver.find_element(By.ID, "Password").send_keys("OMSGN9")
        driver.find_element(By.ID, "btnLogin").click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Transportation"))
        )
        print("✅ Login successful!")

    def navigate_to_commodity_master(self):
        """Navigate to Commodity Master."""
        menu_items = [
            "Transportation",
            "Transportation Master »",
            "Common Masters »",
            "Commodity",
        ]
        for link_text in menu_items:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            ).click()
            print(f"✅ {link_text} clicked successfully")

    def add_commodities_from_excel(self):
        """Read Excel file and add multiple commodities dynamically."""
        driver = self.driver
        data = pd.read_excel("test_data.xlsx")  # Load test data

        if self.switch_to_iframe("btn_NewRecord"):
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "btn_NewRecord"))
            ).click()
            print("✅ New Record button clicked successfully")

        for index, row in data.iterrows():
            commodity_name = str(row["Commodity Name"])
            commodity_code = str(row["Commodity Code"])

            # Ensure we are in the correct iframe before interacting with form fields
            if self.switch_to_iframe("MasterName"):
                master_name_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "MasterName"))
                )
                master_name_field.clear()
                master_name_field.send_keys(commodity_name)

                code_field = driver.find_element(By.ID, "Code")
                code_field.clear()
                code_field.send_keys(commodity_code)

                # Click "Save & New" button
                driver.find_element(By.ID, "mysubmitNew").click()

                # ✅ Wait for form to refresh before adding the next commodity
                WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element_value((By.ID, "MasterName"), "")
                )

                print(
                    f"✅ Commodity '{commodity_name}' (Code: {commodity_code}) saved successfully!"
                )

        print("🎉 All commodities added successfully!")

    def test_commodity(self):
        """Complete Commodity creation workflow using Excel data."""
        self.login()
        self.navigate_to_commodity_master()
        self.add_commodities_from_excel()

    @classmethod
    def tearDownClass(cls):
        """Close the browser after all tests."""
        cls.driver.quit()
        print("🔒 Browser closed.")


if __name__ == "__main__":
    unittest.main()

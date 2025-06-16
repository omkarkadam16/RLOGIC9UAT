from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class CommodityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the Chrome WebDriver and open the browser."""
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def switch_to_iframe(self, element_id):
        """Switch to the iframe containing the specified element."""
        driver = self.driver
        driver.switch_to.default_content()

        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for index, iframe in enumerate(iframes):
            driver.switch_to.frame(index)
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

    def test_add_multiple_commodities(self):
        """Perform login and add multiple commodity entries."""
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")

        # 🔹 Login
        driver.find_element(By.ID, "Login").send_keys("Riddhi")
        driver.find_element(By.ID, "Password").send_keys("OMSGN9")
        driver.find_element(By.ID, "btnLogin").click()

        # Wait for the Transportation menu to appear
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Transportation"))
        )
        print("✅ Login successful!")

        # 🔹 Navigate through menu items
        menu_items = [
            ("Transportation", "Transportation"),
            ("Transportation Master »", "Transportation Master"),
            ("Common Masters »", "Common Masters"),
            ("Commodity", "Commodity Masters"),
        ]

        for link_text, description in menu_items:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            ).click()
            print(f"✅ {description} link clicked successfully")

        # 🔹 Click "New Record" button once
        if self.switch_to_iframe("btn_NewRecord"):
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "btn_NewRecord"))
            ).click()
            print("✅ New Record button clicked successfully")

        # 🔹 List of commodities to be added
        commodities = [("TEST11", "T11"), ("TEST9", "T9"), ("TEST10", "T10")]

        for name, code in commodities:
            # Switch to the iframe containing the input fields
            if self.switch_to_iframe("MasterName"):
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "MasterName"))
                ).send_keys(name)
                print(f"✅ Commodity Name '{name}' filled")

                driver.find_element(By.ID, "Code").send_keys(code)
                print(f"✅ Commodity Code '{code}' filled")

                # Click "mysubmitNew" to save and refresh the form
                driver.find_element(By.ID, "mysubmitNew").click()
                print(f"✅ Commodity '{name}' saved and new form opened")

                # Wait for the form to refresh before entering new data
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "MasterName"))
                )

    @classmethod
    def tearDownClass(cls):
        """Close the browser after all tests are completed."""
        cls.driver.quit()
        print("🔒 Browser closed.")


if __name__ == "__main__":
    unittest.main()

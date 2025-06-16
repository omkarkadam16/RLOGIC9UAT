from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager


class RegisterUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 5)

    def click_element(self, by, value, retry=2):
        for attempt in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by, value))).click()
                print(f"[SUCCESS] Clicked element: {value}")
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
            print(f"[SUCCESS] Clicked element using JavaScript: {value}")
            return True
        except:
            return False

    def send_keys(self, by, value, text):
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        element.clear()
        element.send_keys(text)
        print(f"Sent keys: {text} to element: {value}")

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

    def checkbox(self, checkbox_id):
        """Selects a checkbox if not already selected and verifies it."""
        checkbox = self.driver.find_element(By.ID, checkbox_id)
        if not checkbox.is_selected():
            checkbox.click()
            print(f"Selected checkbox: {checkbox_id}")

    def select_dropdown(self, by, value, option_text):
        self.wait.until(EC.visibility_of_element_located((by, value)))
        dropdown = Select(self.driver.find_element(by, value))
        dropdown.select_by_visible_text(option_text)
        print(f"Selected dropdown option: {option_text}")

    def select_products(self, product_names):
        for i in range(1, 4):
            self.click_element(By.XPATH, f"//*[@id='pagination']/li[{i}]/a")
            time.sleep(2)

            # Iterate through all rows in the product table
            for row in self.driver.find_elements(
                By.XPATH, "//table[@id='productTable']/tbody/tr"
            ):
                name = row.find_element(By.XPATH, "./td[2]").text.strip()

                if name in product_names:
                    row.find_element(By.XPATH, "./td[4]/input").click()
                    print(f"✅ Selected '{name}'")

                    product_names.remove(name)

                    if not product_names:
                        return

    def test_register_user(self):
        driver = self.driver
        driver.get("https://testautomationpractice.blogspot.com/")
        print("Navigated to Automation Exercise")

        self.send_keys(By.ID, "name", "Omkar Kadam")

        self.send_keys(By.ID, "email", "omkarkadam058@gmail.com")

        self.send_keys(By.ID, "phone", "9284326684")

        self.send_keys(By.ID, "textarea", "Post, Turbhe, Tal - Poladpur, Dist- Raigad")

        self.click_element(By.ID, "male")

        for days in ["monday", "tuesday", "thursday", "friday", "saturday"]:
            self.checkbox(days)

        self.select_dropdown(By.ID, "country", "India")

        self.select_dropdown(By.ID, "colors", "Blue")

        self.select_dropdown(By.ID, "animals", "Dog")

        # Normal Date picker
        self.send_keys(By.ID, "datepicker", "01/01/2023")

        # Date picker handling
        self.click_element(By.ID, "txtDate")
        self.select_dropdown(By.CLASS_NAME, "ui-datepicker-year", "2020")  # Select year
        self.select_dropdown(
            By.CLASS_NAME, "ui-datepicker-month", "Oct"
        )  # Select month
        self.click_element(By.XPATH, "//a[@data-date='16']")  # Select date

        # Select a Date Range
        self.send_keys(By.ID, "start-date", "01/01/2023")  # Start date
        self.send_keys(By.ID, "end-date", "12/31/2023")  # End date
        self.click_element(By.CLASS_NAME, "submit-btn")
        time.sleep(1)

        # Upload file
        file_input = driver.find_element(
            By.ID, "singleFileInput"
        )  # Locate the "Choose File" input field
        file_path = r"C:\Users\user\Desktop\Omkar Kadam_selenium\PC Config.txt"  # Provide the absolute path of the file
        file_input.send_keys(file_path)
        # Click the upload button
        upload_button = driver.find_element(
            By.XPATH, "//form[@id='singleFileForm']//button[@type='submit']"
        )
        # //form[@id = 'singleFileForm'] → Finds the < form > with id="singleFileForm".
        # //button[@type = 'submit'] → Finds the submit button inside that form.
        upload_button.click()
        print("File uploaded successfully!")

        # Pagination
        self.select_products(["Television", "Action Camera"])

        # Sroll down comboBox
        self.select_dropdown(By.ID, "dropdown", "Item 16")
        print("ComboBox scrolled successfully")

        # Footer Links
        self.click_element(By.LINK_TEXT, "Download Files")
        print("LinkTest clicked successfully")

        # Download Files
        self.send_keys(By.ID, "inputText", "Tesing Files")  # Enter text into txt file
        self.click_element(By.ID, "generateTxt")  # Generate txt file
        self.click_element(By.ID, "txtDownloadLink")  # Click link to download txt file

        time.sleep(1)
        self.driver.save_screenshot("Registration Form.png")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

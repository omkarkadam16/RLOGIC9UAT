from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as ex
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time


class SeleniumHelper:
    def __init__(self, driver):
        """
        Initialize the SeleniumHelper class with a WebDriver instance.
        :param driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def normal_click(self, by, value):
        """
        Click an element when it becomes clickable.
        :param by: Locator strategy (By.ID, By.NAME, etc.)
        :param value: Locator value
        """
        self.wait.until(EC.element_to_be_clickable((by, value))).click()

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
        input_field = self.wait.until(EC.visibility_of_element_located((by, value)))
        input_field.clear()
        input_field.send_keys(text)
        time.sleep(2)  # Allow time for suggestions to appear
        suggestions = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-menu-item"))
        )
        for i in suggestions:
            if text.upper() in i.text.upper():
                i.click()
                print("Selected autocomplete option:", text)
                return  # <-- this just exits the method early
        input_field.send_keys(Keys.DOWN)
        input_field.send_keys(Keys.ENTER)
        print("Selected autocomplete option using keyboard:", text)

    def click_element_with_retry(self, by, value, max_attempts=3):
        """Click an element with retry logic and JS fallback."""
        attempt = 0
        element = None

        while attempt < max_attempts:
            try:
                element = self.wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
                print(f"[SUCCESS] Clicked element: {value}")
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

            # JavaScript Click Fallback
            if element:
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    print(f"[SUCCESS] Clicked element using JavaScript: {value}")
                    return True
                except ex.JavascriptException as js_error:
                    print(
                        f"[ERROR] JavaScript click failed due to {type(js_error).__name__}"
                    )

            attempt += 1

        print(f"[ERROR] Failed to click element {value} after {max_attempts} attempts.")
        return False

    def click_element(self, by, value, retries=2):
        for attempt in range(retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
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

    def close_popups(self):
        """
        Close unexpected popups dynamically.
        """
        try:
            close_button = self.driver.find_element(By.CLASS_NAME, "close")
            close_button.click()
        except:
            pass  # No popup found

    def switch_frames(self, element_id):
        driver = self.driver
        driver.switch_to.default_content()  # Reset to main page
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            try:
                driver.switch_to.frame(iframe)
                driver.find_element(By.ID, element_id)  # Just try finding the element
                print(f"Switched to iframe containing element: {element_id}")
                return True  # If found, return True
            except NoSuchElementException:
                driver.switch_to.default_content()  # Reset to check the next frame

        print(f"Element with ID '{element_id}' not found in any iframe.")
        return False  # Element not found in any iframe

    def get_text(self, by_type, element_id):
        """Extracts text from an element"""
        try:
            element = self.wait.until(
                EC.presence_of_element_located((by_type, element_id))
            )
            return element.text.strip() if element.text else None
        except Exception as e:
            print(f"[ERROR] Could not extract text from {element_id}: {str(e)}")
            return None

    def checkbox(self, checkbox_id):
        """Selects a checkbox if not already selected and verifies it."""
        checkbox = self.driver.find_element(By.ID, checkbox_id)
        if not checkbox.is_selected():
            checkbox.click()
            print(f"Selected checkbox: {checkbox_id}")

    def paginate_select(self, product_names):
        """
        Selects checkboxes for the given product names from a paginated table.

        Parameters:
        product_names (set or list): A set/list of product names to be selected.
        """

        for i in range(1, 4):  # Iterate through pagination pages 1 to 3
            self.click_element(
                By.XPATH, f"//*[@id='pagination']/li[{i}]/a"
            )  # Click on page number
            time.sleep(2)  # Wait for the table to update

            # Iterate through all rows in the product table
            for row in self.driver.find_elements(
                By.XPATH, "//table[@id='productTable']/tbody/tr"
            ):
                name = row.find_element(
                    By.XPATH, "./td[2]"
                ).text.strip()  # Extract product name

                if name in product_names:  # Check if product is in the desired list
                    row.find_element(
                        By.XPATH, "./td[4]/input"
                    ).click()  # Click checkbox
                    print(f"✅ Selected '{name}'")

                    product_names.remove(name)  # Remove selected product from list

                    if not product_names:  # Exit function if all products are selected
                        return

    def handle_popup(self, button_text="OK"):
        try:
            # Wait for the popup button with the given text
            popup_ok_button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//div[contains(@class, 'ui-dialog')]//button[text()='{button_text}']",
                    )
                )
            )
            popup_ok_button.click()
            print(f"Popup with button '{button_text}' handled successfully.")
            return True
        except ex.TimeoutException:
            print(f"Popup with button '{button_text}' not found.")
            return False

    def send_keys_alert(self, by, value, text):
        for attempt in range(3):
            try:
                print(f"[INFO] Attempt {attempt + 1}: Entering text...")
                element = self.wait.until(EC.visibility_of_element_located((by, value)))
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
                print(f"[WARNING]Error : {type(e)} occurred. Retrying...")
                time.sleep(1)
        return False

    def handle_alert(self):
        """Check for an alert and handle it if present."""
        try:
            self.wait.until(EC.alert_is_present())  # Small delay to allow alert to appear
            alert = self.driver.switch_to.alert
            print(f"[ALERT] Detected: {alert.text}")
            alert.accept()
            print("[ALERT] Alert accepted.")
            return True
        except ex.NoAlertPresentException:
            print("[INFO] No alert found. Continuing execution...")
            return False

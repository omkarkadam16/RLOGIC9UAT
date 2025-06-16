from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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
        """
        Send text to an input field when it becomes visible.
        :param by: Locator strategy
        :param value: Locator value
        :param text: Text to be entered
        """
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        if element.is_enabled():
            element.clear()
            element.send_keys(text)
        else:
            raise Exception(f"Element located by ({by}, {value}) is not enabled.")

    def select_dropdown(self, by, value, option_text):
        """
        Select an option from a dropdown by visible text.
        :param by: Locator strategy
        :param value: Locator value
        :param option_text: Option text to select
        """
        self.wait.until(EC.visibility_of_element_located((by, value)))
        dropdown = Select(self.driver.find_element(by, value))
        dropdown.select_by_visible_text(option_text)

    def autocomplete_select(self, by, value, text):
        """
        Select an autocomplete suggestion based on input text.
        :param by: Locator strategy
        :param value: Locator value
        :param text: Text to input and search in suggestions
        """
        input_field = self.wait.until(EC.visibility_of_element_located((by, value)))
        input_field.clear()
        input_field.send_keys(text)
        time.sleep(2)  # Allow time for suggestions to appear
        suggestions = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-menu-item"))
        )
        for suggestion in suggestions:
            if text.upper() in suggestion.text.upper():
                suggestion.click()
                return
        input_field.send_keys(Keys.DOWN)
        input_field.send_keys(Keys.ENTER)

    def click_element(self, by, value, max_attempts=3):
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

    def click_element_simple(self, by, value, retries=2):
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
        """
        Switch to the iframe that contains a specific element.
        Returns True if successful, False otherwise.
        """
        self.driver.switch_to.default_content()  # Reset to main page

        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")

        for iframe in iframes:
            self.driver.switch_to.frame(iframe)
            try:
                if self.driver.find_element(By.ID, element_id):
                    print(f"Switched to iframe containing element: {element_id}")
                    return True  # Successfully found the element inside this iframe
            except NoSuchElementException:
                self.driver.switch_to.default_content()  # Go back to main content before checking next iframe

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

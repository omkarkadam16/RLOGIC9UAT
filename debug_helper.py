from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as ex
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
        element.clear()
        element.send_keys(text)

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

    def hover_over_element(self, by, value):
        """
        Hover over an element.
        :param by: Locator strategy
        :param value: Locator value
        """
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        ActionChains(self.driver).move_to_element(element).perform()

    def right_click(self, by, value):
        """
        Perform a right-click (context click) on an element.
        :param by: Locator strategy
        :param value: Locator value
        """
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        ActionChains(self.driver).context_click(element).perform()

    def drag_and_drop(self, source_by, source_value, target_by, target_value):
        """
        Drag an element from source and drop it on target.
        :param source_by: Source element locator strategy
        :param source_value: Source element locator value
        :param target_by: Target element locator strategy
        :param target_value: Target element locator value
        """
        source = self.wait.until(
            EC.visibility_of_element_located((source_by, source_value))
        )
        target = self.wait.until(
            EC.visibility_of_element_located((target_by, target_value))
        )
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def handle_alert(self, action="accept"):
        """
        Handle JavaScript alerts (accept or dismiss).
        :param action: "accept" to confirm, "dismiss" to cancel
        """
        alert = self.wait.until(EC.alert_is_present())
        if action.lower() == "accept":
            alert.accept()
        elif action.lower() == "dismiss":
            alert.dismiss()

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
        print(
            f"No matching suggestion found for '{text}'. Assuming the last suggestion was selected."
        )

    def click_element_while_loop(self, by, value, max_attempts=3):
        """
        Click an element with retry logic and JavaScript fallback.
        :param by: Locator strategy
        :param value: Locator value
        :param max_attempts: Maximum retry attempts before failing
        """
        attempt = 0
        element = None
        while attempt < max_attempts:
            try:
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
                    f"Attempt {attempt + 1}: Failed to click element {value} due to {type(e).__name__}. Retrying..."
                )
                time.sleep(1)

            # JavaScript Click Fallback
            try:
                if element:
                    self.driver.execute_script("arguments[0].click();", element)
                    print(f"Successfully clicked element using JavaScript: {value}")
                    return True
            except ex.JavascriptException as js_error:
                print(
                    f"Attempt {attempt + 1}: JavaScript click failed due to {type(js_error).__name__}"
                )

            attempt += 1

        print(f"Failed to click element {value} after {max_attempts} attempts.")
        return False

    def click_element(self, by, value, retries=2):
        print(f"[INFO] Clicking element: {value} with {retries} retries")
        for attempt in range(retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
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
        except Exception as e:
            print(
                f"[ERROR] Failed to click element: {value}. Exception: {type(e).__name__}"
            )
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
        """Switch to an iframe that contains a specific element"""
        self.driver.switch_to.default_content()
        for iframe in self.driver.find_elements(By.TAG_NAME, "iframe"):
            self.driver.switch_to.frame(iframe)
            try:
                if self.driver.find_element(By.ID, element_id):
                    return True
            except:
                self.driver.switch_to.default_content()
        return False

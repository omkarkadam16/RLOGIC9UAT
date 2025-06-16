from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains

# On completion of this exercise, you can learn the following concepts.
# click()
# driver navigation commands
# getLocation()
# getCss()
# getSize()
# isEnabled()


class ButtonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

    def click_element(self, by, value):
        try:
            self.wait.until(EC.element_to_be_clickable((by, value))).click()
            print(f"Clicked On:{value}")
            return True
        except (
            ex.ElementClickInterceptedException,
            ex.StaleElementReferenceException,
            ex.TimeoutException,
        ):
            return False

    def switch_frames(self, element_id):
        driver = self.driver
        driver.switch_to.default_content()
        iframe = driver.find_elements(By.TAG_NAME, "iframe")
        for i in iframe:
            driver.switch_to.frame(i)
            try:
                if driver.find_element(By.ID, element_id):
                    return True
            except ex.NoSuchElementException:
                driver.switch_to.default_content()
        return False

    def test_button(self):
        driver = self.driver
        driver.get("https://letcode.in/button")
        print("Page Open Successfully")

        # Goto Home and come back here using driver command
        self.click_element(By.ID, "home")
        driver.back()  # Navigate back to the main page
        print("Back to default page")

        # Get the X & Y co-ordinates
        i = self.driver.find_element(By.ID, "position")
        locations = i.location
        x_coordinate = locations["x"]
        y_coordinate = locations["y"]
        print(f"X Coordinate: {x_coordinate}, Y Coordinate: {y_coordinate}")

        # Find the color of the button
        i = self.driver.find_element(By.ID, "color")
        colors = i.value_of_css_property("color")
        print(colors)

        # Find the height & width of the button
        i = self.driver.find_element(By.ID, "property")
        h = i.size
        print(h)

        # Confirm button is disable
        i = self.driver.find_element(By.ID, "isDisabled")
        confirmation = i.is_enabled()
        print(f"Button is enable ?{confirmation}")

        # Click and Hold Button
        button = driver.find_element(
            By.XPATH, "(//h2[normalize-space()='Button Hold!'])[1]"
        )  # Ensure this is the correct link text
        actions = ActionChains(driver)
        actions.click_and_hold(button).perform()
        time.sleep(3)
        print("Click and hold the button")
        # Release the button
        actions.release().perform()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

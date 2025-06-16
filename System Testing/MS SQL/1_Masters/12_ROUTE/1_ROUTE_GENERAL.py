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


class RouteGeneral(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 15)

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
            element.clear()
            element.send_keys(text)
            return True
        except ex.NoSuchElementException:
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
        input_text = self.wait.until(EC.visibility_of_element_located((by, value)))
        input_text.clear()
        input_text.send_keys(text)
        time.sleep(1)
        suggest = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-menu-item"))
        )
        for i in suggest:
            if text.upper() in i.text.upper():
                i.click()
                return
        input_text.send_keys(Keys.DOWN)
        input_text.send_keys(Keys.ENTER)

    def test_Route_General(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        menus = [
            "Transportation",
            "Transportation Master »",
            "Route »",
            "Route - General",
        ]
        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)

        data = [
            {
                "Group": "East --- West",
                "Start": "JAIPUR",
                "End": "DELHI",
                "Via": "HYDERABAD",
                "Controlling": "JAIPUR",
                "From": "JAIPUR",
                "To": "HYDERABAD",
                "Distance": "560",
                "Final": "DELHI",
                "Distance1": "460",
            },
            {
                "Group": "East --- West",
                "Start": "DELHI",
                "End": "AHMEDABAD",
                "Via": "PUNE",
                "Controlling": "DELHI",
                "From": "DELHI",
                "To": "PUNE",
                "Distance": "850",
                "Final": "AHMEDABAD",
                "Distance1": "780",
            },
            {
                "Group": "East --- North",
                "Start": "HYDERABAD",
                "End": "PUNE",
                "Via": "AHMEDABAD",
                "Controlling": "HYDERABAD",
                "From": "HYDERABAD",
                "To": "AHMEDABAD",
                "Distance": "620",
                "Final": "PUNE",
                "Distance1": "870",
            },
            {
                "Group": "East --- North",
                "Start": "AHMEDABAD",
                "End": "DELHI",
                "Via": "BHIWANDI",
                "Controlling": "AHMEDABAD",
                "From": "AHMEDABAD",
                "To": "BHIWANDI",
                "Distance": "620",
                "Final": "DELHI",
                "Distance1": "870",
            },
            {
                "Group": "East --- West",
                "Start": "BHIWANDI",
                "End": "AHMEDABAD",
                "Via": "DELHI",
                "Controlling": "BHIWANDI",
                "From": "BHIWANDI",
                "To": "DELHI",
                "Distance": "1210",
                "Final": "AHMEDABAD",
                "Distance1": "780",
            },
        ]

        for i in data:
            if self.switch_frames("btn_NewRecord"):
                self.click_element(By.ID, "btn_NewRecord")
                time.sleep(2)

            # General Details
            if self.switch_frames("EffectiveFrom"):
                self.send_keys(By.ID, "EffectiveFrom", "01-04-2018")
                self.select_dropdown(By.ID, "RouteTypeId", "Direct")
                self.select_dropdown(By.ID, "RouteGroupId", i["Group"])
                self.autocomplete_select(
                    By.ID, "StartServiceNetworkId-select", i["Start"]
                )
                self.autocomplete_select(By.ID, "EndServiceNetworkId-select", i["End"])
                self.autocomplete_select(By.ID, "ViaServiceNetworkId-select", i["Via"])
                self.autocomplete_select(
                    By.ID, "ControllingLocationId-select", i["Controlling"]
                )

            # Route Service Network
            # Route 1
            if self.switch_frames("FromServiceNetworkId-select"):
                self.autocomplete_select(
                    By.ID, "FromServiceNetworkId-select", i["From"]
                )
                self.autocomplete_select(By.ID, "ToServiceNetworkId-select", i["To"])
                self.send_keys(By.ID, "Distance", i["Distance"])
                self.click_element(By.ID, "btnSave-RouteServiceNetworkSession749")
                time.sleep(1)

                # Route 2
                self.autocomplete_select(By.ID, "ToServiceNetworkId-select", i["Final"])
                self.send_keys(By.ID, "Distance", i["Distance1"])
                self.click_element(By.ID, "btnSave-RouteServiceNetworkSession749")
                time.sleep(1)

            if self.switch_frames("mysubmit"):
                self.click_element(By.ID, "mysubmit")
                time.sleep(2)

        print("All routes created successfully.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

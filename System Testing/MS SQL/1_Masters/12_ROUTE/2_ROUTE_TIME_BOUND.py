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


class RouteTimeBound(unittest.TestCase):
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

    def test_Route_Time_Bound(self):
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
            "Route - Time Bound",
        ]
        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)

        data = [
            {
                "Group": "East --- West",
                "Start": "JAIPUR",
                "End": "HYDERABAD",
                "Via": "DELHI",
                "Controlling": "JAIPUR",
                "From": "JAIPUR",
                "To": "DELHI",
                "Distance": "650",
                "RH": "10",
                "RM": "25",
                "HH": "01",
                "HM": "14",
                "GH": "00",
                "GM": "45",
                "Final": "HYDERABAD",
                "Distance1": "780",
                "RH1": "15",
                "RM1": "45",
                "HH1": "02",
                "HM1": "05",
                "GH1": "01",
                "GM1": "03",
            },
            {
                "Group": "East --- West",
                "Start": "HYDERABAD",
                "End": "AHMEDABAD",
                "Via": "PUNE",
                "Controlling": "HYDERABAD",
                "From": "HYDERABAD",
                "To": "PUNE",
                "Distance": "740",
                "RH": "12",
                "RM": "32",
                "HH": "02",
                "HM": "03",
                "GH": "01",
                "GM": "07",
                "Final": "AHMEDABAD",
                "Distance1": "680",
                "RH1": "10",
                "RM1": "13",
                "HH1": "01",
                "HM1": "54",
                "GH1": "01",
                "GM1": "08",
            },
        ]

        for i in data:
            if self.switch_frames("btn_NewRecord"):
                self.click_element(By.ID, "btn_NewRecord")
                time.sleep(2)

            # General Details
            if self.switch_frames("EffectiveFrom"):
                self.send_keys(By.ID, "EffectiveFrom", "01-04-2018")
                self.select_dropdown(By.ID, "RouteTypeId", "Service")
                self.select_dropdown(By.ID, "RouteGroupId", i["Group"])
                self.autocomplete_select(
                    By.ID, "StartServiceNetworkId-select", i["Start"]
                )
                self.autocomplete_select(By.ID, "EndServiceNetworkId-select", i["End"])
                self.autocomplete_select(By.ID, "ViaServiceNetworkId-select", i["Via"])
                self.autocomplete_select(
                    By.ID, "ControllingLocationId-select", i["Controlling"]
                )
                self.select_dropdown(By.ID, "VehicleTypeId", "15 MT")

            # Route Service Network
            # Route 1
            if self.switch_frames("FromServiceNetworkId-select"):
                self.autocomplete_select(
                    By.ID, "FromServiceNetworkId-select", i["From"]
                )
                self.autocomplete_select(By.ID, "ToServiceNetworkId-select", i["To"])
                self.send_keys(By.ID, "Distance", i["Distance"])
                # Running Time(Hrs/Mins)
                self.send_keys(By.ID, "RunningTimeTimePickerHrs", i["RH"])
                self.send_keys(By.ID, "RunningTimeTimePickerMins", i["RM"])
                # Halt Time(Hrs/Mins)
                self.send_keys(By.ID, "HaltTimeTimePickerHrs", i["HH"])
                self.send_keys(By.ID, "HaltTimeTimePickerMins", i["HM"])
                # Grace Time(Hrs/Mins)
                self.send_keys(By.ID, "GraceTimeTimePickerHrs", i["GH"])
                self.send_keys(By.ID, "GraceTimeTimePickerMins", i["GM"])
                self.click_element(By.ID, "btnSave-RouteServiceNetworkSession754")
                time.sleep(1)

                # Route 2
                self.autocomplete_select(By.ID, "ToServiceNetworkId-select", i["Final"])
                self.send_keys(By.ID, "Distance", i["Distance1"])
                # Running Time(Hrs/Mins)
                self.send_keys(By.ID, "RunningTimeTimePickerHrs", i["RH1"])
                self.send_keys(By.ID, "RunningTimeTimePickerMins", i["RM1"])
                # Halt Time(Hrs/Mins)
                self.send_keys(By.ID, "HaltTimeTimePickerHrs", i["HH1"])
                self.send_keys(By.ID, "HaltTimeTimePickerMins", i["HM1"])
                # Grace Time(Hrs/Mins)
                self.send_keys(By.ID, "GraceTimeTimePickerHrs", i["GH1"])
                self.send_keys(By.ID, "GraceTimeTimePickerMins", i["GM1"])
                self.click_element(By.ID, "btnSave-RouteServiceNetworkSession754")
                time.sleep(2)
                Route_Name = self.driver.find_element(By.ID, "RouteName")
                Route_Name = Route_Name.get_attribute("value")

                self.click_element(By.ID, "mysubmit")
                time.sleep(2)
                print(f"Route {Route_Name} saved successfully")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

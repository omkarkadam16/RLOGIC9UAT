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


class ProfileRights(unittest.TestCase):
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

    def handle_popup(self):
        try:
            # Wait for the popup to appear
            popup_ok_button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[@class='ui-dialog-buttonset']/button[text()='OK']",
                    )
                )
            )
            popup_ok_button.click()
            print("Popup handled successfully.")
            return True
        except ex.TimeoutException:
            print("Popup not found.")
            return False

    def test_profile_rights(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript?ccode=UATASCRIPT")

        self.send_keys(By.ID, "Login", "admin")
        self.send_keys(By.ID, "Password", "Omsgn9")
        self.click_element(By.ID, "btnLogin")

        menus = ["Administration", "User Config »", "User Rights"]
        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)

        data = [
            {"Group": "User Config"},
            {"Group": "Grid Config"},
            {"Group": "Implementation"},
            {"Group": "Link"},
            {"Group": "Geographical Hierarchy"},
            {"Group": "Charge Head"},
            {"Group": "Custom Field"},
            {"Group": "Organisational Hierarchy"},
            {"Group": "Document Setup"},
            {"Group": "GST Master"},
            {"Group": "GST Configuration"},
            {"Group": "Inventory Transaction"},
            {"Group": "Inventory Master"},
            {"Group": "Ledger Creation"},
            {"Group": "Account Master"},
            {"Group": "Bank Master"},
            {"Group": "Finacial Post"},
            {"Group": "Ledger Mapping"},
            {"Group": "Operational Payment"},
            {"Group": "Operational Receipt"},
            {"Group": "Purchase Voucher"},
            {"Group": "Contra"},
            {"Group": "Sales Vouchers"},
            {"Group": "Ledger Openings"},
            {"Group": "Receipt Voucher"},
            {"Group": "Payment Voucher"},
            {"Group": "Journal Voucher"},
            {"Group": "Fund Transfer"},
            {"Group": "Bank Reconciliation"},
            {"Group": "Other Transaction"},
            {"Group": "Booking"},
            {"Group": "Indent / Placement"},
            {"Group": "Outward"},
            {"Group": "Inward"},
            {"Group": "Delivery"},
            {"Group": "Trip Management"},
            {"Group": "Inter Office Memo"},
            {"Group": "Bill"},
            {"Group": "Money Receipt"},
            {"Group": "Contract"},
            {"Group": "Purchase Bill"},
            {"Group": "Track N Trace Reports"},
            {"Group": "Transport SAC HSN Mapping"},
            {"Group": "Common Masters"},
            {"Group": "Party"},
            {"Group": "Customer"},
            {"Group": "Vendor"},
            {"Group": "Consignor/Consignee"},
            {"Group": "Route"},
            {"Group": "Vehicle"},
            {"Group": "Fuel"},
            {"Group": "Preventive Maintainance"},
            {"Group": "Driver"},
            {"Group": "Tyre"},
            {"Group": "Loan"},
            {"Group": "Job Work"},
            {"Group": "Tyre Movement"},
            {"Group": "Renewals"},
            {"Group": "Purchase"},
        ]

        for i in data:
            # General Details
            if self.switch_frames("UserId"):
                self.select_dropdown(By.ID, "UserId", "admin")
                self.select_dropdown(By.ID, "GroupId", i["Group"])
                time.sleep(5)
                self.click_element(By.ID, "LinkchkIsSelectAll")
                self.click_element(By.ID, "btnLinkRightsSave")
                time.sleep(1)

                # Handle the popup
                self.handle_popup()

                print(i["Group"], "Rights saved")

        print("All routes created successfully.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

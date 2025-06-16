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


class DMLoadingAndUnloadingExpenses(unittest.TestCase):
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

    def test_DM_LoadingAndUnloadingExpenses(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        menus = [
            "Finance",
            "Finance Master »",
            "Account Master »".upper(),
            "Finance Rule",
        ]
        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)
            if self.switch_frames("ddl_SearchField"):
                self.select_dropdown(By.ID, "ddl_SearchField", "Rule Name")
                self.send_keys(By.ID, "txt_search", "document mapping")
                self.click_element(By.ID, "btn_Seach")
                self.click_element(By.ID, "dd 4")
                self.click_element(By.PARTIAL_LINK_TEXT, "Edit")
                time.sleep(2)

                # Finance Rule BILL
                if self.switch_frames("Sign"):
                    self.select_dropdown(By.ID, "Sign", "Cr")
                    self.select_dropdown(By.ID, "ProcessId", "BILL")
                    self.autocomplete_select(
                        By.ID, "LedgerId-select", "Loading & Unloading Expense"
                    )
                    self.click_element(By.ID, "ProcessId")
                    self.click_element(By.ID, "btnSave-FinanceRuleConfigSession")
                    time.sleep(2)
                    self.select_dropdown(By.ID, "Sign", "Dr")
                    self.select_dropdown(By.ID, "ProcessId", "BILL")
                    self.autocomplete_select(
                        By.ID, "LedgerId-select", "Loading & Unloading Expense"
                    )
                    self.click_element(By.ID, "ProcessId")
                    self.click_element(By.ID, "btnSave-FinanceRuleConfigSession")
                    print("Finance Rule BILL saved")

                # Finance Rule Vehicle LCC
                if self.switch_frames("Sign"):
                    self.select_dropdown(By.ID, "Sign", "Cr")
                    self.select_dropdown(By.ID, "ProcessId", "Vehicle LCC")
                    self.autocomplete_select(
                        By.ID, "LedgerId-select", "Loading & Unloading Expense"
                    )
                    self.click_element(By.ID, "ProcessId")
                    self.click_element(By.ID, "btnSave-FinanceRuleConfigSession")
                    time.sleep(2)
                    self.select_dropdown(By.ID, "Sign", "Dr")
                    self.select_dropdown(By.ID, "ProcessId", "Vehicle LCC")
                    self.autocomplete_select(
                        By.ID, "LedgerId-select", "Loading & Unloading Expense"
                    )
                    self.click_element(By.ID, "ProcessId")
                    self.click_element(By.ID, "btnSave-FinanceRuleConfigSession")
                    print("Finance Rule Vehicle LCC saved")

                # Finance Rule Trip Settlement
                if self.switch_frames("Sign"):
                    self.select_dropdown(By.ID, "Sign", "Cr")
                    self.select_dropdown(By.ID, "ProcessId", "Trip Settlement")
                    self.autocomplete_select(
                        By.ID, "LedgerId-select", "Loading & Unloading Expense"
                    )
                    self.click_element(By.ID, "ProcessId")
                    self.click_element(By.ID, "btnSave-FinanceRuleConfigSession")
                    time.sleep(2)
                    self.select_dropdown(By.ID, "Sign", "Dr")
                    self.select_dropdown(By.ID, "ProcessId", "Trip Settlement")
                    self.autocomplete_select(
                        By.ID, "LedgerId-select", "Loading & Unloading Expense"
                    )
                    self.click_element(By.ID, "ProcessId")
                    self.click_element(By.ID, "btnSave-FinanceRuleConfigSession")
                    print("Finance Rule Trip Settlement saved")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

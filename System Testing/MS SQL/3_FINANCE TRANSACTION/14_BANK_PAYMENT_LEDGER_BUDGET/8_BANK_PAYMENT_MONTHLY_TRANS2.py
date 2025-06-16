from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager


class Payment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 15)

    def click_element(self, by, value, retry=2):
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by, value))).click()
                print("Clicked on element", value)
                return True
            except (
                ex.ElementClickInterceptedException,
                ex.StaleElementReferenceException,
                ex.TimeoutException,
            ):
                print(
                    f"Retrying click on {by} with value {value}, attempt {i+1}/{retry}"
                )
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
        try:
            input_text = self.wait.until(EC.visibility_of_element_located((by, value)))
            input_text.clear()
            input_text.send_keys(text)
            time.sleep(3)

            suggest = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-menu-item"))
            )
            for i in suggest:
                if text.upper() in i.text.upper():
                    i.click()
                    time.sleep(1)
                    print("Selected autocomplete option:", text)
                    return

            input_text.send_keys(Keys.DOWN)
            input_text.send_keys(Keys.ENTER)
            print("Selected autocomplete option using keyboard:", text)

        except Exception as e:
            print(f"Error in autocomplete_select: {str(e)}")

    def test_Payment_Master(self):
        """Main test case"""
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        for i in (
            "Finance",
            "Finance Transaction »",
            "Payment Voucher »",
            "Bank Payment",
        ):
            self.click_element(By.LINK_TEXT, i)
            print(f"Navigated to {i}.")

        if self.switch_frames("btn_NewRecord"):
            self.click_element(By.ID, "btn_NewRecord")

            if self.switch_frames("OrganizationId"):
                self.select_dropdown(By.ID, "OrganizationId", "HYDERABAD")
                # Calendar
                self.click_element(By.CLASS_NAME, "ui-datepicker-trigger")
                self.select_dropdown(By.CLASS_NAME, "ui-datepicker-month", "Jul")
                self.select_dropdown(By.CLASS_NAME, "ui-datepicker-year", "2024")
                self.click_element(By.XPATH, "//a[text()='15']")

                # Header Ledger Info
                self.autocomplete_select(
                    By.ID, "LedgerVoucherSubledgerMainSession-select", "SBI Bank"
                )
                self.click_element(By.ID, "btnHeaderShowLedgerBalance")
                time.sleep(2)

            # Voucher Ledger Details
            self.autocomplete_select(
                By.ID,
                "LedgerPartyVoucherLegderSubledgerSessionName-select",
                "Electricity Expenses",
            )
            self.click_element(By.ID, "btnHeaderShowLedgerBalance")
            time.sleep(2)
            self.send_keys(By.ID, "Debit", "5000")
            self.send_keys(By.ID, "Narration", "BILL PAID")

            # Adjustment Details
            self.autocomplete_select(
                By.ID, "AnalysisHeadId-select", "HYD-ANALYSIS HEAD"
            )
            self.click_element(
                By.ID,
                "btnSave-VoucherLedgerCollectionSession310VoucherLedgerAnalysisSession",
            )
            self.click_element(By.XPATH, "(//a[normalize-space()='Cost Center'])[1]")
            if self.switch_frames("CostCenterId-select"):
                self.autocomplete_select(By.ID, "CostCenterId-select", "HYDERABAD")
                time.sleep(1)
                self.click_element(
                    By.ID,
                    "btnSave-VoucherLedgerCollectionSession310VoucherLedgerCostCenterSession",
                )
                time.sleep(2)
            self.click_element(By.ID, "btnSave-VoucherLedgerCollectionSession310")
            time.sleep(3)

            # Update Narration
            self.send_keys(By.XPATH, "(//textarea[@id='Narration'])[2]", "BILL PAID")
            self.click_element(By.ID, "UpdateNarration")

            # Payment Details
            self.send_keys(By.ID, "PaymentPaidTo", "ABCD PVT LTD")
            self.send_keys(By.ID, "ChequeNo", "1234567890")

            # Submit Payment
            self.click_element(By.ID, "mysubmit")
            print("Advanced Payment submitted successfully.")
            time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

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
            "Journal Voucher »",
            "JV (Other than Cash & Bank)",
        ):
            self.click_element(By.LINK_TEXT, i)
            print(f"Navigated to {i}.")

        if self.switch_frames("btn_NewRecord"):
            self.click_element(By.ID, "btn_NewRecord")

            if self.switch_frames("OrganizationId"):
                self.select_dropdown(By.ID, "OrganizationId", "DELHI")
                # Calendar
                self.send_keys(By.ID, "DocumentDate", "11-06-2024")

                # LedgerName Info
                self.autocomplete_select(
                    By.ID, "LedgerVoucherLegderSubledgerSession-select", "Cash In Hand"
                )
                self.send_keys(By.ID, "Credit", "3000")
                self.click_element(By.ID, "btnShowLedgerBalance")
                time.sleep(2)
                self.click_element(By.ID, "btnSave-VoucherLedgerCollectionSession241")

            # SubLedgerName Info
            self.autocomplete_select(
                By.ID, "SubLedgerVoucherLegderSubledgerSession-select", "INTER INDIA"
            )
            self.click_element(By.ID, "btnShowLedgerBalance")
            time.sleep(2)
            self.send_keys(By.ID, "Debit", "3000")
            self.send_keys(By.ID, "Narration", "Payment of Rent")

            # Adjustment Details
            self.click_element(
                By.XPATH, "(//a[normalize-space()='Adjustment Details'])[1]"
            )
            if self.switch_frames("BillRefTypeId"):
                time.sleep(1)
                self.click_element(
                    By.ID,
                    "btnSave-VoucherLedgerCollectionSession241VoucherLedgerBillRefSession",
                )
                time.sleep(2)

            # TDS Details
            self.click_element(By.XPATH, "(//a[normalize-space()='TDS Details'])[1]")
            if self.switch_frames("TDSPaymentNatureId"):
                self.select_dropdown(By.ID, "TDSPaymentNatureId", "Payment of Rent")
            self.click_element(By.ID, "btnSave-VoucherLedgerCollectionSession241")
            time.sleep(3)

            # Update Narration
            self.send_keys(
                By.XPATH, "(//textarea[@id='Narration'])[2]", "Payment of Rent"
            )
            self.click_element(By.ID, "UpdateNarration")
            time.sleep(2)

            # Submit Payment
            self.click_element(By.ID, "mysubmit")
            time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

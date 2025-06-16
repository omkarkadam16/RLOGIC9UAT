import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import unittest
import time
from selenium.common import exceptions as ex
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class EntityRelation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

    def send_keys(self, by, value, text):
        """Send text to an input field when it becomes visible."""
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        if element.is_enabled():
            element.clear()
            element.send_keys(text)
        else:
            raise Exception(f"Element located by ({by}, {value}) is not enabled.")

    def switch_frames(self, element_id):
        self.driver.switch_to.default_content()
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            self.driver.switch_to.frame(iframe)
            try:
                if self.driver.find_element(By.ID, element_id):
                    return True
            except ex.NoSuchElementException:
                self.driver.switch_to.default_content()
        return False

    def click_element(self, by, value, retries=2):
        """Click an element, retrying if necessary."""
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

    def test_master(self):
        self.driver.get("http://45.120.137.239/Rlogic9MGLN")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "OMSGN9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful")

        for links in [
            "Administration",
            "R-Logic.9 Admin »",
            "Implementation »",
            "Entity Relation",
        ]:
            self.click_element(By.LINK_TEXT, links)

        if self.switch_frames("LinkId-select"):
            element = self.driver.find_element(By.ID, "LinkId-select")
            element.send_keys("JV (Other than Cash & Bank)")
            time.sleep(2)
            element.send_keys(Keys.TAB)
            print("JV (Other than Cash & Bank")

            # Read Sheet1 from Excel
            df_sheet1 = pd.read_excel("JV(Cash & Bank).xlsx", sheet_name="Sheet1")

            for index, row in df_sheet1.iterrows():
                try:
                    print(
                        f"Processing AsmQualifiedName (Sheet1): {row['AsmQualifiedName']}"
                    )

                    # Check if the value is not NaN before sending keys
                    if pd.notna(row["AsmQualifiedName"]):
                        self.send_keys(
                            By.ID, "AsmQualifiedName", row["AsmQualifiedName"]
                        )

                    if pd.notna(row["Entity Code"]):
                        self.send_keys(By.ID, "EntityCode", row["Entity Code"])

                    if pd.notna(row["Entity Name"]):
                        self.send_keys(By.ID, "EntityName", row["Entity Name"])

                    if pd.notna(row["Parent Entity Code"]):
                        self.send_keys(
                            By.ID, "ParentEntityCode", row["Parent Entity Code"]
                        )

                    if pd.notna(row["Primary Group Column"]):
                        self.send_keys(
                            By.ID, "PrimaryGroupColumns", row["Primary Group Column"]
                        )

                    if pd.notna(row["Property Name"]):
                        self.send_keys(By.ID, "PropertyName", row["Property Name"])

                    # Save button click for Sheet1
                    if self.switch_frames("btnSave-ImportEntityColumnSessionName782"):
                        self.click_element(
                            By.ID, "btnSave-ImportEntityColumnSessionName782"
                        )
                        time.sleep(2)
                        df_sheet1.at[index, "Status"] = "Passed"
                    else:
                        df_sheet1.at[index, "Status"] = "Failed"

                except Exception as e:
                    print(
                        f"Failed to process AsmQualifiedName {row['AsmQualifiedName']} (Sheet1): {str(e)}"
                    )

            # Save updated Sheet1 back to Excel
            df_sheet1.to_excel("JV(Cash & Bank).xlsx", index=False, engine="openpyxl")

            # Read Sheet2 from Excel
            df_sheet2 = pd.read_excel("JV(Cash & Bank).xlsx", sheet_name="Sheet2")

            for index, row in df_sheet2.iterrows():
                try:
                    print(f"Processing Entity Code (Sheet2): {row['Entity Code']}")

                    # Check if the value is not NaN before sending keys
                    if pd.notna(row["Entity Code"]):
                        self.send_keys(By.ID, "EntityCode", row["Entity Code"])

                    if pd.notna(row["Entity Property"]):
                        self.send_keys(By.ID, "EntityProperty", row["Entity Property"])

                    if pd.notna(row["Id For Selection Criteria"]):
                        self.send_keys(
                            By.ID,
                            "IdSelectionCriteria",
                            row["Id For Selection Criteria"],
                        )

                    if pd.notna(row["Import Column Name"]):
                        self.send_keys(
                            By.ID, "ImportColumnName", row["Import Column Name"]
                        )

                    if pd.notna(row["Foreign Entity Name"]):
                        self.send_keys(
                            By.ID, "ForeignEntityName", row["Foreign Entity Name"]
                        )

                    if pd.notna(row["Foreign Key Name"]):
                        self.send_keys(By.ID, "ForeignKeyName", row["Foreign Key Name"])

                    if pd.notna(row["Foreign Display Name"]):
                        self.send_keys(
                            By.ID, "ForeignDisplayName", row["Foreign Display Name"]
                        )

                    # Save button click for Sheet2
                    if self.switch_frames(
                        "btnSave-ImportEntityColumnMapSessionName782"
                    ):
                        self.click_element(
                            By.ID, "btnSave-ImportEntityColumnMapSessionName782"
                        )
                        time.sleep(2)
                        df_sheet2.at[index, "Status"] = "Passed"
                    else:
                        df_sheet2.at[index, "Status"] = "Failed"
                        print(
                            f"Failed to switch to the correct frame for {row['Entity Code']}"
                        )

                except Exception as e:
                    print(
                        f"Failed to process Entity Code {row['Entity Code']} (Sheet2): {str(e)}"
                    )

            # Save updated Sheet2 back to Excel
            df_sheet2.to_excel("JV(Cash & Bank).xlsx", index=False, engine="openpyxl")

            print(
                "✅ JV(Cash & Bank) Sheet2 Completed! Check JV(Cash & Bank).xlsx for results."
            )


# If you want to run the test
if __name__ == "__main__":
    unittest.main()

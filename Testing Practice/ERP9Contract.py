from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import unittest, time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager

class Contract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 15)
        
    def click_element(self,by,value,retry = 3):
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by,value))).click()
        
                return True
            except (ex.ElementClickInterceptedException,ex.StaleElementReferenceException):
                print(f"attempt{i+1}/{retry}") 
                time.sleep(1)           
        try:
            a = self.driver.find_element(by,value)
            self.driver.execute_script("arguments[0].click();",a)
            return True
        except ex.JavascriptException:
            return False
        
    
    def send_keys(self,by,value,text):
        try:
            i = self.wait.until(EC.element_to_be_clickable((by,value)))
            i.clear()
            i.send_keys(text)
            print("Entered text value = ", text)
            return True
        except(ex.ElementClickInterceptedException,ex.NoSuchElementException,ex.StaleElementReferenceException):
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
                    
                
    def autoselection(self,by,value,text):
        a = self.wait.until(EC.visibility_of_element_located((by,value)))
        a.clear()
        a.send_keys(text)
        time.sleep(2)
        
        i = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"ui-menu-item")))
        for j in i:
            if text.upper() in j.text.upper():
                j.click()
                return
            
        a.send_keys(Keys.DOWN)
        a.send_keys(Keys.ENTER)    
    
    
    def test_contract(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/")
        
        print("Logging in...")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")
        
        
        for i in (
            "Transportation",
            "Transportation Transaction »",
            "Contract »",
            "Customer Contract",
        ):
            self.click_element(By.LINK_TEXT,i)
            print("Navigate to :",i)
            
            if self.switch_frames("btn_NewRecord"):
                self.click_element(By.ID, "btn_NewRecord")

            # Document Details
            if self.switch_frames("OrganizationId"):
                self.select_dropdown(By.ID, "OrganizationId", "DELHI")
     
     
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
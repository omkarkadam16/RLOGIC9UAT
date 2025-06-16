import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import base64

# Set Chrome options for headless (no UI)
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

# Create driver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the page you want to print
driver.get("http://192.168.0.72/Rlogic9RLS/")
time.sleep(2)

# Print to PDF
pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {})
# This decodes the base64 data and saves it as a real PDF file named page.pdf.
with open("page.pdf", "wb") as f: #wb = write binary
    f.write(base64.b64decode(pdf_data['data'])) #base64.b64decode(pdf_data['data'])

print("PDF saved as output.pdf")

# Close the browser
driver.quit()

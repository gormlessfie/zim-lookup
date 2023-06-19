from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from openpyxl import Workbook
from datetime import datetime

def wait_for_content(driver, element):
    # Wait for the JavaScript to fill in elements
    wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
    element_locator = (By.XPATH, element)
    wait.until(EC.presence_of_element_located(element_locator))
    
    
    
    
# Setup excel workbook
workbook = Workbook()
worksheet = workbook.active
worksheet.title = "Shipping Date Changes"


# Create a new instance of the Firefox driver
driver = webdriver.Firefox()
driver.get('https://www.msc.com/en/track-a-shipment')

# Get list of MSC tracking numbers
list_tracking_numbers = open("list-trackers.txt", "r").readlines()

# Select booking number search option


for entry in list_tracking_numbers: 


workbook.save("output/zim_shipping_dates_changes.xlsx")

driver.close()
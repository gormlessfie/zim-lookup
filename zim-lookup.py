import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from openpyxl import Workbook
from datetime import datetime
import time

def wait_for_content(driver, element):
    # Wait for the JavaScript to fill in elements
    wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
    element_locator = (By.XPATH, element)
    wait.until(EC.presence_of_element_located(element_locator))
    
def accept_cookies_banner(driver):
    wait_for_content(driver, "//button[@id='onetrust-accept-btn-handler']")
    accept_button = driver.find_element(By.XPATH, "//button[@id='onetrust-accept-btn-handler']")
    accept_button.click()
    
def search(driver, tracker):
    wait_for_content(driver, "//input[@id='shipment-main-search-2']")
    input_box = driver.find_element(By.XPATH, "//input[@id='shipment-main-search-2']")
    input_box.send_keys(tracker)
    input_box.send_keys(Keys.ENTER)
    
    wait_for_content(driver, "//input[@class='btn btn-primary chips-search-button']")
    track_shipment_button = driver.find_element(By.XPATH, "//input[@class='btn btn-primary chips-search-button']")
    time.sleep(1)
    track_shipment_button.click()
    
def retrieve_eta_date(driver):
    wait_for_content(driver, "//div[@id='etaDate']")
    eta_date = driver.find_element(By.XPATH, "//div[@id='etaDate']")
    
    return format_date(eta_date)
    
def format_date(date):
    # Parse the input string into a datetime object
    date_object = datetime.strptime(date, "%d-%M-%Y")

    # Format the date as "month/day"
    formatted_date = date_object.strftime("%m/%d")
    return formatted_date
    
# Setup excel workbook
workbook = Workbook()
worksheet = workbook.active
worksheet.title = "Shipping Date Changes"

# Create a new instance of the Firefox driver
driver = uc.Chrome(use_subprocess=True)
driver.get('https://www.zim.com/tools/track-a-shipment')

# Get list of MSC tracking numbers
list_tracking_numbers = open("list-trackers.txt", "r").readlines()

# Accepts cookies banner
accept_cookies_banner(driver)

for entry in list_tracking_numbers: 
    # Search using entry
    search(driver, entry)
    date = retrieve_eta_date(driver)
    row = [entry.strip(), date]
    worksheet.append(row)

workbook.save("output/zim_shipping_dates_changes.xlsx")

driver.close()
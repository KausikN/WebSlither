'''
A python browser and web automation tool using selenium
'''

# Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

# Util Functions
def delay(delayTime=1):
    time.sleep(delayTime)

# Main Functions
def FirefoxDriver():
    return webdriver.Firefox(executable_path="SeleniumDrivers/geckodriver.exe")

def ChromeDriver():
    return webdriver.Chrome(executable_path="SeleniumDrivers/chromedriver.exe")

def EdgeDriver():
    return webdriver.Edge(executable_path="SeleniumDrivers/msedgedriver.exe")

def gotoURL(driver, url):
    driver.get(url)
    return driver

def getTitle(driver):
    return driver.title

def destroyDriver(driver):
    driver.close()

def WaitTillLoad(driver, element_present, timeout=3):
    print("Waiting for page to load...")
    try:
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load.")
        return False
    finally:
        print("Page loaded!")
        return True
    return True

# Driver Code

# Setup Driver
# driver = FirefoxDriver()

# # Goto Website
# driver = gotoURL(driver, "http://www.python.org")
# print("In", getTitle(driver))

# # Find elements
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# print("Search Found:", ("No results found." not in driver.page_source))

# # Destroy Driver
# destroyDriver(driver)
'''
Web Slither Commands
'''

# Imports
from WebSlither import *
from functools import partial

##############################################################################################################################

# Main Driver Vars
DRIVER = None
DELAY_SCALE = 1.0

LOAD_TIMEOUT = 3.0

VERBOSE = True

# Driver Functions
def SetDriverConnector(driverName='firefox'):
    global DRIVER

    driverName = driverName.strip().lower()[:1]
    if driverName == 'c':
        if VERBOSE: print("Initialising Chrome Driver...")
        DRIVER = ChromeDriver()
    if driverName == 'e':
        if VERBOSE: print("Initialising Edge Driver...")
        DRIVER = EdgeDriver()
    if VERBOSE: print("Initialising Firefox Driver...")
    DRIVER = FirefoxDriver()

def SetDelayScale(scale):
    global DELAY_SCALE
    DELAY_SCALE = scale
    if VERBOSE: print("Delay Scale set to", DELAY_SCALE)

def Delay(delayVal=1.0, scale=1.0):
    if VERBOSE: print("Delaying by", delayVal*scale, "seconds...")
    delay(delayVal*scale)

def GotoURL(url):
    global DRIVER
    DRIVER.get(url)
    if VERBOSE: print("Went to", DRIVER.title)

def WriteDataToField(fieldType, fieldName, value):
    global DRIVER

    fieldType = fieldType.strip().lower()[:1]

    # Wait till field loads
    fieldTypeModule = By.ID
    if fieldType == 'c':
        fieldTypeModule = By.CLASS_NAME
    elif fieldType == 'n':
        fieldTypeModule = By.NAME
    
    if WaitTillLoad(DRIVER, EC.presence_of_element_located((fieldTypeModule, fieldName)), LOAD_TIMEOUT):
        # After loading
        field = DRIVER.find_element(by=fieldTypeModule, value=fieldName)
        field.clear()
        field.send_keys(value)
        field.send_keys(Keys.RETURN)
        if VERBOSE: print("Written", value, "to", fieldType + ":" + fieldName, "successfully.")
    else:
        if VERBOSE: print("Writing", value, "to", fieldType + ":" + fieldName, "failed due to TIMEOUT ERROR.")

def ReadDataFromField(fieldType, fieldName):
    global DRIVER

    fieldType = fieldType.strip().lower()[:1]

    # Wait till field loads
    fieldTypeModule = By.ID
    if fieldType == 'c':
        fieldTypeModule = By.CLASS_NAME
    elif fieldType == 'n':
        fieldTypeModule = By.NAME
    
    if WaitTillLoad(DRIVER, EC.presence_of_element_located((fieldTypeModule, fieldName)), LOAD_TIMEOUT):
        # After loading
        field = DRIVER.find_element(by=fieldTypeModule, value=fieldName)
        readData = field.get_attribute("innerHTML")
        if VERBOSE: print("Read", "from", fieldType + ":" + fieldName, "successfully.")
        print("Data in", fieldType + ":" + fieldName, "->", readData)
    else:
        if VERBOSE: print("Reading", "from", fieldType + ":" + fieldName, "failed due to TIMEOUT ERROR.")

def ClickField(fieldType, fieldName):
    global DRIVER

    fieldType = fieldType.strip().lower()[:1]

    # Wait till field loads
    fieldTypeModule = By.ID
    if fieldType == 'c':
        fieldTypeModule = By.CLASS_NAME
    elif fieldType == 'n':
        fieldTypeModule = By.NAME
    
    if WaitTillLoad(DRIVER, EC.presence_of_element_located((fieldTypeModule, fieldName)), LOAD_TIMEOUT):
        # After loading
        field = DRIVER.find_element(by=fieldTypeModule, value=fieldName)
        field.click()
        if VERBOSE: print("Clicked", fieldType + ":" + fieldName, "successfully.")
    else:
        if VERBOSE: print("Clicking", fieldType + ":" + fieldName, "failed due to TIMEOUT ERROR.")

def PressKeyToField(fieldType, fieldName, key):
    global DRIVER

    # Check if key is valid
    key = key.upper().replace(' ', '_')
    if key not in dir(Keys):
        if VERBOSE: print("Key", key, "is invalid.")
        return

    fieldType = fieldType.strip().lower()[:1]

    # Wait till field loads
    fieldTypeModule = By.ID
    if fieldType == 'c':
        fieldTypeModule = By.CLASS_NAME
    elif fieldType == 'n':
        fieldTypeModule = By.NAME
    
    if WaitTillLoad(DRIVER, EC.presence_of_element_located((fieldTypeModule, fieldName)), LOAD_TIMEOUT):
        # After loading
        field = DRIVER.find_element(by=fieldTypeModule, value=fieldName)
        field.send_keys(Keys.__dict__[key])
        if VERBOSE: print("Pressed", key, "to", fieldType + ":" + fieldName, "successfully.")
    else:
        if VERBOSE: print("Pressed", key, "to", fieldType + ":" + fieldName, "failed due to TIMEOUT ERROR.")

def PressKeyToBrowser(key):
    global DRIVER

    # Check if key is valid
    key = key.upper().replace(' ', '_')
    if key not in dir(Keys):
        if VERBOSE: print("Key", key, "is invalid.")
        return

    actions = ActionChains(DRIVER)
    actions.send_keys(Keys.__dict__[key]).perform()
    if VERBOSE: print("Pressed", key, "to", "browser", "successfully.")
        

# Driver Code
'''
Parser for reading and decoding web slither files

WebSlitherFile examples

# {anything}
Comment - not considered while decoding

driver {Firefox/Chrome/Edge/F/C/E}
d {Firefox/Chrome/Edge/F/C/E}
Sets the driver to be used

delayScale 1.0
dS 1.0
Sets the delay scale to 1.0 seconds

delay 0.5
d 0.5
Gives a delay of (0.5)*delayScale

delayA 1.0
dA 1.0
Gives a absolute delay of 1.0 seconds without scale

goto {link}
g {link}
Loads the given link

write i/c/n {id/class/name} {value}
w i/c/n {id/class/name} {value}
Writes the value into those fields

read i/c/n {id/class/name}
r i/c/n {id/class/name}
Reads from the field

click i/c/n {id/class/name}
c i/c/n {id/class/name}
Clicks the field

key i/c/n {id/class/name} {keyName}
k i/c/n {id/class/name} {keyName}
Presses the key mentioned in the field
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

##############################################################################################################################

# Main Parse Vars
COMMAND_MAP = {
    "driver": SetDriverConnector,

    "delayScale": SetDelayScale,
    "delayAbsolute": Delay,
    "delay": Delay,

    "goto": GotoURL,

    "write": WriteDataToField,
    "read": ReadDataFromField,
    "click": ClickField,
    "keyPress": PressKeyToField
}
COMMENT_STR = '#'

# Main Parse Functions
def GetCommandName(val):
    val = val.strip().lower()

    if val in ['driver', 'dr']:
        return 'driver'
    elif val in ['ds', 'delayScale']:
        return 'delayScale'
    elif val in ['da', 'delayabsolute']:
        return 'delayAbsolute'
    elif val in ['d', 'delay']:
        return 'delay'
    elif val in ['g', 'goto']:
        return 'goto'
    elif val in ['w', 'write']:
        return 'write'
    elif val in ['r', 'read']:
        return 'read'
    elif val in ['c', 'click']:
        return 'click'
    elif val in ['k', 'key', 'keypress', 'presskey']:
        return 'keyPress'
    return ""

def GetCommand(cmd, data):
    if cmd == 'driver':
        return partial(COMMAND_MAP[cmd], ' '.join(data))
    elif cmd == 'delayScale':
        return partial(COMMAND_MAP[cmd], float(data[0].strip()))
    elif cmd == 'delayAbsolute':
        return partial(COMMAND_MAP[cmd], float(data[0].strip()), 1.0)
    elif cmd == 'delay':
        return partial(COMMAND_MAP[cmd], float(data[0].strip()), DELAY_SCALE)
    elif cmd == 'goto':
        return partial(COMMAND_MAP[cmd], ' '.join(data))
    elif cmd == 'write':
        return partial(COMMAND_MAP[cmd], data[0], data[1], ' '.join(data[2:]))
    elif cmd == 'read':
        return partial(COMMAND_MAP[cmd], data[0], ' '.join(data[1:]))
    elif cmd == 'click':
        return partial(COMMAND_MAP[cmd], data[0], ' '.join(data[1:]))
    elif cmd == 'keyPress':
        return partial(COMMAND_MAP[cmd], data[0], data[1], ' '.join(data[2:]))
    return None

def ParseWebSlitherData(data):
    # Parse Info
    parsedData = []

    lines = data.split("\n")
    for line in lines:
        # Remove commented part
        if COMMENT_STR in line:
            line = line[:line.find(COMMENT_STR)]
        # Check empty lines
        if line.strip() == "":
            continue

        parsedLine = line.split(' ')
        parsedData.append(parsedLine)

    # Decode Data
    commands = []
    for pL in parsedData:
        cmdName = GetCommandName(pL[0])
        cmd = GetCommand(cmdName, pL[1:])
        commands.append(cmd)
        print(pL)
        print(cmdName)
        print(cmd)
        print()

    return commands

def RunWebSlitherFile(path=None, data=None):
    if data is None:
        data = open(path, 'r').read()

    commands = ParseWebSlitherData(data)
    for cmd in commands:
        cmd()

# Driver Code
# Params
webSlitherPath = 'Examples/DinoGame.ws'
# Params

# RunCode
RunWebSlitherFile(path=webSlitherPath)
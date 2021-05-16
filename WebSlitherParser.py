'''
Parser for reading and decoding web slither files

WebSlitherFile examples

# {anything}
Comment - not considered while decoding

 - {checkpointName}
Adds a checkpoint of name checkpointName

jump {checkpointName}
Jumps the execution to the position of the mentioned checkpointName

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

keybrowser {keyName}
kb {keyName}
Presses the key mentioned in the browser window
'''

# Imports
from WebSlither import *
from WebSlitherCommands import *
from functools import partial

########################################################################################################################
# Main Runtime Vars
CHECKPOINTS = {}
EXECUTION_CURRENT_POSITION = -1

########################################################################################################################
# Main Execution Functions
def SetCheckpoint(name, pos):
    global CHECKPOINTS
    CHECKPOINTS[name] = pos
    if VERBOSE: print("Added CHECKPOINT:", name, "at position", str(pos) + ".")


def JumpToCheckpoint(name):
    global EXECUTION_CURRENT_POSITION
    if name in CHECKPOINTS.keys():
        EXECUTION_CURRENT_POSITION = CHECKPOINTS[name] - 1 # -1 is because of default EXECUTION_CURRENT_POSITION += 1 after every command
        if VERBOSE: print("Jump to CHECKPOINT:", name, "at position", str(CHECKPOINTS[name]), "successful.")
    else:
        if VERBOSE: print("Jump to CHECKPOINT:", name, "failed due to invalid CHECKPOINT.")

########################################################################################################################

# Main Parse Vars
COMMAND_MAP = {
    "CHECKPOINT_SET": SetCheckpoint,
    "CHECKPOINT_JUMP": JumpToCheckpoint,

    "driver": SetDriverConnector,

    "delayScale": SetDelayScale,
    "delayAbsolute": Delay,
    "delay": Delay,

    "goto": GotoURL,

    "write": WriteDataToField,
    "read": ReadDataFromField,
    "click": ClickField,
    "keyPressBrowser": PressKeyToBrowser,
    "keyPress": PressKeyToField
}
COMMENT_STR = '#'

# Main Parse Functions
def GetCommandName(val):
    val = val.strip().lower()

    if val in ['-', 'checkpoint', 'cp']:
        return 'CHECKPOINT_SET'
    elif val in ['jump', 'j']:
        return 'CHECKPOINT_JUMP'

    elif val in ['driver', 'dr']:
        return 'driver'
    elif val in ['ds', 'delayScale']:
        return 'delayScale'
    elif val in ['da', 'delayabsolute', 'delaya']:
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
    elif val in ['kb', 'keybrowser', 'keybrowserpress', 'presskeybrowser']:
        return 'keyPressBrowser'
    elif val in ['k', 'key', 'keypress', 'presskey']:
        return 'keyPress'
    return ""

def GetCommand(cmd, data, pos=-1):
    if cmd == 'CHECKPOINT_SET':
        return partial(COMMAND_MAP[cmd], ' '.join(data), pos)
    elif cmd == 'CHECKPOINT_JUMP':
        return partial(COMMAND_MAP[cmd], ' '.join(data))

    elif cmd == 'driver':
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
    elif cmd == 'keyPressBrowser':
        return partial(COMMAND_MAP[cmd], ' '.join(data))
    elif cmd == 'keyPress':
        return partial(COMMAND_MAP[cmd], data[0], data[1], ' '.join(data[2:]))
    return None

def ParseWebSlitherData(data):
    # Parse Info and Decode Data
    n_ignored_lines = 0

    lines = data.split("\n")
    commands = []
    curLineIndex = 0
    for line in lines:
        line = line.strip()

        # Remove commented part
        if COMMENT_STR in line:
            line = line[:line.find(COMMENT_STR)]
        # Check empty lines
        if line.strip() == "":
            n_ignored_lines += 1
            continue

        parsedLine = line.split(' ')
        cmdName = GetCommandName(parsedLine[0])
        cmd = GetCommand(cmdName, parsedLine[1:], curLineIndex)
        commands.append(cmd)
        print(parsedLine)
        print(cmdName)
        print(cmd)
        print()

        curLineIndex += 1

    return commands

def RunWebSlitherFile(path=None, data=None):
    global EXECUTION_CURRENT_POSITION

    if data is None:
        data = open(path, 'r').read()

    commands = ParseWebSlitherData(data)

    EXECUTION_CURRENT_POSITION = 0
    while(EXECUTION_CURRENT_POSITION < len(commands)):
        commands[EXECUTION_CURRENT_POSITION]()
        EXECUTION_CURRENT_POSITION += 1

# Driver Code
# Params
webSlitherPath = 'Examples/DinoGame.ws'
# Params

# RunCode
RunWebSlitherFile(path=webSlitherPath)
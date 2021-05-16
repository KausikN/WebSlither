'''
WebSlither script for using google translate
'''

# Imports
from WebSlither import *

# Main Functions


# Driver Code
# Params
translateText = 'Paravai'

fromLanguage = 'Tamil'
toLanguage = 'English'

delayScale = 0.5
# Params

# RunCode
# Create Driver
driver = FirefoxDriver()

# Goto Website
googleURL = 'https://www.google.com/'
driver.get(googleURL)
print("Went to", driver.title)

delay(delayScale)

## Search Google Translate
# Find search element (name = 'q') and enter google translate search query and search
googleTranslateSearchText = 'Google Translate'
searchBarName = 'q'

# Wait for page to load
WaitTillLoad(driver, EC.presence_of_element_located((By.NAME, searchBarName)))

# After loading
searchBar = driver.find_element_by_name(searchBarName)
searchBar.clear()
searchBar.send_keys(googleTranslateSearchText)
searchBar.send_keys(Keys.RETURN)

print("Google Translate Search Found:", ("No results found." not in driver.page_source))

delay(delayScale)

## Setup Languages
## Select From Language
print("Selecting From Language...")
fromLangSelectorButtonID = 'tw-sl'

WaitTillLoad(driver, EC.presence_of_element_located((By.ID, fromLangSelectorButtonID)))
fromLangSelectorButton = driver.find_element_by_id(fromLangSelectorButtonID)
fromLangSelectorButton.click()

delay(delayScale/2)

fromLangSelectorTextID = 'sl_list-search-box'

WaitTillLoad(driver, EC.presence_of_element_located((By.ID, fromLangSelectorTextID)))
fromLangSelectorText = driver.find_element_by_id(fromLangSelectorTextID)
fromLangSelectorText.clear()
fromLangSelectorText.send_keys(fromLanguage)
fromLangSelectorText.send_keys(Keys.RETURN)

delay(delayScale)

## Select To Language
print("Selecting To Language...")
toLangSelectorButtonID = 'tw-tl'

WaitTillLoad(driver, EC.presence_of_element_located((By.ID, toLangSelectorButtonID)))
toLangSelectorButton = driver.find_element_by_id(toLangSelectorButtonID)
toLangSelectorButton.click()

delay(delayScale/2)

toLangSelectorTextID = 'tl_list-search-box'

WaitTillLoad(driver, EC.presence_of_element_located((By.ID, toLangSelectorTextID)))
toLangSelectorText = driver.find_element_by_id(toLangSelectorTextID)
toLangSelectorText.clear()
toLangSelectorText.send_keys(toLanguage)
toLangSelectorText.send_keys(Keys.RETURN)

delay(delayScale)

## Enter Text
fromTextID = 'tw-source-text-ta'

WaitTillLoad(driver, EC.presence_of_element_located((By.ID, fromTextID)))
fromText = driver.find_element_by_id(fromTextID)
fromText.clear()
fromText.send_keys(translateText)
fromText.send_keys(Keys.RETURN)

delay(1)

## Get Translated Text
toTextClass = 'Y2IQFc'

WaitTillLoad(driver, EC.presence_of_element_located((By.CLASS_NAME, toTextClass)))
fromText = driver.find_element_by_class_name(toTextClass)
translatedText = str(fromText.get_attribute("innerHTML"))

delay(delayScale)

print()
print("Input Text:", translateText)
print("Translated Text:", translatedText)

# while(True):
#     fromText = driver.find_element_by_class_name(toTextClass)
#     print("Translated Text:", fromText.get_attribute("innerHTML"), "-", fromText.text)

delay(delayScale)

# Destroy Driver
destroyDriver(driver)
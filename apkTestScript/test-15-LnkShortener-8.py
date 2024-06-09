import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'de.hirtenstrasse.michael.lnkshortener'
desired_caps['appActivity'] = 'de.hirtenstrasse.michael.lnkshortener.MainActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(5)

# home page
try:

    # # branch
    # el0 = driver.find_elements_by_id('de.hirtenstrasse.michael.lnkshortener:id/shortenButton')[0]
    # el0.click()
    # time.sleep(3)

    el1 = driver.find_element_by_accessibility_id('More options')
    el1.click()
    time.sleep(3)

    el2 = driver.find_elements_by_id('de.hirtenstrasse.michael.lnkshortener:id/title')[0]
    el2.click()
    time.sleep(3)

    el3 = driver.find_element_by_android_uiautomator('new UiSelector().text("Set Domain")')
    el3.click()
    time.sleep(3)

finally:
    time.sleep(5)
    driver.quit()

'''
{
  "platformName": "Android",
  "platformVersion": "6.0.1",
  "deviceName": "127.0.0.1:7555",
  "noReset": true,
  "appPackage": "de.hirtenstrasse.michael.lnkshortener",
  "appActivity": "de.hirtenstrasse.michael.lnkshortener.MainActivity"
}
'''

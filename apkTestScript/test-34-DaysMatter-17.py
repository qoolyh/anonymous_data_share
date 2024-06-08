import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'com.clover.daysmatter'
desired_caps['appActivity'] = 'com.clover.daysmatter.ui.activity.MainActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(5)

# home page
try:

    el1 = driver.find_element_by_accessibility_id('Add a New Event')
    el1.click()
    time.sleep(3)

    el2 = driver.find_elements_by_id('com.clover.daysmatter:id/icon_category')[0]
    el2.click()

    # # branch1
    # el2 = driver.find_elements_by_id('android:id/title')[0]
    # el2.click()

    # # branch2
    # el2 = driver.find_elements_by_id('com.clover.daysmatter:id/summary_category')[0]
    # el2.click()

    # # branch3
    # el2 = driver.find_elements_by_id('com.clover.daysmatter:id/preference_list_arrow3')[0]
    # el2.click()

finally:
    time.sleep(5)
    driver.quit()

'''
{
  "platformName": "Android",
  "platformVersion": "6.0.1",
  "deviceName": "127.0.0.1:7555",
  "noReset": true,
  "appPackage": "com.clover.daysmatter",
  "appActivity": "com.clover.daysmatter.ui.activity.MainActivity"
}
'''

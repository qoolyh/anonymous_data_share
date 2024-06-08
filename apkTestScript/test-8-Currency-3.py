import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'org.billthefarmer.currency'
desired_caps['appActivity'] = 'org.billthefarmer.currency.Main'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(5)

# home page
try:

    el1 = driver.find_element_by_accessibility_id('Settings')
    el1.click()
    time.sleep(3)

    el2 = driver.find_elements_by_class_name('android.widget.TextView')[10]
    el2.click()

    # # branch1
    # el2 = driver.find_elements_by_class_name('android.widget.TextView')[10]
    # el2.click()

    # # branch2
    # el2 = driver.find_element_by_android_uiautomator('new UiSelector().text("Currency version 1.0")')
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
  "appPackage": "org.billthefarmer.currency",
  "appActivity": "org.billthefarmer.currency.Main"
}
'''

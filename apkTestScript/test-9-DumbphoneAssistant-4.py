import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'com.github.yeriomin.dumbphoneassistant'
desired_caps['appActivity'] = 'com.github.yeriomin.dumbphoneassistant.ManageContactsActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(5)

# home page
try:

    el1 = driver.find_element_by_android_uiautomator('new UiSelector().text("Sim Card")')
    el1.click()
    time.sleep(3)

    el2 = driver.find_element_by_accessibility_id('Delete contact from SIM')
    el2.click()

finally:
    time.sleep(5)
    driver.quit()

'''
{
  "platformName": "Android",
  "platformVersion": "6.0.1",
  "deviceName": "127.0.0.1:7555",
  "noReset": true,
  "appPackage": "com.github.yeriomin.dumbphoneassistant",
  "appActivity": "com.github.yeriomin.dumbphoneassistant.ManageContactsActivity"
}
'''

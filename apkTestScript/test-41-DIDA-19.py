import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'cn.ticktick.task'
desired_caps['appActivity'] = 'com.ticktick.task.activity.MeTaskActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(20)

# template page
try:

    el1 = driver.find_element_by_android_uiautomator('new UiSelector().text("Daily record")')
    el1.click()
    time.sleep(3)

    el2 = driver.find_element_by_accessibility_id('More options')
    el2.click()
    time.sleep(3)

    el3 = driver.find_element_by_android_uiautomator('new UiSelector().text("Re-name")')
    el3.click()

finally:
    time.sleep(5)
    driver.quit()

'''
{
  "platformName": "Android",
  "platformVersion": "6.0.1",
  "deviceName": "127.0.0.1:7555",
  "noReset": true,
  "appPackage": "cn.ticktick.task",
  "appActivity": "com.ticktick.task.activity.MeTaskActivity"
}
'''

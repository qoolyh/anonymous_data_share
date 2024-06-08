import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'free.rm.skytube.extra'
desired_caps['appActivity'] = 'free.rm.skytube.gui.activities.MainActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(10)

# home page
try:

    el1 = driver.find_element_by_android_uiautomator('new UiSelector().text("Feed")')
    el1.click()
    time.sleep(3)

    # # branch1
    # el0 = driver.find_element_by_android_uiautomator('new UiSelector().text("Most Popular")')
    # el0.click()
    # time.sleep(3)
    #
    # el1 = driver.find_element_by_android_uiautomator('new UiSelector().text("Feed")')
    # el1.click()
    # time.sleep(3)

    # # branch2
    # el0 = driver.find_element_by_android_uiautomator('new UiSelector().text("Bookmarks")')
    # el0.click()
    # time.sleep(3)
    #
    # el1 = driver.find_element_by_android_uiautomator('new UiSelector().text("Feed")')
    # el1.click()
    # time.sleep(3)

    el2 = driver.find_elements_by_id('free.rm.skytube.extra:id/importSubscriptionsButton')[0]
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
  "appPackage": "free.rm.skytube.extra",
  "appActivity": "free.rm.skytube.gui.activities.MainActivity"
}
'''

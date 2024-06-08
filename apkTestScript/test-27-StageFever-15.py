import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'com.fr3ts0n.stagefever'
desired_caps['appActivity'] = 'com.fr3ts0n.stagefever.MainActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(5)

# home page
try:

    # # branch1
    # el0 = driver.find_elements_by_id('android:id/up')[0]
    # el0.click()
    # time.sleep(3)

    # # branch2
    # el0 = driver.find_elements_by_id('android:id/home')[0]
    # el0.click()
    # time.sleep(3)

    # # branch3
    # el0 = driver.find_elements_by_id('android:id/action_bar_title')[0]
    # el0.click()
    # time.sleep(3)

    el1 = driver.find_element_by_accessibility_id('More options')
    el1.click()
    time.sleep(3)

    el2 = driver.find_elements_by_id('android:id/title')[0]
    el2.click()
    time.sleep(3)

    el3 = driver.find_element_by_android_uiautomator('new UiSelector().text("Font size of notes [dp]")')
    time.sleep(3)

    # # branch4
    # el3 = driver.find_element_by_android_uiautomator('new UiSelector().text("Font size in dp")')
    # el3.click()

finally:
    time.sleep(5)
    driver.quit()

'''
{
  "platformName": "Android",
  "platformVersion": "6.0.1",
  "deviceName": "127.0.0.1:7555",
  "noReset": true,
  "appPackage": "com.fr3ts0n.stagefever",
  "appActivity": "com.fr3ts0n.stagefever.MainActivity"
}
'''
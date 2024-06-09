import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'me.tsukanov.counter'
desired_caps['appActivity'] = 'me.tsukanov.counter.ui.MainActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(10)

# home page
try:

    el1 = driver.find_element_by_id('android:id/up')
    el1.click()
    time.sleep(3)

    # # branch1
    # el1 = driver.find_element_by_id('android:id/home')
    # el1.click()
    # time.sleep(3)

    # # branch2
    # el1 = driver.find_element_by_id('android:id/action_bar_title')
    # el1.click()
    # time.sleep(3)

    el2 = driver.find_element_by_android_uiautomator('new UiSelector().text("Add counter")')
    el2.click()

    # branch3
    # el2 = driver.find_elements_by_class_name('android.widget.ImageView')[2]
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
  "appPackage": "me.tsukanov.counter",
  "appActivity": "me.tsukanov.counter.ui.MainActivity"
}
'''

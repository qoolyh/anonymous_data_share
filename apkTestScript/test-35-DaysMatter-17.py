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

    el = driver.find_elements_by_class_name('android.widget.ImageView')[2]
    el.click()

    # # branch1
    # el1 = driver.find_elements_by_class_name('android.widget.ImageView')[1]
    # el1.click()
    # time.sleep(5)
    #
    # el2 = driver.find_elements_by_class_name('android.widget.ImageView')[20]
    # el2.click()
    # time.sleep(5)

    # # branch2
    # el1 = driver.find_elements_by_class_name('android.widget.ImageView')[3]
    # el1.click()
    # time.sleep(5)
    #
    # el2 = driver.find_elements_by_class_name('android.widget.ImageView')[3]
    # el2.click()
    # time.sleep(5)

    # # branch3
    # el1 = driver.find_elements_by_class_name('android.widget.ImageView')[4]
    # el1.click()
    # time.sleep(5)
    #
    # el2 = driver.find_elements_by_class_name('android.widget.ImageView')[13]
    # el2.click()
    # time.sleep(5)

    # # branch4
    # el0 = driver.find_element_by_accessibility_id('Open the main menu')
    # el0.click()
    # time.sleep(3)
    #
    # el1 = driver.find_elements_by_class_name('android.widget.ImageView')[12]
    # el1.click()

    # # branch5
    # el0 = driver.find_element_by_accessibility_id('Open the main menu')
    # el0.click()
    # time.sleep(3)
    #
    # el1 = driver.find_element_by_android_uiautomator('new UiSelector().text("Date Calculator")')
    # el1.click()


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

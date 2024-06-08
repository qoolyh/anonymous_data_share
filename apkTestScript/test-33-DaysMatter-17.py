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
time.sleep(10)

# home page
try:

    # # branch1
    # el0 = driver.find_elements_by_class_name('android.widget.ImageView')[1]
    # el0.click()
    # time.sleep(3)

    # # branch1 successor1
    # el1 = driver.find_element_by_accessibility_id('Open the main menu')
    # el1.click()
    # time.sleep(3)
    #
    # el2 = driver.find_element_by_android_uiautomator('new UiSelector().text("Work")')
    # el2.click()

    # # branch1 successor2
    # el1 = driver.find_element_by_accessibility_id('Open the main menu')
    # el1.click()
    # time.sleep(3)
    #
    # el2 = driver.find_elements_by_class_name('android.widget.ImageView')[28]
    # el2.click()

    # # branch1 successor3
    # el1 = driver.find_element_by_accessibility_id('Open the main menu')
    # el1.click()
    # time.sleep(3)
    #
    # el2 = driver.find_elements_by_class_name('android.widget.TextView')[35]
    # el2.click()

    # # branch2
    # el0 = driver.find_elements_by_class_name('android.widget.ImageView')[2]
    # el0.click()
    # time.sleep(3)

    # # branch2 successor1
    # el1 = driver.find_element_by_accessibility_id('Open the main menu')
    # el1.click()
    # time.sleep(3)
    #
    # el2 = driver.find_element_by_android_uiautomator('new UiSelector().text("Work")')
    # el2.click()

    # # branch2 successor2
    # el1 = driver.find_element_by_accessibility_id('Open the main menu')
    # el1.click()
    # time.sleep(3)
    #
    # el2 = driver.find_elements_by_class_name('android.widget.ImageView')[11]
    # el2.click()

    # # branch2 successor3
    # el1 = driver.find_element_by_accessibility_id('Open the main menu')
    # el1.click()
    # time.sleep(3)
    #
    # el2 = driver.find_elements_by_class_name('android.widget.TextView')[16]
    # el2.click()

    # # branch3
    # el0 = driver.find_elements_by_class_name('android.widget.ImageView')[3]
    # el0.click()
    # time.sleep(3)

    # # branch3 successor1
    # el1 = driver.find_element_by_accessibility_id('Open the main menu')
    # el1.click()
    # time.sleep(3)
    #
    # el2 = driver.find_element_by_android_uiautomator('new UiSelector().text("Work")')
    # el2.click()

    # # branch3 successor2
    # el1 = driver.find_element_by_accessibility_id('Open the main menu')
    # el1.click()
    # time.sleep(3)
    #
    # el2 = driver.find_elements_by_class_name('android.widget.ImageView')[9]
    # el2.click()

    # # branch3 successor3
    # el1 = driver.find_element_by_accessibility_id('Open the main menu')
    # el1.click()
    # time.sleep(3)
    #
    # el2 = driver.find_element_by_android_uiautomator('new UiSelector().text("0")')
    # el2.click()

    # # branch4
    # el0 = driver.find_elements_by_class_name('android.widget.ImageView')[4]
    # el0.click()
    # time.sleep(3)

    # # branch4 successor1
    # el1 = driver.find_element_by_accessibility_id('Open the main menu')
    # el1.click()
    # time.sleep(3)
    #
    # el2 = driver.find_element_by_android_uiautomator('new UiSelector().text("Work")')
    # el2.click()

    # # branch4 successor2
    # el1 = driver.find_element_by_accessibility_id('Open the main menu')
    # el1.click()
    # time.sleep(3)
    #
    # el2 = driver.find_elements_by_class_name('android.widget.ImageView')[19]
    # el2.click()

    # # branch4 successor3
    # el1 = driver.find_element_by_accessibility_id('Open the main menu')
    # el1.click()
    # time.sleep(3)
    #
    # el2 = driver.find_element_by_android_uiautomator('new UiSelector().text("0")')
    # el2.click()

    el1 = driver.find_element_by_accessibility_id('Open the main menu')
    el1.click()
    time.sleep(3)

    el2 = driver.find_elements_by_class_name('android.widget.ImageView')[8]
    el2.click()

    # # branch5
    # el2 = driver.find_element_by_android_uiautomator('new UiSelector().text("Work")')
    # el2.click()

    # # branch6
    # el2 = driver.find_elements_by_class_name('android.widget.TextView')[22]
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

import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'com.google.android.apps.docs'
desired_caps['appActivity'] = 'com.google.android.apps.docs.drive.app.navigation.NavigationActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(10)

# home page
try:

    el1 = driver.find_element_by_accessibility_id('More actions for paperRecord')
    el1.click()
    time.sleep(3)

    # # branch1
    # el0 = driver.find_elements_by_id('com.google.android.apps.docs:id/entry_thumbnail')[0]
    # el0.click()
    # time.sleep(3)
    #
    # el1 = driver.find_element_by_accessibility_id('More options')
    # el1.click()
    # time.sleep(3)

    # # branch2
    # el0 = driver.find_elements_by_id('com.google.android.apps.docs:id/badge_view')[0]
    # el0.click()
    # time.sleep(3)
    #
    # el1 = driver.find_element_by_accessibility_id('More options')
    # el1.click()
    # time.sleep(3)

    # # branch3
    # el0 = driver.find_elements_by_id('com.google.android.apps.docs:id/entry_filetype')[0]
    # el0.click()
    # time.sleep(3)
    #
    # el1 = driver.find_element_by_accessibility_id('More options')
    # el1.click()
    # time.sleep(3)

    # # branch4
    # el0 = driver.find_element_by_accessibility_id('paperRecord Folder')
    # el0.click()
    # time.sleep(3)
    #
    # el1 = driver.find_element_by_accessibility_id('More options')
    # el1.click()
    # time.sleep(3)

    el2 = driver.find_element_by_android_uiautomator('new UiSelector().text("Details & activity")')
    el2.click()

    # # branch5
    # el2 = driver.find_elements_by_class_name('android.widget.ImageView')[8]
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
  "appPackage": "com.google.android.apps.docs",
  "appActivity": "com.google.android.apps.docs.drive.app.navigation.NavigationActivity"
}
'''

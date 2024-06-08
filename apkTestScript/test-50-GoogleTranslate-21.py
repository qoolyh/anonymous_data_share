import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'com.google.android.apps.translate'
desired_caps['appActivity'] = 'com.google.android.apps.translate.TranslateActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(10)

# home page
try:

    el1 = driver.find_elements_by_id('com.google.android.apps.translate:id/touch_to_type_text')[0]
    el1.click()

    el2 = driver.find_elements_by_class_name('android.widget.ImageView')[0]
    el2.click()

    el3 = driver.find_element_by_android_uiautomator('new UiSelector().text("Handwriting")')
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
  "appPackage": "com.google.android.apps.translate",
  "appActivity": "com.google.android.apps.translate.TranslateActivity"
}
'''

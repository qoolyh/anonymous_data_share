import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '192.168.1.119:18888'
desired_caps['appPackage'] = 'com.faltenreich.diaguard'
desired_caps['appActivity'] = 'com.faltenreich.diaguard.feature.navigation.MainActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(5)

# home page
try:

    el1 = driver.find_element_by_accessibility_id('Open Navigator')
    el1.click()
    time.sleep(3)

    el2 = driver.find_element_by_android_uiautomator('new UiSelector().text("Export")')
    el2.click()
    time.sleep(3)

    el3 = driver.find_elements_by_id('com.faltenreich.diaguard:id/date_end_button')[0]
    el3.click()
    time.sleep(3)

    el4 = driver.find_elements_by_id('android:id/button1')[0]
    el4.click()

finally:
    time.sleep(3)
    driver.quit()

'''
{
  "platformName": "Android",
  "platformVersion": "6.0.1",
  "deviceName": "192.168.1.119:18888",
  "noReset": true,
  "appPackage": "com.faltenreich.diaguard",
  "appActivity": "com.faltenreich.diaguard.feature.navigation.MainActivity"
}
'''
import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '192.168.1.119:18888'
desired_caps['appPackage'] = 'org.quantumbadger.redreader'
desired_caps['appActivity'] = 'org.quantumbadger.redreader.activities.MainActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(5)

# home page
try:

    el1 = driver.find_elements_by_class_name('android.widget.TextView')[4]
    el1.click()
    time.sleep(3)

    el2 = driver.find_elements_by_id('org.quantumbadger.redreader:id/dialog_mainmenu_custom_type')[0]
    el2.click()
    time.sleep(3)

    el3 = driver.find_elements_by_id('android:id/text1')[0]
    el3.click()
    time.sleep(3)

    el4 = driver.find_elements_by_id('android:id/button1')[0]
    el4.click()

finally:
    time.sleep(1)
    driver.quit()

'''
{
  "platformName": "Android",
  "platformVersion": "6.0.1",
  "deviceName": "192.168.1.119:18888",
  "noReset": true,
  "appPackage": "org.quantumbadger.redreader",
  "appActivity": "org.quantumbadger.redreader.activities.MainActivity"
}
'''
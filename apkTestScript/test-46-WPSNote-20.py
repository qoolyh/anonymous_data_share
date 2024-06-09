import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'cn.wps.note'
desired_caps['appActivity'] = 'cn.wps.note.StartActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(5)

# home page
try:

    el1 = driver.find_elements_by_class_name("android.widget.ImageView")[7]
    el1.click()
    time.sleep(3)

    el2 = driver.find_elements_by_id('cn.wps.note:id/me_setting')[0]
    el2.click()
    time.sleep(3)

    el3 = driver.find_elements_by_id('cn.wps.note:id/font_setting')[0]
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
  "appPackage": "cn.wps.note",
  "appActivity": "cn.wps.note.StartActivity"
}
'''

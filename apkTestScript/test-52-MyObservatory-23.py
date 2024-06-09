import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'hko.MyObservatory_v1_0'
desired_caps['appActivity'] = 'hko.homepage.Homepage2Activity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(30)

# home page
try:

    el1 = driver.find_element_by_accessibility_id('Add')
    el1.click()

finally:
    time.sleep(5)
    driver.quit()

'''
{
  "platformName": "Android",
  "platformVersion": "6.0.1",
  "deviceName": "127.0.0.1:7555",
  "noReset": true,
  "appPackage": "hko.MyObservatory_v1_0",
  "appActivity": "hko.homepage.Homepage2Activity"
}
'''

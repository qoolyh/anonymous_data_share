import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '192.168.1.119:18888'
desired_caps['appPackage'] = 'org.bookdash.android'
desired_caps['appActivity'] = 'org.bookdash.android.presentation.splash.SplashActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(5)

# home page
try:

    el1 = driver.find_elements_by_id('org.bookdash.android:id/action_language_choice')[0]
    el1.click()

finally:
    time.sleep(3)
    driver.quit()

'''
{
  "platformName": "Android",
  "platformVersion": "6.0.1",
  "deviceName": "192.168.1.119:18888",
  "noReset": true,
  "appPackage": "org.bookdash.android",
  "appActivity": "org.bookdash.android.presentation.splash.SplashActivity"
}
'''
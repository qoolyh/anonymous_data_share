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
time.sleep(10)

try:
    el1 = driver.find_elements_by_id('org.bookdash.android:id/text_current_language')[0]
    el1.click()

finally:
    time.sleep(3)
    driver.quit()

import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'com.github.yeriomin.dumbphoneassistant'
desired_caps['appActivity'] = 'com.github.yeriomin.dumbphoneassistant.ManageContactsActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(10)

try:
    el1 = driver.find_elements_by_id('com.github.yeriomin.dumbphoneassistant:id/button_to_sim')[0]
    el1.click()

finally:
    time.sleep(3)
    driver.quit()

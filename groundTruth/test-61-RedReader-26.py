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
time.sleep(10)

try:
    el1 = driver.find_elements_by_id('org.quantumbadger.redreader:id/list_item_secondary_icon')[0]
    el1.click()
    time.sleep(3)

    el2 = driver.find_elements_by_id('android:id/button2')[0]
    el2.click()

finally:
    time.sleep(3)
    driver.quit()

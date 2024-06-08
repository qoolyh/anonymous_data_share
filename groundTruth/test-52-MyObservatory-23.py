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
time.sleep(10)

try:
    el1 = driver.find_elements_by_id('hko.MyObservatory_v1_0:id/district_btn')[0]
    el1.click()
    time.sleep(3)

    el2 = driver.find_elements_by_id('hko.MyObservatory_v1_0:id/add_location_btn')[0]
    el2.click()

finally:
    time.sleep(3)
    driver.quit()

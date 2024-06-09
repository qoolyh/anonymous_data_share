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
time.sleep(10)

try:
    el1 = driver.find_elements_by_id('com.faltenreich.diaguard:id/fab_primary')[0]
    el1.click()
    time.sleep(3)

    el2 = driver.find_elements_by_id('com.faltenreich.diaguard:id/tag_input')[0]
    el2.click()
    time.sleep(3)

    el3 = driver.find_elements_by_id('com.faltenreich.diaguard:id/tag_name')[1]
    el3.click()

finally:
    time.sleep(3)
    driver.quit()

import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'com.simplemobiletools.calculator'
desired_caps['appActivity'] = 'com.simplemobiletools.calculator.activities.SplashActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(10)

try:
    el1 = driver.find_element_by_accessibility_id('More options')
    el1.click()
    time.sleep(3)

    el2 = driver.find_elements_by_id('com.simplemobiletools.calculator:id/title')[0]
    el2.click()
    time.sleep(3)

    el3 = driver.find_elements_by_id('com.simplemobiletools.calculator:id/settings_customize_colors_label')[0]
    el3.click()
    time.sleep(3)

    el4 = driver.find_elements_by_id('com.simplemobiletools.calculator:id/customization_theme')[0]
    el4.click()
    time.sleep(3)

    el5 = driver.find_element_by_android_uiautomator('new UiSelector().text("Light")')
    el5.click()

finally:
    time.sleep(3)
    driver.quit()

import time
from appium import webdriver

desired_caps = {}                                                       # 定义一个字典，存储 Capability 相关信息
desired_caps['platformName'] = 'Android'                                # 定义设备平台名称
desired_caps['platformVersion'] = '6.0.1'                               # 定义设备版本号
desired_caps['deviceName'] = '127.0.0.1:7555'                           # 定义设备名称
desired_caps['appPackage'] = 'com.simplemobiletools.applauncher'        # 获取包名
desired_caps['appActivity'] = 'com.simplemobiletools.applauncher.activities.SplashActivity'  # 定义 Activity -- app 的启动页面
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)  # 调用 appium 服务并传参
time.sleep(10)

# home page
try:

    el1 = driver.find_element_by_accessibility_id('More options')
    el1.click()
    time.sleep(3)

    el2 = driver.find_element_by_android_uiautomator('new UiSelector().text("Settings")')
    el2.click()
    time.sleep(3)

    el3 = driver.find_elements_by_id('com.simplemobiletools.applauncher:id/settings_customize_colors_label')[0]
    el3.click()
    time.sleep(3)

    el4 = driver.find_element_by_android_uiautomator('new UiSelector().text("Dark theme")')
    el4.click()
    time.sleep(3)

    # # 分支
    # el4 = driver.find_element_by_android_uiautomator('new UiSelector().text("Theme")')
    # el4.click()
    # time.sleep(3)

    el5 = driver.find_element_by_android_uiautomator('new UiSelector().text("Light theme")')
    el5.click()

finally:
    time.sleep(5)
    driver.quit()

'''
{
  "platformName": "Android",
  "platformVersion": "6.0.1",
  "deviceName": "127.0.0.1:7555",
  "noReset": true,
  "appPackage": "com.simplemobiletools.applauncher",
  "appActivity": "com.simplemobiletools.applauncher.activities.SplashActivity"
}
'''
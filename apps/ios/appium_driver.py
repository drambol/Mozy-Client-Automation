import time

from lib.platformhelper import PlatformHelper
if PlatformHelper.is_mac():
    import atomac

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lib.loghelper import LogHelper
from apps.ios.iOS_installer import iOS_Installer

class Driver(object):

    driver = None

    def __init__(self):
        self.restart_appium_server()
        # self.driver = iOS_Installer.create_driver()

    @classmethod
    def locate_element(self, element, wait_time=10):
        self.driver = iOS_Installer.create_driver()
        WebDriverWait(self.driver, wait_time).until((EC.visibility_of_element_located((By.XPATH, element))))
        return WebDriverWait(self.driver, wait_time).until((EC.presence_of_element_located((By.XPATH, element))))

    @classmethod
    def locate_elements(self, element, wait_time=10):
        self.driver = iOS_Installer.create_driver()
        WebDriverWait(self.driver, wait_time).until((EC.visibility_of_element_located((By.XPATH, element))))
        return WebDriverWait(self.driver, wait_time).until((EC.presence_of_all_elements_located((By.XPATH, element))))

    @staticmethod
    def restart_appium_server():
        LogHelper.info('===========Now Restarting Appium Server===========')
        print('===========Now Restarting Appium Server===========')
        atomac.launchAppByBundleId('com.appium.Appium')
        app = atomac.getAppRefByBundleId('com.appium.Appium')
        time.sleep(2)
        exec_button = app.findFirstR(AXRole='AXButton', AXIdentifier='_NS:15')
        dustbin_button = app.findFirstR(AXRole='AXButton', AXIdentifier='_NS:215')
        status = exec_button._getAttribute('AXTitle')
        if status == 'Stop':
            exec_button.Press()
            time.sleep(2)
        dustbin_button.Press()
        exec_button.Press()
        time.sleep(15)
        LogHelper.info('===========Appium Server is launched successfully===========')
        print('===========Appium Server is launched successfully===========')
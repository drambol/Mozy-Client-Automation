import time

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apps.android.android_installer import Android_Installer


class Driver(object):

    @classmethod
    def locate_element(self, element, wait_time=10):
        self.driver = Android_Installer.create_driver()
        WebDriverWait(self.driver, wait_time).until((EC.visibility_of_element_located((By.XPATH, element))))
        return WebDriverWait(self.driver, wait_time).until((EC.presence_of_element_located((By.XPATH, element))))

    @classmethod
    def locate_elements(self, element, wait_time=10):
        self.driver = Android_Installer.create_driver()
        WebDriverWait(self.driver, wait_time).until((EC.visibility_of_element_located((By.XPATH, element))))
        return WebDriverWait(self.driver, wait_time).until((EC.presence_of_all_elements_located((By.XPATH, element))))

    @classmethod
    def find_element(self, xpath):
        self.driver = Android_Installer.create_driver()
        el = None
        for i in range(10):
            try:
                el = self.locate_element(xpath, wait_time=1)
                break
            except NoSuchElementException:
                self.scroll_down()
            except WebDriverException:
                self.scroll_down()
        return el

    @classmethod
    def delayed_click(self, xpath, index=0, sleep_time=1):
        self.driver = Android_Installer.create_driver()
        time.sleep(sleep_time)
        for i in range(15):
            try:
                self.locate_elements(xpath, wait_time=1)[index].click()
                break
            except:
                time.sleep(1)

    @classmethod
    def press_menu(self, code):
        self.driver = Android_Installer.create_driver()
        self.driver.press_keycode(code)

    @classmethod
    def scroll_down(self):
        self.driver = Android_Installer.create_driver()
        x_position = self.driver.get_window_size()['width']/2
        y_position_a = self.driver.get_window_size()['height']/2 + 50
        y_position_b = self.driver.get_window_size()['height'] / 2 - 50
        self.driver.swipe(x_position, y_position_a, x_position, y_position_b, duration=200)
        time.sleep(1)

    @classmethod
    def find_element_by_original_api(self, uia_string):
        self.driver = Android_Installer.create_driver()
        self.driver.find_element_by_android_uiautomator(uia_string)

    @classmethod
    def find_elements_by_original_api(self, uia_string):
        self.driver = Android_Installer.create_driver()
        self.driver.find_elements_by_android_uiautomator(uia_string)

    @classmethod
    def is_element_exists(self, xpath, wait_time=10):
        try:
            self.locate_element(xpath, wait_time)
            return True
        except:
            return False
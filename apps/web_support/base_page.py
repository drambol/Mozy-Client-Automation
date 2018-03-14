import time, platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from configuration.config_adapter import ConfigAdapter
from lib.loghelper import LogHelper
from lib.filehelper import FileHelper
from lib.kpihelper import KPIHelper


class Page(object):

    driver = None

    @classmethod
    def current_driver(self):
        return self.driver

    @classmethod
    def current_window(self):
        return self.driver.current_window_handle

    @classmethod
    def create_browser(self, force=False, type='FIREFOX'):
        download_path = ConfigAdapter.get_download_path()
        if platform.system() == "Linux":
            download_path = ConfigAdapter.get_installer_path()
        if platform.system() == "Darwin":
            if FileHelper.dir_exist(download_path):
                FileHelper.delete_directory(download_path)
            FileHelper.create_directory(download_path)

        if (self.driver is None and type.upper() == 'FIREFOX') or force:
            profile = webdriver.FirefoxProfile()
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.download.manager.showWhenStarting", False)
            profile.set_preference("browser.download.dir", download_path.replace("/", "\\"))
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/mzd;application/mzdx;application/octet-stream;application/zip")
            self.driver = webdriver.Firefox(firefox_profile=profile)
            self.driver.maximize_window()

        if self.driver is None and type.upper() == 'CHROME':
            options = webdriver.ChromeOptions()
            options.add_experimental_option("prefs", {'download.default_directory': download_path})
            self.driver = webdriver.Chrome(chrome_options=options)
            self.driver.maximize_window()

        return self.driver
        # pass

    @classmethod
    def wait_for_page_load(self, timeout=60):
        old_page = self.driver.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.driver, timeout).until(staleness_of(old_page))

    @classmethod
    def locate_element(self, xpath, wait_time=30):
        """
        Locate element by xpath
        @timeout: 30
        return element if found, or None if not found
        """
        LogHelper.debug("Locate element %s" %xpath)
        el = None
        try:
            el = WebDriverWait(self.driver, wait_time).until((EC.visibility_of_element_located((By.XPATH, xpath))))
            # el = WebDriverWait(self.driver, wait_time).until(lambda driver: EC.visibility_of_element_located((By.XPATH, xpath)))
            # el = WebDriverWait(self.driver, wait_time).until(lambda driver: driver.find_element_by_xpath(xpath))

            LogHelper.info("Element %s found %s" %(xpath, el))

        except Exception, e:
            LogHelper.error(repr(e))
            LogHelper.error("Element %s is not found %s" % (xpath, el))
        finally:
            return el

    @classmethod
    def locate_button(self, xpath, wait_time=30):
        """
        Locate button element by xpath
        @timeout: 30
        return element if found, or None if not found
        """
        LogHelper.debug("Locate button %s" %xpath)
        el = None
        try:
            el = WebDriverWait(self.driver, wait_time).until((EC.element_to_be_clickable((By.XPATH, xpath))))

            LogHelper.info("Button %s found %s" %(xpath, el))

        except Exception, e:
            LogHelper.error(repr(e))
            LogHelper.error("Button %s is not found %s" % (xpath, el))
        finally:
            return el

    @classmethod
    def locate_element_by_id(cls,id,wait_time=30):
        LogHelper.debug("locate ID element %s" % id)
        el = None
        try:
            el = WebDriverWait(cls.driver, wait_time).until((EC.visibility_of_element_located((By.ID, id))))
            LogHelper.debug("ID element %s found %s" % (id, el))

        except Exception, e:
            LogHelper.error(repr(e))
            # Page.quit()
            LogHelper.error("ID Element %s is not found %s" % (id, el))
        finally:
            return el

    @classmethod
    def find_element_by_tag_name(cls,tag_name,wait_time=30):
        LogHelper.debug("locate element %s" % tag_name)
        el = None
        try:
            el = WebDriverWait(cls.driver,wait_time).until((EC.visibility_of_element_located((By.TAG_NAME, tag_name))))
            LogHelper.debug("Tag name %s found %s" % (tag_name, el))

        except Exception, e:
            LogHelper.error(repr(e))
            # Page.quit()
            LogHelper.error("Tag name %s is not found %s" % (tag_name, el))
        finally:
            return el

    @classmethod
    def find_element_by_linktext(cls,linktext,wait_time=30):
        LogHelper.debug("Locate linktext %s" % linktext)
        el = None
        try:
            el = WebDriverWait(cls.driver, wait_time).until((EC.visibility_of_element_located((By.LINK_TEXT, linktext))))
            LogHelper.debug("Linktext element %s found %s" % (linktext, el))

        except Exception, e:
            LogHelper.error(repr(e))
            # Page.quit()
            LogHelper.error("Linktext %s is not found %s" % (linktext, el))
        finally:
            return el

    @classmethod
    def switch_to_iframe(cls,iframe):
        driver = cls.driver

        try:
            # iframe_element = driver.find_element_by_tag_name(iframe)
            iframe_element = cls.locate_element(iframe)
            driver.switch_to.frame(iframe_element)
            # element = driver.find_element_by_id(id)
            return True
        except Exception, e:
            LogHelper.error(repr(e))
            Page.quit()
            LogHelper.error("Iframe %s is not found" % (iframe))
            return None


    @classmethod
    def locate_elements(self, xpath, wait_time=30):
        LogHelper.debug('Locate elements %s' %xpath)
        els = None
        try:
            # WebDriverWait(cls.driver, wait_time).until((EC.visibility_of_element_located((By.XPATH, xpath))))
            els = WebDriverWait(self.driver, wait_time).until((EC.presence_of_all_elements_located((By.XPATH, xpath))))

        except Exception, e:
            LogHelper.error(repr(e))
            # Page.quit()
            LogHelper.error("Elements %s are not found %s" % (xpath, els))
        finally:
            return els

    @classmethod
    def is_element_exist(self, xpath, wait_time=30):
        return self.locate_element(xpath, wait_time)
        # return
        # if result:
        #     return result
        # else:
        #     return None


    @classmethod
    def is_linktext_exist(self,linktext,wait_time=30):
        return self.find_element_by_linktext(linktext)
        # if result:
        #     return True
        # else:
        #     return None

    @classmethod
    def wait_for_element_list(self, xpath, index=0):
        element = None
        for i in range(30):
            try:
                element = self.driver.find_elements_by_xpath(xpath)[index]
                break
            except:
                time.sleep(1)
        return element

    @classmethod
    def delayed_click(self, xpath, index=0, sleep_time=1):
        time.sleep(sleep_time)
        for i in range(60):
            try:
                el = self.driver.find_elements_by_xpath(xpath)[index]
                self.driver.execute_script("arguments[0].scrollIntoView();", el)
                el.click()
                LogHelper.info("click element %s succussed" %xpath)
                return True
            except:
                time.sleep(2)
        return False

    @classmethod
    def select_menu(self, xpath, menu):
        element = self.locate_element(xpath)
        actionChains = ActionChains(self.driver)
        actionChains.context_click(element).perform()
        self.driver.find_element_by_xpath("//li[@title='" + menu + "']").click()

    @classmethod
    def switch_to_window(cls, window):
        main_window = cls.current_window()
        driver = cls.driver
        window_element = driver.find_element_by_tag_name(window)
        driver.switch_to.window(window_element)
        # element = driver.find_element_by_id(id)

    @classmethod
    def uncheck(self, xpath):
        el = Page.locate_element(xpath)
        if el.is_selected():
            el.click()

    @classmethod
    def check(self, xpath):
        el = Page.locate_element(xpath)
        if not el.is_selected():
            el.click()

    @classmethod
    def clear(cls, xpath):
        el = Page.locate_element(xpath)
        el.clear()

    @classmethod
    def close_driver(self):
        self.driver.quit()
        self.driver = None

    @classmethod
    def select_dropbox(self,xpath,visible_text):
        element = self.locate_element(xpath)
        Select(element).select_by_visible_text(visible_text)

    @classmethod
    def quit(self):
        self.driver.quit()
        self.driver = None

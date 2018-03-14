import os
from appium import webdriver
from lib.jenkinshelper import JenkinsHelper
from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.config_adapter import ConfigAdapter
from lib.loghelper import LogHelper
from configuration.android.android_config_loader import ANDROID_CONFIG

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class Android_Installer(object):

    driver = None

    @staticmethod
    def download_and_install(build, job):
        jh = JenkinsHelper(GLOBAL_CONFIG["JENKINS"]["URL"], GLOBAL_CONFIG["JENKINS"]["USERNAME"], GLOBAL_CONFIG["JENKINS"]["KEY"])
        dest = ConfigAdapter.get_installer_path('ANDROID')
        jh.download_packages(jh.get_packages(job, build), dest=dest)

    @classmethod
    def create_driver(self):
        if self.driver == None:
            LogHelper.info("======Ready to install Mozy Client to Android Simulator======")
            desired_caps = {}
            desired_caps['platformName'] = ANDROID_CONFIG['SIMULATOR']['PLATFORM_NAME']
            desired_caps['platformVersion'] = ANDROID_CONFIG['SIMULATOR']['PLATFORM_VERSION']
            desired_caps['app'] = PATH(ANDROID_CONFIG['SIMULATOR']['APP'])
            desired_caps['deviceName'] = ANDROID_CONFIG['SIMULATOR']['DEVICE_NAME']
            desired_caps['app-package'] = ANDROID_CONFIG['SIMULATOR']['APP_PACKAGE']
            desired_caps['app-activity'] = ANDROID_CONFIG['SIMULATOR']['APP_ACTIVITY']
            self.driver = webdriver.Remote(ANDROID_CONFIG['SIMULATOR']['APPIUM_URI'], desired_caps)
        return self.driver
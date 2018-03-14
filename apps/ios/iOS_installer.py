import os
from appium import webdriver
from lib.loghelper import LogHelper
from configuration.ios.ios_config_loader import IOS_CONFIG

class iOS_Installer(object):

    driver = None

    @classmethod
    def download_and_install(self, build, job):
        LogHelper.info('Building a new app from XCode......')

    @classmethod
    def create_driver(self):
        if self.driver == None:
            app = os.path.abspath(IOS_CONFIG['SIMULATOR']['ABS_PATH'])
            self.driver = webdriver.Remote(
                command_executor=IOS_CONFIG['SIMULATOR']['APPIUM_URI'],
                desired_capabilities={
                    'app': app,
                    'platformName': IOS_CONFIG['SIMULATOR']['CAPABILITY']['PLATFORM_NAME'],
                    'platformVersion': IOS_CONFIG['SIMULATOR']['CAPABILITY']['PLATFORM_VERSION'],
                    'deviceName': IOS_CONFIG['SIMULATOR']['CAPABILITY']['DEVICE_NAME'],
                }
            )
        return self.driver
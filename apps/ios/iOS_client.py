import os
from appium import webdriver
from configuration.ios.ios_config_loader import IOS_CONFIG
from apps.ios.iOS_installer import iOS_Installer
from apps.ios.iOS_controller import iOS_Controller

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class IOSClient(object):

    # driver = None

    @property
    def installer(cls):
        return iOS_Installer()

    @property
    def controller(self):
        return iOS_Controller()

    # @classmethod
    # def tearDown(self):
    #     iOS_Controller().tearDown()
    #
    # @classmethod
    # def login(self):
    #     iOS_Controller().login()
    #
    # @classmethod
    # def verify_version(self):
    #     iOS_Controller().verify_version()

    # @classmethod
    # def install_mozy(self):
    #     app = os.path.abspath(IOS_CONFIG['SIMULATOR']['ABS_PATH'])
    #     self.driver = webdriver.Remote(
    #         command_executor = IOS_CONFIG['SIMULATOR']['APPIUM_URI'],
    #         desired_capabilities = {
    #             'app': app,
    #             'platformName': IOS_CONFIG['SIMULATOR']['CAPABILITY']['PLATFORM_NAME'],
    #             'platformVersion': IOS_CONFIG['SIMULATOR']['CAPABILITY']['PLATFORM_VERSION'],
    #             'deviceName': IOS_CONFIG['SIMULATOR']['CAPABILITY']['DEVICE_NAME']
    #         })
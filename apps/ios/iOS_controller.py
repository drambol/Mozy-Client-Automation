from __future__ import print_function
import time
from configuration.ios.ios_config_loader import IOS_CONFIG
from lib.loghelper import LogHelper
from lib.cmdhelper import CmdHelper
from apps.ios.appium_driver import Driver
from apps.ios.iOS_installer import iOS_Installer
from apps.ios.ios_gui.my_mozy_view import My_Mozy_View

class iOS_Controller(Driver):

    xpaths = {'sign_into_Mozy_button': "//UIAApplication[1]/UIAWindow[2]/UIAButton[1]",
              'email_address_textfield': "//UIAApplication[1]/UIAWindow[2]/UIATextField[1]",
              'password_textfield': "//UIAApplication[1]/UIAWindow[2]/UIASecureTextField[1]",
              'sign_in_button': "//UIAApplication[1]/UIAWindow[3]/UIAKeyboard[1]/UIAButton[4]",
              'processing_bar': "//UIAApplication[1]/UIAWindow[5]/UIAAlert[1]/UIACollectionView[1]/UIACollectionCell[2]/UIAButton[1]",
              'decline_presscode_button': "//UIAApplication[1]/UIAWindow[2]/UIANavigationBar[1]/UIAButton[2]",
              'setting_icon': "//UIAButton[@label='Settings']",
              'about_textfield': "//UIAStaticText[@label='About']",
              'version_textfield': "//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIATableCell[1]/UIAStaticText[2]",
              'logout_button': "//*[@label='Sign out from Mozy']",
              'confirm_logout_button': "//UIAButton[@label='Yes']",
              }

    @classmethod
    def prepare_environment(cls, env):
        LogHelper.info("Nothing to do for iOS client here")

    @classmethod
    def tearDown(self):
        LogHelper.info("======Test done, close Android Simulator and Appium Server======")
        print("======Test done, close Android Simulator and Appium Server======")
        self.driver = iOS_Installer.create_driver()
        self.driver.quit()
        try:
            cmd = "osascript -e 'quit app \"iOS Simulator\"'"
            CmdHelper.run(cmd)
            cmd = "osascript -e 'quit app \"Appium\"'"
            CmdHelper.run(cmd)
        except Exception as Error:
            print(Error.message)

    @classmethod
    def login(self):
        username = IOS_CONFIG['CREDENTIAL']['STD1']['USERNAME']
        password = IOS_CONFIG['CREDENTIAL']['STD1']['PASSWORD']
        self.locate_element(self.xpaths['sign_into_Mozy_button']).click()
        self.locate_element(self.xpaths['email_address_textfield']).send_keys(username)
        self.locate_element(self.xpaths['password_textfield']).send_keys(password)
        self.locate_element(self.xpaths['sign_in_button']).click()
        time.sleep(5)
        self.locate_element(self.xpaths['processing_bar']).click()
        # self.locate_element(self.xpaths['decline_presscode_button']).click()

    @classmethod
    def move_to_settings(self):
        My_Mozy_View.navigate_to()
        try:
            self.locate_element(self.xpaths['setting_icon']).click()
        except:
            My_Mozy_View.navigate_to()
            self.locate_element(self.xpaths['setting_icon']).click()

    @classmethod
    def verify_version(self, version):
        LogHelper.info("======Verify APK versoin======")
        self.move_to_settings()
        self.locate_element(self.xpaths['about_textfield']).click()
        version_number = self.locate_element(self.xpaths['version_textfield']).text
        assert version_number == version, 'Version Number is not as expected!'
        LogHelper.info("Mozy app version: " + version_number)
        print("Mozy app version: " + version_number)

    @classmethod
    def logout(self):
        LogHelper.info("======Ready to logout Mozy account======")
        My_Mozy_View.navigate_to()
        self.locate_element(self.xpaths['setting_icon']).click()
        self.locate_element(self.xpaths['logout_button']).click()
        self.locate_element(self.xpaths['confirm_logout_button']).click()
        assert self.locate_element(self.xpaths['sign_into_Mozy_button']).is_displayed()

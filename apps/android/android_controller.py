import os, time, subprocess
from lib.loghelper import LogHelper
from configuration.android.android_config_loader import ANDROID_CONFIG
from apps.android.android_installer import Android_Installer
from apps.android.appium_driver import Driver

class Android_Controller(Driver):

    xpaths = {'accept_button': "//*[@text='Accept']",
              'sign_into_Mozy_button': "//*[@text='Sign in to Mozy']",
              'email_address_textfield': "//*[@text='Email address']",
              'edit_textfield': "//*[@class='android.widget.EditText']",
              'sign_in_button': "//*[@text='Sign In']",
              'decline_presscode_button': "//*[@text='No']",
              'ok_button': "//*[@text='OK']",
              'display_all_tab': "//*[@text='All Files']",
              'setting_textview': "//*[@text='Settings']",
              'about_textview': "//*[@text='About']",
              'my_mozy_textview': "//*[@text='My Mozy']",
              'sign_out_textview': "//*[@text='Sign Out']",
              'textview': "//*[@class='android.widget.TextView']"
              }

    @staticmethod
    def prepare_environment(env):
        LogHelper.info("======Current test environment: " + env + "======")
        LogHelper.info("======Ready to start Android Simulator and Appium Server======")
        subprocess.Popen('cmd /c taskkill /F /IM node.exe /T')
        subprocess.Popen('cmd /c cd ' + os.getenv('Android_Home') + '\\tools && emulator -avd ' + ANDROID_CONFIG['SIMULATOR']['DEVICE_NAME'])
        time.sleep(30)
        os.system("start cmd /k appium")
        subprocess.Popen('cmd /c del C:\\android_installer\\Mozy.apk /F')
        time.sleep(10)
        subprocess.Popen('cmd /c ren C:\\android_installer\\Mozy_*.apk Mozy.apk')

    @classmethod
    def login(self):
        LogHelper.info("======Ready to log in Mozy Android======")
        username = ANDROID_CONFIG['CREDENTIAL']['STD1']['USERNAME']
        password = ANDROID_CONFIG['CREDENTIAL']['STD1']['PASSWORD']
        self.locate_element(self.xpaths['accept_button']).click()
        self.locate_element(self.xpaths['sign_into_Mozy_button']).click()
        self.locate_element(self.xpaths['email_address_textfield']).send_keys(username)
        self.locate_elements(self.xpaths['edit_textfield'])[1].send_keys(password)
        self.locate_element(self.xpaths['sign_in_button']).click()
        Driver.delayed_click(self.xpaths['decline_presscode_button'])
        assert self.locate_element(self.xpaths['display_all_tab']).is_displayed()
        LogHelper.info("Log in successfully with " + username)

    @classmethod
    def logout(self):
        LogHelper.info("======Ready to log out in Mozy Android======")
        self.press_menu(82)
        try:
            self.locate_element(self.xpaths['my_mozy_textview'], wait_time=1).click()
            self.press_menu(82)
        except:
            pass # Eat exception here to handle log out from different screens.
        finally:
            self.locate_element(self.xpaths['setting_textview']).click()
        self.find_element(self.xpaths['sign_out_textview']).click()
        Driver.delayed_click(self.xpaths['ok_button'])
        assert self.locate_element(self.xpaths['sign_into_Mozy_button']).is_displayed()
        LogHelper.info("Sign out Mozy account successfully.")

    @classmethod
    def verify_version(self):
        LogHelper.info("======Verify APK Version======")
        self.press_menu(82)
        self.locate_element(self.xpaths['setting_textview']).click()
        self.locate_element(self.xpaths['about_textview']).click()
        apk_version = self.locate_elements(self.xpaths['textview'])[3].text
        LogHelper.info("Expected APK Version is " + ANDROID_CONFIG['Environment']['VERSION'])
        LogHelper.info("Actual APK Version is " + str(apk_version))
        assert apk_version == ANDROID_CONFIG['Environment']['VERSION']

    @classmethod
    def tearDown(self):
        LogHelper.info("======Test done, close Android Simulator and Appium Server======")
        self.driver = Android_Installer.create_driver()
        self.driver.quit()
        try:
            subprocess.Popen('cmd /c taskkill /F /IM conhost.exe /T')
            subprocess.Popen('cmd /c taskkill /F /IM emulator-arm.exe /T')
            subprocess.Popen('cmd /c taskkill /F /IM qemu-system-i386.exe /T')
        except Exception as Error:
            print Error.message
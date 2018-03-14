from lib.platformhelper import PlatformHelper

if PlatformHelper.is_win():
    from pywinauto import timings
    from pywinauto.application import Application
    from pywinauto.findwindows import find_windows
    from pywinauto import ElementNotFoundError

from configuration.runner_config_loader import RUNNER_CONFIG
from apps.windows.windows_controller import Windows_Controller


class WindowsGUIBaseElement(object):
    oem = "MozyPro"

    @classmethod
    def current_window(self):
        return self.app.window_(handle=self._handle)

    # @classmethod
    # def wait_windows_ready(self):
    #     # timings.WaitUntilPasses(self.element_wait_time, 1, checkwindow)
    #     try:
    #         # wait a maximum of 10.5 seconds for the
    #         # window to be found in increments of .5 of a second.
    #         # P.int a message and re-raise the original exception if never found.
    #         timings.WaitUntilPasses(self.element_wait_time, .5, self.Exists, (ElementNotFoundError))
    #         return True
    #     except ElementNotFoundError as e:
    #         print("ERROR: Timed out")
    #         raise e
    #         return False

    # @classmethod
    # def locate_element(self, xpath, wait_time=30):
    #     print ("locate element %s" %xpath)
    #     el = None
    #     try:
    #         el = WebDriverWait(self.driver, wait_time).until((EC.visibility_of_element_located((By.XPATH, xpath))))
    #         print ("element %s found %s" %(xpath, el))
    #     except NoSuchElementException as e:
    #         print (e.message)
    #     except TimeoutException as e:
    #         print (e.message)
    #     return el

    def __init__(self, name, matcher, element_wait_time=None):
        oem = RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"
        # self._app = self.launch_mozy(self.oem)
        # self._app = None

        self._name = name
        self._matcher = matcher
        self._element_wait_time = element_wait_time or 30
        self._window = None
        # self._app = Application().connect(title_re=self.title)
        self._app = None
        # print self._name

    # @classmethod
    def wait_windows_ready(self, **kwargs):

        if self._window:
            self.window.set_focus()
        # self.title = self.oem + " - Status"
        # self._app = Application().start(Windows_Controller(self.oem).statusapp)
        self._app = Application().connect(title_re=self.title)
        # self._app = Application().connect(title=self.oem + " - Status")

        def checkwindow():
            self._handle = find_windows(**kwargs)[0]
            return self._handle

        timings.WaitUntilPasses(self.element_wait_time, 1, checkwindow)
        self._window = self.app.window_(handle=self._handle)
        return self._window

    # @classmethod
    # def current_window(cls):
    #     return cls.app.window_(handle=cls._handle)

    @property
    def name(self):
        return self._name

    @property
    def matcher(self):
        return self._matcher

    @property
    def element_wait_time(self):
        return self._element_wait_time

    @property
    def window(self):
        return self._window

    @name.setter
    def name(self, value):
        self._name = value

    @matcher.setter
    def matcher(self, value):
        self._matcher = value

    @window.setter
    def window(self, value):
        self._window = value

    @property
    def app(self):
        if self._app is None:
            return Application().start(path=Windows_Controller(self.oem).statusapp)
        return self._app

    @app.setter
    def app(self, value):
        self._app = value

    @staticmethod
    def retrieve(window, name):
        if window is None:
            return None
        else:
            return window[name]

    # def wait_window(self):
    #     if self._window:
    #         self.window.set_focus()
    #     return self._window

    def launch_mozy(self, oem="mozypro"):
        # if oem == "mozypro":
        #     self.oem = "MozyPro"
        # else:
        #     self.oem = "MozyEnterprise"
        # self._app = Application().start(Windows_Controller(self.oem).statusapp)
        if self._app is None:
            self._app = Application().start(path=Windows_Controller(self.oem).statusapp)
        return self.app


    def window_ready(self):
        if self._window:
            self.window.set_focus()
        return self._window



# End of WindowsGUIBaseElement Class


if __name__ == "__main__":

    from windows_status_element import WindowsStatusElement

    status = WindowsStatusElement("ContinueSetup", "ContinueSetup")
    # status.wait_window()
    status.window.ContinueSetup.Click()
    # systray_icons = status.app.ShellTrayWnd.NotificationAreaToolbar
    # status.app.ClickSystemTrayIcon("Microsoft Outlook")
    # print status.window.Settings.exists()
    # print status.window.ContinueSetup.exists()
    # print status.window.StartBackup.exists()
    # print status.window.Details.exists()
    # print status.app.PopupMenu
    # status.app.PopupMenu.Menu()

    # print status.window.print_control_identifiers()
    # print status.window.ContinueSetup.Click()

    # settings = WindowsSettingsElement("FileSystem")
    # settingswindow = settings.wait_window()
    # print settingswindow.FileSystem.exists()
    # print settingswindow.Restore.exists()
    # print settingswindow.Welcome.exists()
    #
    # wizard = WindowsWizardElement("Email", "Email")
    # wizard.wait_window()
    # print wizard.window.EmailAddressEdit.exists()
    # print wizard.window.EmailAddressEdit.exists()
    # print wizard.window["EmailAddressEdit"].exists()
    # print wizard.window["EmailAddressEdit"].texts()[0]
    # wizard.window.EmailAddressEdit.set_text("testuser@mozy.com")
    # wizard.window.PasswordEdit.set_text("testuser@mozy.com")
    # wizard.window.NextButton.Click()
    # exit()
    #
    # error = WindowsErrorElement("wxWindowClassNR1", "wxWindowClassNR1")
    # error.wait_window()
    # print error.window.wxWindowClassNR1.exists()
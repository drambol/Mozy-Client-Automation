from lib.platformhelper import PlatformHelper

if PlatformHelper.is_win():
    from pywinauto.application import Application

from windows_gui_base import WindowsGUIBaseElement


class WindowsWizardElement(WindowsGUIBaseElement):

    def __init__(self, name, matcher, element_wait_time=None):
        self.title = self.oem + " Setup Wizard"

        self._element_wait_time = element_wait_time or 20

        # self._app = Application().connect(title_re=self.title)

        super(WindowsWizardElement, self).__init__(name, matcher, self.element_wait_time)

        # self.wait_window(title=self.title, visible_only=True)

    def wait_window(self):
        self.wait_windows_ready(title=self.title, visible_only=True)
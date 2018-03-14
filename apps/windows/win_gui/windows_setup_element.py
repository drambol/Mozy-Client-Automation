
from windows_gui_base import WindowsGUIBaseElement


class WindowsSetupElement(WindowsGUIBaseElement):

    def __init__(self, name, matcher, element_wait_time=None):
        self.title = self.oem + " Setup"
        self._element_wait_time = element_wait_time or 30


        super(WindowsSetupElement, self).__init__(name, matcher, self.element_wait_time)
        # self.wait_window(title=self.title, enabled_only = True)


    def wait_window(self):
        self.wait_windows_ready(title=self.title, enabled_only=True)
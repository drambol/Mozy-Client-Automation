
from windows_gui_base import WindowsGUIBaseElement


class WindowsSettingsElement(WindowsGUIBaseElement):

    def __init__(self, name, matcher, element_wait_time=None):
        self.title = self.oem + " - Settings"

        self._element_wait_time = element_wait_time or 30

        # self._app = Application().connect(title_re=self.title)

        super(WindowsSettingsElement, self).__init__(name, matcher, self.element_wait_time)
        # self.wait_window(title=self.title, class_name=u'wxWindowClassNR')

    def wait_window(self):
        self.wait_windows_ready(title=self.title, class_name=u'wxWindowClassNR')


class WindowsProxySettingsElement(WindowsGUIBaseElement):
    def __init__(self, name, matcher, element_wait_time=None):
        self.title = "Proxy Settings"

        self._element_wait_time = element_wait_time or 30

        # self._app = Application().connect(title_re=self.title)

        super(WindowsProxySettingsElement, self).__init__(name, matcher, self.element_wait_time)
        # self.wait_window(title=self.title, class_name=u'wxWindowClassNR')

    def wait_window(self):
        self.wait_windows_ready(title=self.title)


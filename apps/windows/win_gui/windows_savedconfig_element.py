
from windows_gui_base import WindowsGUIBaseElement


class WindowsSavedConfigElement(WindowsGUIBaseElement):

    def __init__(self, name, matcher, element_wait_time=None):
        self.title = "Use Saved Configuration"

        self._element_wait_time = element_wait_time or 10

        # self._app = Application().connect(title_re=self.title)

        super(WindowsSavedConfigElement, self).__init__(name, matcher, self.element_wait_time)



    def wait_window(self):
        self.wait_windows_ready(title_re=self.title)
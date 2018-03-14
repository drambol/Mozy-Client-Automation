
from windows_gui_base import WindowsGUIBaseElement


class WindowsSaveKeyElement(WindowsGUIBaseElement):

    def __init__(self, name, matcher, element_wait_time=None):
        self.title = "Save Key"

        self._element_wait_time = element_wait_time or 5

        # self._app = Application().connect(title_re=self.title)

        super(WindowsSaveKeyElement, self).__init__(name, matcher, self.element_wait_time)
        # self.wait_window(title_re=self.title)

    def wait_window(self):
        self.wait_windows_ready(title_re=self.title)

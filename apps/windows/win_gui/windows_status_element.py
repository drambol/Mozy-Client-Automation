from lib.platformhelper import PlatformHelper

if PlatformHelper.is_win():
    from pywinauto import timings
    from pywinauto.application import Application
    from pywinauto.findwindows import find_windows

from windows_gui_base import WindowsGUIBaseElement



class WindowsStatusElement(WindowsGUIBaseElement):

    def __init__(self, name, matcher, element_wait_time=None):
        self.title = self.oem + " - Status"

        self._element_wait_time = element_wait_time or 20

        # self._app = Application().connect(title_re=self.title)

        super(WindowsStatusElement, self).__init__(name, matcher, self.element_wait_time)
        # self.wait_window(title=self.title, class_name=u'wxWindowClassNR')


    def wait_window(self):
        self.wait_windows_ready(title=self.title, class_name=u'wxWindowClassNR')
    # def wait_window(self, ):
    #     WindowsGUIBaseElement.wait_window(title=self.title, class_name=u'wxWindowClassNR')

        # self.title = self.oem + " - Status"
        # self._app = Application().start(Windows_Controller(self.oem).statusapp)
        # self._app = Application().connect(title=self.oem + " - Status")

        # def checkwindow():
        #     self._handle = find_windows(title=self.title, class_name=u'wxWindowClassNR')[0]
        #     return self._handle
        #
        # timings.WaitUntilPasses(self.element_wait_time, 1, checkwindow)
        # self._window = self.app.window_(handle=self._handle)
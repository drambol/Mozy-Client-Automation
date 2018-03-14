
from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil

from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_errordialog_element import WindowsErrorElement

class WindowsErrorDialog(WindowsUIBase):

    elements = []
    # Error Code Link
    elements.append(WindowsErrorElement('wxWindowClassNR1', 'wxWindowClassNR1'))
    elements.append(WindowsErrorElement('OKButton', 'OKButton'))

    def __init__(self, oem="mozypro"):
        # super(LoginDialog, self).__init__()
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"

        super(WindowsErrorDialog, self).__init__()



    @property
    def errordialog(self):
        return self._errordialog

    def apply(self):
        WindowsGUIUtil.click_button(self.OKButton)

    def get_errorcode(self):
        # http://mozypro.com/error/ConnectionError7
        # return ConnectionError7
        textfiled = self.wxWindowClassNR1
        errorcode_link = textfiled.window_text()
        return errorcode_link.split("/")[-1]

if __name__ == "__main__":
    dg = WindowsErrorDialog("mozypro")
    # status.backup_button.Click()
    # print dg.errordialog.print_control_identifiers()
    # print dg.errordialog.wxWindowClassNR1.window_text()
    print dg.get_errorcode()
    dg.apply()
    # dg.errordialog.wxWindowClassNR1.set_
    # # dg.errordialog.WaitNot("visible")
    # dg.errordialog.OKButton
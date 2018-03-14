
from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil

from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_selectkeyfile_element import SelectFileElement

class SelectFileDialog(WindowsUIBase):

    elements = []
    # Error Code Link
    elements.append(SelectFileElement('wxWindowClassNR1', 'wxWindowClassNR1'))
    elements.append(SelectFileElement('SaveButton', 'SaveButton'))
    elements.append(SelectFileElement('CancelButton', 'CancelButton'))

    def __init__(self, oem="mozypro"):
        # super(LoginDialog, self).__init__()
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"

        super(SelectFileDialog, self).__init__()


    def apply(self):
        savebutton = self.SaveButton
        if WindowsGUIUtil.is_visible(savebutton):
            WindowsGUIUtil.click_button(savebutton)

    def cancel(self):
        cancelbutton = self.CancelButton
        if WindowsGUIUtil.is_visible(cancelbutton):
            WindowsGUIUtil.click_button(cancelbutton)

    def exists(self):
        if WindowsGUIUtil.is_visible(self.SaveButton):
            return True
        else:
            return False

if __name__ == "__main__":
    dg = SelectFileDialog("mozypro")
    # status.backup_button.Click()
    # print dg.errordialog.print_control_identifiers()
    # print dg.errordialog.wxWindowClassNR1.window_text()
    print dg.get_errorcode()
    dg.apply()
    # dg.errordialog.wxWindowClassNR1.set_
    # # dg.errordialog.WaitNot("visible")
    # dg.errordialog.OKButton
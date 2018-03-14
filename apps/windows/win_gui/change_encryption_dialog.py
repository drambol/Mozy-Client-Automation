
from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil

from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_changekey_element import WindowsChangeEncryptionKeyElement


class ChangeEncryptionKeyDialog(WindowsUIBase):

    elements = []
    elements.append(WindowsChangeEncryptionKeyElement('OKButton', 'OKButton'))
    elements.append(WindowsChangeEncryptionKeyElement('CancelButton', 'CancelButton'))

    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"

        super(ChangeEncryptionKeyDialog, self).__init__()


    @property
    def changeencryptiondialog(self):
        return self._changeencryptiondialog


    def apply(self):
        okbutton = self.OKButton
        if WindowsGUIUtil.is_visible(okbutton):
            WindowsGUIUtil.click_button(okbutton)

    def cancel(self):
        cancelbutton = self.CancelButton
        if WindowsGUIUtil.is_visible(cancelbutton):
            WindowsGUIUtil.click_button(cancelbutton)


if __name__ == "__main__":

    changeencryptiondlg = ChangeEncryptionKeyDialog("mozypro")
    changeencryptiondlg.apply()


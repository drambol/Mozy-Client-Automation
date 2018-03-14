
from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil

from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_confirmreplacemachine_element import WindowsConfirmReplaceMachineElement


class ConfirmReplaceMachineDialog(WindowsUIBase):

    elements = []
    elements.append(WindowsConfirmReplaceMachineElement('YesButton', 'YesButton'))
    elements.append(WindowsConfirmReplaceMachineElement('NoButton', 'NoButton'))

    def __init__(self, oem="mozypro"):

        super(ConfirmReplaceMachineDialog, self).__init__()

    def apply(self):
        WindowsGUIUtil.click_button(self.YesButton)

    def cancel(self):
        WindowsGUIUtil.click_button(self.NoButton)

if __name__ == "__main__":
    confirmreplace_dlg = ConfirmReplaceMachineDialog("MozyEnterprise")
    confirmreplace_dlg.YesButton.exists()
    # confirmreplace_dlg.apply()
    confirmreplace_dlg.cancel()

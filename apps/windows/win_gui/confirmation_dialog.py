
from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil

from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_wizard_element import WindowsWizardElement


class ConfirmationDialog(WindowsUIBase):

    elements = []
    elements.append(WindowsWizardElement('SettingsDialog', 'SettingsDialog'))
    elements.append(WindowsWizardElement('FinishButton', 'FinishButton'))
    elements.append(WindowsWizardElement('BackButton', 'BackButton'))
    elements.append(WindowsWizardElement('CancelButton', 'CancelButton'))

    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"

        print "Initial Confirmation Dialog"

        super(ConfirmationDialog, self).__init__()

    @property
    def confirmdialog(self):
        return self._confirmdialog

    @property
    def finishbutton(self):
        return self._finishbutton

    @property
    def backbutton(self):
        return self._backbutton

    @property
    def cancelbutton(self):
        return self._cancelbutton

    def apply(self):
        if WindowsGUIUtil.is_visible(self.SettingsDialog):
            WindowsGUIUtil.click_button(self.FinishButton)

    def back(self):
        back_button = self.BackButton
        if WindowsGUIUtil.is_visible(back_button):
            WindowsGUIUtil.click_button(back_button)

    def cancel(self):
        cancel_button = self.CancelButton
        if WindowsGUIUtil.is_visible(cancel_button):
            WindowsGUIUtil.click_button(cancel_button)


if __name__ == "__main__":
    confirm = ConfirmationDialog("mozypro")
    print confirm.print_control_identifiers()
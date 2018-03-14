
from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil

from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_wizard_element import WindowsWizardElement


class AddReplaceMachineDialog(WindowsUIBase):

    elements = []
    elements.append(WindowsWizardElement('AddComputer', 'AddComputer'))    # AddThisComputer
    elements.append(WindowsWizardElement('ReplaceSelectedComputer', 'ReplaceSelectedComputer'))
    elements.append(WindowsWizardElement('ReplaceComputerCombobox', 'ReplaceComputerCombobox'))
    elements.append(WindowsWizardElement('NextButton', 'NextButton'))
    elements.append(WindowsWizardElement('BackButton', 'BackButton'))
    elements.append(WindowsWizardElement('CancelButton', 'CancelButton'))

    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"

        super(AddReplaceMachineDialog, self).__init__()

    def add_new_computer(self):
        addcomputerbutton = self.AddComputer
        # print addcomputerbutton.exists()
        # print addcomputerbutton.verify_visible()
        WindowsGUIUtil.click_radio_button(addcomputerbutton)

    def replace_selected_computer(self, id=-1):
        replacebutton = self.ReplaceSelectedComputer
        replacecombobox = self.ReplaceComputerCombobox
        print replacebutton.exists()
        print replacecombobox.exists()
        WindowsGUIUtil.click_radio_button(replacebutton)
        # select the first computer
        WindowsGUIUtil.select_combobox(replacecombobox, index=id)

    def apply(self):
        WindowsGUIUtil.click_button(self.NextButton)

    def back(self):
        WindowsGUIUtil.click_button(self.BackButton)

    def cancel(self):
        WindowsGUIUtil.click_button(self.CancelButton)

if __name__ == "__main__":
    arm_dialog = AddReplaceMachineDialog("MozyEnterprise")
    # arm_dialog._window.wait('visible')
    print arm_dialog.AddComputer
    print arm_dialog.AddComputer.exists()
    # print arm_dialog.AddComputer.is_visible()
    if arm_dialog.AddComputer.exists():
        arm_dialog.add_new_computer()
        arm_dialog.replace_selected_computer(1)
        arm_dialog.apply()
        # arm.cancel()

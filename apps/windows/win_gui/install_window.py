import time
from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_setup_element import WindowsSetupElement
from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil


class SetupWindow(WindowsUIBase):

    elements = []
    elements.append(WindowsSetupElement('NextButton', '&Next'))

    elements.append(WindowsSetupElement('CancelButton', 'CancelButton'))

    elements.append(WindowsSetupElement('Viewthelicenseagreement', 'View the license agreement'))
    elements.append(WindowsSetupElement('Chooseadifferentinstalllocation', 'Choose a different install location'))

    elements.append(WindowsSetupElement('CheckBox1', 'CheckBox1'))
    elements.append(WindowsSetupElement('CheckBox2', 'CheckBox2'))

    elements.append(WindowsSetupElement('AcceptButton', 'Accept'))
    elements.append(WindowsSetupElement('FinishButton', '&Finish'))
    elements.append(WindowsSetupElement('Welcome', 'Welcome'))

    elements.append(WindowsSetupElement('LocationEdit', 'Edit'))
    elements.append(WindowsSetupElement('AlertIcon', 'Information icon'))

    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"
        print "Initialize Setup Window"
        super(SetupWindow, self).__init__()

    def open_setupwindow(self):
        result = False
        welcome_page = self.Welcome
        if WindowsGUIUtil.is_visible(welcome_page):
            result = True
        return result

    def license_agreement_checked(self):
        licence_select = self.CheckBox1
        result = WindowsGUIUtil.is_selected(licence_select)
        return result

    def location_change_checked(self):
        install_location = self.CheckBox2
        result = WindowsGUIUtil.is_selected(install_location)
        return result

    def choose_license_agreement(self):
        WindowsGUIUtil.click_button(self.Viewthelicenseagreement)

    def choose_location_change(self):
        WindowsGUIUtil.click_button(self.Chooseadifferentinstalllocation)

    def install_start(self):
        InstallPanel(self.oem).install()
        time.sleep(2)

    def cancel(self):
        WindowsGUIUtil.click_button(self.CancelButton)

    def apply(self):
        WindowsGUIUtil.click_button(self.NextButton)
        time.sleep(2)

    def accept(self):
        WindowsGUIUtil.click_button(self.AcceptButton)
        time.sleep(2)

    def finish_and_exit(self):
        WindowsGUIUtil.click_button(self.FinishButton)

    def choose_yes_on_cancel(self):
        CancelPanel(self.oem).click_yes()

    def choose_no_on_cancel(self):
        CancelPanel(self.oem).click_no()

    def set_location(self, path):
        location = self.LocationEdit
        WindowsGUIUtil.input_edit_content(location, path)

    def alert_info_popup(self):
        time.sleep(20)
        alert_info = self.AlertIcon
        if WindowsGUIUtil.is_visible(alert_info):
            print "The alert info appears successfully."
        else:
            print "The alert info does not appear rightly."


class InstallPanel(WindowsUIBase):
    elements=[]
    elements.append(WindowsSetupElement('InstallButton', '&Install'))
    elements.append(WindowsSetupElement('CancelButton', 'CancelButton'))


    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"
        print "Initialize Setup Window"
        super(InstallPanel, self).__init__()


    def install(self):
        time.sleep(2)
        if WindowsGUIUtil.is_visible(self.InstallButton):
            WindowsGUIUtil.click_button(self.InstallButton)


class CancelPanel(WindowsUIBase):
    elements = []
    elements.append(WindowsSetupElement('YesButton', '&Yes'))
    elements.append(WindowsSetupElement('NoButton', '&No'))

    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"
        print "Initialize Setup Window"
        super(CancelPanel, self).__init__()

    def click_yes(self):
        WindowsGUIUtil.click_button(self.YesButton)

    def click_no(self):
        WindowsGUIUtil.click_button(self.NoButton)


if __name__ == "__main__":
    setup = SetupWindow("mozypro")
    setup.set_location('E:\\')


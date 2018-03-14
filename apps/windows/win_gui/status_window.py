
import time

from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_status_element import WindowsStatusElement

from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil



class StatusWindow(WindowsUIBase):

    elements = []
    # elements.append(WindowsUIBase('status_window', {'title': u'MozyPro - Status', 'class_name': u'wxWindowClassNR'}))
    elements.append(WindowsStatusElement('ContinueSetup', 'ContinueSetup'))
    elements.append(WindowsStatusElement('StartBackup', 'StartBackup'))
    elements.append(WindowsStatusElement('CancelBackup', 'CancelBackup'))
    elements.append(WindowsStatusElement('RestoreButton', 'RestoreButton'))
    elements.append(WindowsStatusElement('Settings', 'Settings'))
    elements.append(WindowsStatusElement('Details', 'Details'))



    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"

        print "Initial Status Windows"
        super(StatusWindow, self).__init__()


    @property
    def statuswindow(self):
        return self._statuswindow

    def isopen(self, oem="mozypro"):
        """Check Status dialog Title"""
        pass

    def open_logindialog(self):
        # if self.continuesetupbutton.exists:
        continuebutton = self.ContinueSetup
        if continuebutton.exists():
            WindowsGUIUtil.click_button(continuebutton)
            time.sleep(3)
            return True
        else:
            return False

    @property
    def logindialog(self):
        return self._logindialog

    def open(self, windowname):
        if windowname.upper() == "Settings".upper():
            self.open_settingwindow()
        if windowname.upper() == "History".upper():
            self.open_historyspanel()
        if windowname.upper() == "Restore".upper():
            self.open_restorepanel()
        if windowname.upper() == "Login".upper():
            self.open_logindialog()

    def open_restorepanel(self):
        # self.restorebutton.Click()
        WindowsGUIUtil.click_button(self.RestoreButton)
        time.sleep(15)

    def open_settingwindow(self):
        # self.settingsbutton.Click()
        WindowsGUIUtil.click_button(self.Settings)
        time.sleep(10)

    def open_historyspanel(self):
        # self.historybutton.Click()
        WindowsGUIUtil.click_button(self.Details)
        time.sleep(10)

    def startbackup(self):
        # self.backupbutton.Click()
        WindowsGUIUtil.click_button(self.StartBackup)

    def cancelbackup(self):
        # self.backupbutton.Click()
        WindowsGUIUtil.click_button(self.CancelBackup)

    def client_is_activated(self):
        """
        If client is activated, then displays "Start Backup" button.
        Otherwise, displays "Continue Setup" button
        """
        if self.ContinueSetup.exists:
            return False
        else:
            return True


if __name__ == "__main__":
    statuswindow = StatusWindow("mozypro")
    statuswindow.open_logindialog()

import time

from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil

from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_gui_element import WindowsWizardElement

from apps.windows.win_gui.add_replace_machine_dialog import AddReplaceMachineDialog
from apps.windows.win_gui.saved_config_dialog import SavedConfigDialog
from apps.windows.win_gui.set_encryption_dialog import EncryptionDialog
from apps.windows.win_gui.summary_dialog import SummaryDialog
from apps.windows.win_gui.confirmation_dialog import ConfirmationDialog


class LoginDialog(WindowsUIBase):

    elements = []
    elements.append(WindowsWizardElement('EmailAddressEdit', 'EmailAddressEdit'))
    elements.append(WindowsWizardElement('PasswordEdit', 'PasswordEdit'))
    elements.append(WindowsWizardElement('NextButton', 'NextButton'))
    elements.append(WindowsWizardElement('BackButton', 'BackButton'))
    elements.append(WindowsWizardElement('CancelButton', 'CancelButton'))

    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"

        super(LoginDialog, self).__init__()


    @property
    def logindialog(self):
        return self._logindialog

    def is_open(self):
        if self._logindialog is None:
            return False
        else:
            return True


    def apply(self):
        WindowsGUIUtil.click_button(self.NextButton)

    def back(self):
        WindowsGUIUtil.click_button(self.BackButton)

    def cancel(self):
        WindowsGUIUtil.click_button(self.CancelButton)

    def set_keylessinfo(self, username, password):
        email = self.EmailAddressEdit
        pwd = self.PasswordEdit
        try:
            result = WindowsGUIUtil.input_text(email, username)
            if result:
                result = WindowsGUIUtil.input_text(pwd, password)
                if result:
                    self.apply()
        except RuntimeError as e:
            print e
            return False
        else:
            return True

    def keyless_activate(self, username, password, encryptiontype="pkey", key="test1234"):

        # email = self.EmailAddressEdit
        # pwd = self.PasswordEdit
        try:
        #     WindowsGUIUtil.input_text(email, username)
        #
        #     WindowsGUIUtil.input_text(pwd, password)
        #
        #     self.apply()

            time.sleep(20)

            arm_dialog = AddReplaceMachineDialog(self.oem)

            if WindowsGUIUtil.is_visible(arm_dialog.AddComputer):
                arm_dialog.add_new_computer()
                # arm_dialog.replace_selected_computer(-1)
                arm_dialog.apply()

            time.sleep(20)


            print "....Set encryption...."
            encryption_dialog = EncryptionDialog(self.oem)
            # if encryption_dialog.Button4 or encryption_dialog.UseDefaultKeyButton or encryption_dialog.UseRandomKeyButton or encryption_dialog.UsePersonalKeyButton:
            #     encryption_dialog.set_encyption_key(encryptiontype, key)
            encryption_dialog.set_encyption_key(encryptiontype, key)
            time.sleep(2)

            summary_dialog = SummaryDialog(self.oem)
            # if summary_dialog.NextButton.exists():
            if WindowsGUIUtil.is_visible(summary_dialog.NextButton):
                summary_dialog.apply()
            time.sleep(2)

            confirm_dialog = ConfirmationDialog(self.oem)
            # if confirm_dialog.SettingsDialog:
            if WindowsGUIUtil.is_visible(confirm_dialog.SettingsDialog):
                confirm_dialog.apply()
            time.sleep(2)

        except RuntimeError as e:
            print e
            return False
        else:
            return True

    def key_activate(self, productkey, encryptiontype="pkey", key="test1234"):
        pass

class LoginConfirmDialog(object):

    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"

        super(LoginConfirmDialog, self).__init__()


        element_wait_time = 30
        windowtitle = self.oem + " Setup Wizard"

        self.wait_ready(windowtitle, element_wait_time)


        # Click Cancel Button - Dialog
        self._yesbutton = self.loginconfirmdialog.Button1
        self._nobutton = self.loginconfirmdialog.Button2


    @property
    def loginconfirmdialog(self):
        return self._loginconfirmdialog

    @property
    def yesbutton(self):
        return self._yesbutton

    @property
    def nobutton(self):
        return self._nobutton


if __name__ == "__main__":
    logindialog = LoginDialog("MozyEnterprise")
    # status.backup_button.Click()
    # print status.startbackup
    logindialog.activate("clientqa_ent_pkey@mozy.com", "Test_1234")
    # logindialog.activate("aaa_123_b@mozy.com", "sst_112e")
    # print logindialog.NextButton.exists()
    # print logindialog.NoButton.exists()

    # saveddialog = SavedConfigDialog("mozypro")
    # saveddialog.NoButton.Click()
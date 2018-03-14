
import time

from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil

from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_wizard_element import WindowsWizardElement

from apps.windows.win_gui.add_replace_machine_dialog import AddReplaceMachineDialog
from apps.windows.win_gui.saved_config_dialog import SavedConfigDialog
from apps.windows.win_gui.set_encryption_dialog import EncryptionDialog
from apps.windows.win_gui.change_encryption_dialog import ChangeEncryptionKeyDialog
from apps.windows.win_gui.summary_dialog import SummaryDialog
from apps.windows.win_gui.confirmation_dialog import ConfirmationDialog


class LoginDialog(WindowsUIBase):

    elements = []
    # Product Key
    elements.append(WindowsWizardElement('UseProductKey', 'UseProductKey'))
    elements.append(WindowsWizardElement('ProductKeyEdit', 'ProductKeyEdit'))
    # Keyless
    elements.append(WindowsWizardElement('UseUsernamePassword', 'UseUsernamePassword'))
    elements.append(WindowsWizardElement('EmailAddressEdit', 'EmailAddressEdit'))
    elements.append(WindowsWizardElement('PasswordEdit', 'PasswordEdit'))
    # FedID
    elements.append(WindowsWizardElement('UseSingleSignon', 'UseSingleSignon'))
    elements.append(WindowsWizardElement('HttpEdit', 'HttpEdit'))

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

    def choose_keyless(self):
        usekeyless = self.UseUsernamePassword
        if WindowsGUIUtil.is_visible(usekeyless):
            WindowsGUIUtil.click_button(usekeyless)

    def choose_keyed(self):
        usekey = self.UseProductKey
        if WindowsGUIUtil.is_visible(usekey):
            WindowsGUIUtil.click_button(usekey)

    def choose_fedid(self):
        usesinglesignon = self.UseSingleSignon
        if WindowsGUIUtil.is_visible(usesinglesignon):
            WindowsGUIUtil.click_button(usesinglesignon)

    def set_keylessinfo(self, username, password):
        try:
            if self.set_email(username) and self.set_password(password):
                self.apply()
        except RuntimeError as e:
            print e
            return False
        else:
            return True

    def set_productkey(self, productkey, username, password):
        product_key = self.ProductKeyEdit
        email = self.EmailAddressEdit

        try:
            result = WindowsGUIUtil.input_text(product_key, productkey)
            if result:
                result = WindowsGUIUtil.input_text(email, username)
                if result:
                    self.apply()
        except RuntimeError as e:
            print e
            return False
        else:
            return True

    def set_email(self, username):
        try:
            email = self.EmailAddressEdit
            if WindowsGUIUtil.is_visible(email):
                WindowsGUIUtil.input_text(email, username)

        except RuntimeError as e:
            print e
            return False
        else:
            return True

    def set_password(self, password="Test_1234"):
        try:
            pwd = self.PasswordEdit
            # if WindowsGUIUtil.is_visible(pwd):
            #     WindowsGUIUtil.input_text(pwd, password)
            WindowsGUIUtil.input_text(pwd, password)

        except RuntimeError as e:
            print e
            return False
        else:
            return True

    def set_subdomain(self, subdomain="test_subdomain"):
        sub_domain = self.HttpEdit
        try:
            result = WindowsGUIUtil.input_text(sub_domain, subdomain)
            if result:
                self.apply()
        except RuntimeError as e:
            print e
            return False
        else:
            return True

    def add_replace_machine(self, replace=True):
        arm_dialog = AddReplaceMachineDialog(self.oem)

        if WindowsGUIUtil.is_visible(arm_dialog.AddComputer):
            if replace:
                # HardCode: Replace the last machine
                arm_dialog.replace_selected_computer(-1)
            else:
                arm_dialog.add_new_computer()

            arm_dialog.apply()
        # arm_dialog.add_new_computer()
        # arm_dialog.apply()

    # def set_encryption(self, encryptiontype, key, is_multiencryption=False):
    #     # Skip load encryption dialog
    #     if is_multiencryption and encryptiontype.upper() in ["CKEY", "KMIP", "DEFAULT"]:
    #         pass
    #     else:
    #         encryption_dialog = EncryptionDialog(self.oem)
    #         encryption_dialog.set_encyption_key(encryptiontype, key, is_multiencryption)

    def change_encrption(self, apply=True):
        changeencryptiondlg = ChangeEncryptionKeyDialog("mozypro")
        if apply:
            changeencryptiondlg.apply()
        else:
            changeencryptiondlg.cancel()


    def close_summary(self):
        summary_dialog = SummaryDialog(self.oem)
        summary_dialog.apply()

    def close_confirmation(self):
        confirm_dialog = ConfirmationDialog(self.oem)
        # if confirm_dialog.SettingsDialog:
        confirm_dialog.apply()

    def keyless_activate(self, username, password, encryptiontype="pkey", key="test1234", **kwargs):

        print kwargs
        is_exist = kwargs['is_exist'].upper()
        is_multiencryption = kwargs['multiencryption'] or False
        try:
            if is_exist == "NEW":
                pass
            else:
                # Select keyless option
                self.choose_keyless()

            # Enter username & pwd...
            self.set_keylessinfo(username, password)

            if is_exist == "NEW":
                time.sleep(20)
            else:
                print "Existing user"
                time.sleep(5)
                print "Add or replace machine"
                self.add_replace_machine(replace=True)
                time.sleep(15)

            print "....Set encryption...."
            # self.set_encryption(encryptiontype, key, is_multiencryption)
            encryption_dialog = EncryptionDialog(self.oem)
            encryption_dialog.set_encyption_key(encryptiontype, key, is_multiencryption)
            time.sleep(2)

            self.close_summary()
            time.sleep(2)

            self.close_confirmation()
            time.sleep(2)

        except RuntimeError as e:
            print e
            return False
        else:
            return True

    def key_activate(self, productkey, username, password, encryptiontype="pkey", key="test1234", **kwargs):
        print kwargs
        is_exist = kwargs['is_exist'].upper()
        try:
            print "Select productkey option"
            self.choose_keyed()

            print "Set Product Key"
            print productkey[0]
            self.set_productkey(productkey[0], username, password)

            print "Check password Edit"
            if self.set_password(password):
                self.apply()
            time.sleep(20)

            # print "Check add or replace machine"
            # self.add_replace_machine(replace=False)
            # time.sleep(20)
            if is_exist == "NEW":
                print "NEW...."
                time.sleep(20)
            else:
                print "Existing user"
                time.sleep(5)
                print "Add or replace machine"
                self.add_replace_machine(replace=False)
                time.sleep(15)

            print "Check encryption dialog"
            # self.set_encryption(encryptiontype, key)
            encryption_dialog = EncryptionDialog(self.oem)
            encryption_dialog.set_encyption_key(encryptiontype, key)
            time.sleep(2)

            self.close_summary()
            time.sleep(2)

            self.close_confirmation()
            time.sleep(2)

        except RuntimeError as e:
            print e
            return False
        else:
            return True

    def open_fedidpage(self, subdomain):
        try:
            self.choose_fedid()
            self.set_subdomain(subdomain)
            time.sleep(10)

        except RuntimeError as e:
            print e
            return False
        else:
            return True

    def fedid_activate(self, encryptiontype="pkey", key="test1234", **kwargs):
        is_exist = kwargs['is_exist'].upper()
        """
        FedID supports different Auth_Type: LDAP, Horizon, Mozy
        Currently we support LDAP here.
        """
        try:
            if is_exist == "NEW":
                print "NEW...."
                time.sleep(20)
            else:
                print "Existing user"
                time.sleep(5)
                print "Add or replace machine"
                self.add_replace_machine(replace=False)
                time.sleep(15)

            print "Check encryption dialog"
            # self.set_encryption(encryptiontype, key)
            encryption_dialog = EncryptionDialog(self.oem)
            encryption_dialog.set_encyption_key(encryptiontype, key)
            time.sleep(2)

            self.close_summary()
            time.sleep(2)

            self.close_confirmation()
            time.sleep(2)

        except RuntimeError as e:
            print e
            return False
        else:
            return True

class LoginConfirmDialog(object):

    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"

        super(LoginConfirmDialog, self).__init__()


        element_wait_time = 20
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
    logindialog = LoginDialog("mozypro")
    logindialog.choose_fedid()

    # logindialog.key_activate("aaaaaaascccccdddd", "clientqa_ent_pkey@mozy.com", "Test_1234")

    # logindialog = LoginDialog("MozyEnterprise")
    # # status.backup_button.Click()
    # # print status.startbackup
    # logindialog.activate("clientqa_ent_pkey@mozy.com", "Test_1234")
    # # logindialog.activate("aaa_123_b@mozy.com", "sst_112e")
    # # print logindialog.NextButton.exists()
    # # print logindialog.NoButton.exists()
    #
    # # saveddialog = SavedConfigDialog("mozypro")
    # # saveddialog.NoButton.Click()
import time
from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil

from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_wizard_element import WindowsWizardElement
from apps.windows.win_gui.windows_keyconfirm_element import WindowsKeyConfirmElement
from apps.windows.win_gui.windows_savekey_element import WindowsSaveKeyElement

from apps.windows.win_gui.select_file_dialog import SelectFileDialog


class EncryptionDialog(WindowsUIBase):

    elements = []
    # Radio buttons: Use New/Default Key/Personal Key/CKey
    elements.append(WindowsWizardElement('Button4', 'Button4'))
    elements.append(WindowsWizardElement('UseDefaultKeyButton', 'UseDefaultKeyButton'))
    elements.append(WindowsWizardElement('UseRandomKeyButton', 'UseRandomKeyButton'))
    elements.append(WindowsWizardElement('UsePersonalKeyButton', 'UsePersonalKeyButton'))

    # Enter pkey, import pkey file
    elements.append(WindowsWizardElement('EnterKeyButton', 'EnterKeyButton'))
    elements.append(WindowsWizardElement('EnterKeyEdit', 'EnterKeyEdit'))
    elements.append(WindowsWizardElement('ImportKeyButton', 'ImportKeyButton'))
    elements.append(WindowsWizardElement('Browse', 'Browse'))
    elements.append(WindowsWizardElement('ImportKeyEdit', 'ImportKeyEdit'))

    # Buttons in encryption dialog
    elements.append(WindowsWizardElement('NextButton', 'NextButton'))
    elements.append(WindowsWizardElement('BackButton', 'BackButton'))
    elements.append(WindowsWizardElement('CancelButton', 'CancelButton'))


    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"
        print "Initialize Set Encryption Dialog"

        super(EncryptionDialog, self).__init__()



    def set_defaultkey(self):
        # self.usedefaultkeybutton.CheckByClick()
        self.apply()

    def set_randomkey(self):
        self.userandomkeybutton.CheckByClick()
        self.apply()

    def set_pkey(self, pkey="test1234"):
        usepkeybutton = self.UsePersonalKeyButton
        enterkeybutton = self.EnterKeyButton
        if WindowsGUIUtil.is_visible(usepkeybutton):
            WindowsGUIUtil.click_radio_button(usepkeybutton)
        elif WindowsGUIUtil.is_visible(enterkeybutton):
            WindowsGUIUtil.click_radio_button(enterkeybutton)

        WindowsGUIUtil.input_text(self.EnterKeyEdit, pkey)
        # self.usepkeybutton.CheckByClick()
        # self.enterkeybutton.CheckByClick()
        # self.enterkeyedit.type_keys(pkey)
        self.apply()

        keyconfirmdialog = KeyConfirmDialog(self.oem)
        keyconfirmdialog.apply()

        # if WindowsGUIUtil.is_visible(self.Button4):
        #     # TODO: More encryption related code
        #     print "Use new encryption"
        #     self.apply()
        # else:
        #     keyconfirmdialog = KeyConfirmDialog(self.oem)
        #     keyconfirmdialog.apply()


    def use_newencryption(self):
        usenewencryptionbutton = self.Button4
        if usenewencryptionbutton:
            WindowsGUIUtil.click_radio_button(usenewencryptionbutton)
            self.apply()


    def set_encyption_key(self, type="pkey", key="test1234", is_multiencryption=False):
        # TODO: Support multiple encryption types
        if type.upper() == "PKEY":
            print "Set Private Key."
            return self.set_pkey(pkey=key)
        elif type.upper() == "DEFAULT":
            # return self.set_defaultkey()
            print "Skip Default Key."
            pass
        elif type.upper() == "RANDOM":
            if is_multiencryption:
                return self.set_randomkey()
            else:
                self.apply()
                time.sleep(2)
                savekey_dialog = SaveKeyDialog("mozypro")
                if savekey_dialog.exists():
                    savekey_dialog.cancel()
                selectfile_dlg = SelectFileDialog("mozypro")
                if selectfile_dlg.exists():
                    selectfile_dlg.cancel()

        elif type.upper() == "KMIP":
            pass
        elif type.upper() == "CKEY":
            # There is no encryption dialog if CKey is the only choice
            pass
        else:
            raise TypeError('ERROR: Unknown Encryption Type.')

    @property
    def encryptiondialog(self):
        return self._encryptiondialog


    @property
    def usenewencryptionbutton(self):
        return self._usenewencryptionbutton

    @property
    def usedefaultkeybutton(self):
        return self._usedefaultkeybutton

    @property
    def userandomkeybutton(self):
        return self._userandomkeybutton

    @property
    def usepkeybutton(self):
        return self._usepkeybutton

    @property
    def enterkeybutton(self):
        return self._enterkeybutton

    @property
    def importkeybutton(self):
        return self._importkeybutton

    @property
    def browsebutton(self):
        return self._browsebutton

    @property
    def enterkeyedit(self):
        return self._enterkeyedit

    @property
    def nextbutton(self):
        return self._nextbutton

    def apply(self):
        # self.nextbutton.Click()
        okbutton = self.NextButton
        if WindowsGUIUtil.is_visible(okbutton):
            WindowsGUIUtil.click_button(okbutton)
        # WindowsGUIUtil.click_button(self.NextButton)


class KeyConfirmDialog(WindowsUIBase):

    elements = []
    elements.append(WindowsKeyConfirmElement('OKButton', 'OKButton'))
    elements.append(WindowsKeyConfirmElement('CancelButton', 'CancelButton'))

    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"

        super(KeyConfirmDialog, self).__init__()


    @property
    def keyconfirmdialog(self):
        return self._keyconfirmdialog


    @property
    def okbutton(self):
        return self._okbutton

    @property
    def nobutton(self):
        return self._nobutton

    def apply(self):
        # self.OKButton.Click()
        # okbutton = self.OKButton
        # okbutton.set_focus()
        # okbutton.DoubleClick()
        okbutton = self.OKButton
        if WindowsGUIUtil.is_visible(okbutton):
            WindowsGUIUtil.click_button(okbutton)

    def cancel(self):
        cancelbutton = self.CancelButton
        if WindowsGUIUtil.is_visible(cancelbutton):
            WindowsGUIUtil.click_button(cancelbutton)


class SaveKeyDialog(WindowsUIBase):

    elements = []
    elements.append(WindowsSaveKeyElement('OKButton', 'OKButton'))
    elements.append(WindowsSaveKeyElement('CancelButton', 'CancelButton'))

    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"

        super(SaveKeyDialog, self).__init__()


    @property
    def savekeydialog(self):
        return self._savekeydialog

    def exists(self):
        if WindowsGUIUtil.is_visible(self.OKButton):
            return True
        else:
            return False

    @property
    def okbutton(self):
        return self._okbutton

    @property
    def nobutton(self):
        return self._nobutton

    def apply(self):
        # self.OKButton.Click()
        # okbutton = self.OKButton
        # okbutton.set_focus()
        # okbutton.DoubleClick()
        okbutton = self.OKButton
        if WindowsGUIUtil.is_visible(okbutton):
            WindowsGUIUtil.click_button(okbutton)

    def cancel(self):
        cancelbutton = self.CancelButton
        if WindowsGUIUtil.is_visible(cancelbutton):
            WindowsGUIUtil.click_button(cancelbutton)


if __name__ == "__main__":
    # encyrptiondlg = EncryptionDialog("MozyEnterprise")
    # keyconfirm_dialog = KeyConfirmDialog("MozyEnterprise")
    encyrptiondlg = EncryptionDialog("mozypro")
    encyrptiondlg.apply()
    #
    # savekey_dialog = SaveKeyDialog("mozypro")
    # savekey_dialog.cancel()
    selectfile_dlg = SelectFileDialog("mozypro")
    selectfile_dlg.cancel()
    # savekey_dialog.cancel()

    # keyconfirm_dialog = KeyConfirmDialog("mozypro")
    # encyrptiondlg.set_encyption_key("pkey", "test1234")
    # encyrptiondlg.NextButton.Click()
    # keyconfirm_dialog.apply()
    # keyconfirm_dialog.cancel()



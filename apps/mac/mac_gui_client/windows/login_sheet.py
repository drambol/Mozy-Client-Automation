#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from apps.mac.mac_lib.mozy_ui_element import MacMozyUIBase, Element
from apps.mac.mac_lib.mac_ui_util import MacUIUtils
# from lib.platformhelper import PlatformHelper
from apps.mac.mac_gui_client.windows.personal_pkey_dialog import Personal_Key_Dialog
from apps.mac.mac_gui_client.windows.add_replace_machine_sheet import AddReplaceMachineSheet
from apps.mac.mac_gui_client.windows.select_encryption_type_sheet import SelectEncryptionTypeSheet


class LoginSheet(MacMozyUIBase):

    """
    description: login page
    """
    elements = []
    elements.append(Element("tf_email", {'AXRole': 'AXTextField', 'AXIdentifier': "_NS:80"}))
    elements.append(Element("tf_password", {'AXRole': 'AXTextField', 'AXIdentifier': "_NS:40"}))
    elements.append(Element("btn_next", {'AXRole': 'AXButton', 'AXTitle': 'Next'}))
    elements.append(Element("btn_cancel", {'AXRole': 'AXButton', 'AXTitle': 'Cancel'}))
    elements.append(Element("btn_previous", {'AXRole': 'AXButton', 'AXTitle': 'Previous'}))
    elements.append(Element("btn_preferences", {'AXRole': 'AXButton', 'AXTitle': 'Preferences'}, element_wait_time=60))
    elements.append(Element("st_description", {'AXRole': 'AXStaticText', 'AXIdentifier': '_NS:64'}))
    elements.append(Element("ta_pkey", {'AXRole': 'AXTextArea', 'AXIdentifier': '_NS:61'}, element_wait_time=60))
    elements.append(Element("btn_pknext", {'AXRole': 'AXButton', 'AXTitle': 'Next', 'AXIdentifier': '_NS:49'}))
    elements.append(Element("cb_pk", {'AXRole': 'AXCheckBox', 'AXIdentifier': '_NS:9'}))
    elements.append(Element("btn_pkcancel", {'AXRole': 'AXButton', 'AXTitle': 'Cancel', 'AXIdentifier': '_NS:54'}))

    def __init__(self):
        super(LoginSheet, self).__init__()

    def set_credential_with(self, username, password):
        MacUIUtils.mouse_click_center(self.tf_email)
        MacUIUtils.empty_text(self.tf_email)
        MacUIUtils.input_text(self.tf_email, username)
        MacUIUtils.empty_text(self.tf_password)
        MacUIUtils.input_text(self.tf_password, password)
        MacUIUtils.click_button(self.btn_next)

    def activate(self, username, password, **kwargs):
        """

        :param username:
        :param password:
        :return:
        """
        self.set_credential_with(username, password)

        sh_select_encryption = SelectEncryptionTypeSheet()
        if sh_select_encryption.rd_mozykey:
            sh_select_encryption.activate_with_mozykey()

        add_machine_sh = AddReplaceMachineSheet()
        if add_machine_sh.rd_add:
            add_machine_sh.add_new_machine()

        if kwargs.get('keytext'):
            text = kwargs['keytext']
            is_pkey = self.ta_pkey
            if is_pkey:
                MacUIUtils.input_text(is_pkey, text)
                MacUIUtils.wait_enabled(self.btn_pknext, timeout=60)
                MacUIUtils.click_button(self.btn_pknext)
                save_dialog = Personal_Key_Dialog()
                MacUIUtils.click_button(save_dialog.btn_cancel)
                MacUIUtils.click_checkbox(self.cb_pk, check=True)
                MacUIUtils.click_button(self.btn_pknext)

        MacUIUtils.click_button(self.btn_preferences)

    def description_text(self):

        result = self.st_description.AXValue

        return result

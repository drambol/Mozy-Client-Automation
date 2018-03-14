#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from apps.mac.mac_lib.mozy_ui_element import MacMozyUIBase, Element
from apps.mac.mac_lib.mac_ui_util import MacUIUtils


class SelectEncryptionTypeSheet(MacMozyUIBase):

    """
    sheet that show up in activation process where ask user to select encrpytion type
    """
    elements = []
    elements.append(Element("st_encrption", {'AXRole': 'AXStaticText', 'AXIdentifier': "_NS:40"}))
    elements.append(Element("btn_next", {'AXRole': 'AXButton', 'AXTitle': "Next"}))
    elements.append(Element("rd_mozykey", {'AXRole': 'AXRadioButton', 'AXTitle': "Use MozyPro*"}))
    elements.append(Element("rd_personalkey", {'AXRole': 'AXRadioButton', 'AXTitle': "Use a personal key"}))

    def activate_with_mozykey(self):
        MacUIUtils.click_radio_button(self.rd_mozykey)
        MacUIUtils.click_button(self.btn_next)

    def activate_with_pk(self):
        MacUIUtils.click_radio_button(self.rd_personalkey)
        MacUIUtils.click_button(self.btn_next)

    def select_encryption(self, encryption='MOZY'):
        if encryption.upper() == 'MOZY':
            self.activate_with_mozykey()
        elif encryption.upper() == "PK":
            self.activate_with_pk()
        else:
            raise ValueError("encryption type %s is not support" % encryption)
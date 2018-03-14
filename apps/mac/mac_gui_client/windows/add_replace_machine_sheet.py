#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from apps.mac.mac_lib.mozy_ui_element import MacMozyUIBase, Element
from apps.mac.mac_lib.mac_ui_util import MacUIUtils


class AddReplaceMachineSheet(MacMozyUIBase):
    """
    description:
    """


    elements = []
    elements.append(Element('rd_add', {'AXRole': "AXRadioButton", 'AXTitle': 'Add this computer*'}))
    elements.append(Element('rd_replace', {'AXRole': "AXRadioButton", 'AXTitle': 'Replace*'}))
    elements.append(Element('rd_next', {'AXRole': "AXButton", 'AXTitle': 'Next'}))

    def __init__(self):
        super(AddReplaceMachineSheet, self).__init__()

    def add_new_machine(self):
        MacUIUtils.click_radio_button(self.rd_add)
        MacUIUtils.click_button(self.rd_next)

    def replace_machine(self, machine_name):
        pass




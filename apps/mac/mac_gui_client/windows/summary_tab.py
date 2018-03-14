#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from apps.mac.mac_lib.mozy_ui_element import MacMozyUIBase, Element
from apps.mac.mac_lib.mac_ui_util import MacUIUtils


class SummaryTab(MacMozyUIBase):
    """
    description:
    """

    elements = []
    elements.append(Element('rd_summary', {'AXRole': "AXRadioButton", 'AXTitle': 'Summary'}))
    elements.append(Element('btn_backupnow', {'AXRole': 'AXButton', 'AXTitle': 'Back Up Now'}))
    elements.append(Element('btn_history', {'AXRole': 'AXButton', 'AXTitle': 'History*'}))
    elements.append(Element('tb_summary', {'AXRole': 'AXTable', 'AXIdentifier': '_NS:227'}))
    elements.append(Element('st_username', {'AXRole': 'AXStaticText', 'AXIdentifier': '_NS:361'}))
    elements.append(Element('btn_restore', {'AXRole': 'AXButton', 'AXTitle': 'Restore Files'}))

    def __init__(self):

        super(SummaryTab, self).__init__()

    def click_backup(self):
        button_handle = self.btn_backupnow
        MacUIUtils.click_button(button_handle)

    def backup_now(self):
        self.click_backup()

    def get_title_btn_backup(self):
        button = self.btn_backupnow
        return MacUIUtils.get_element_title(button)

    def get_summary_table(self):
        summary_table = MacUIUtils.get_table_cells(self.tb_summary)
        dict = {}
        for row in summary_table:
            key = row[0]
            value = row[1]
            dict[key] = value
        return dict

    def get_current_username(self):
        el = self.st_username
        if el:
             value = el.AXValue
        else:
            value = ''

        return value

    def click_restore(self):
        self.btn_restore.Press()

    def click_history(self):
        self.btn_history.Press()

    def visit(self):
        MacUIUtils.click_radio_button(self.rd_summary)


# class HistorySheet():
#    def __init__(self):
#        pass

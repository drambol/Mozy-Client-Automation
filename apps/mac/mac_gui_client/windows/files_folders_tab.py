#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from apps.mac.mac_lib.mozy_ui_element import MacMozyUIBase, Element
from apps.mac.mac_lib.mac_ui_util import MacUIUtils


class FilesFoldersTab(MacMozyUIBase):
    """
    description:
    """


    elements = []
    elements.append(Element('tab_files', {'AXRole': "AXRadioButton", 'AXTitle': 'Files*'}))
    elements.append(Element('btn_advanced', {'AXRole': "AXButton", 'AXTitle': 'Advanced*'}))
    elements.append(Element('btn_menu_add', {'AXRole': "AXMenuButton", 'AXIdentifier': '_NS:115'}))
    elements.append(Element('btn_menu_remove', {'AXRole': "AXButton", 'AXIdentifier': '_NS:134'}))
    elements.append(Element('pb_root', {'AXRole': "AXPopUpButton"}))
    elements.append(Element('browser_open', {'AXRole': "AXBrowser", 'AXIdentifier': '_NS:9'}))
    elements.append(Element('btn_add', {'AXRole': "AXButton", 'AXTitle': 'Add'}))
    elements.append(Element('btn_OK', {'AXRole': "AXButton", 'AXTitle': 'OK'}))
    elements.append(Element('rg_buttons', {'AXRole': "AXRadioGroup"}))

    def __init__(self):

        super(FilesFoldersTab, self).__init__()

    def visit(self):
        MacUIUtils.click_button(self.tab_files)

    def click_advance_button(self):
        MacUIUtils.click_button(self.btn_advanced)

    def show_add_files_browser(self):
        handle = self.btn_menu_add
        MacUIUtils.click_popmenu_item_by_value(handle, "File/Folder...")

    def show_suggested_backup_sets(self):
        handle = self.btn_menu_add
        MacUIUtils.click_popmenu_item_by_value(handle, "Suggested File/Folder...")

    def select_root_dest(self):
        rg_buttons = self.rg_buttons
        MacUIUtils.click_button(self.rg_buttons.AXChildren[2])
        MacUIUtils.click_popmenu_item_by_value(self.pb_root, MacUIUtils.get_root_volume_name())

    def select_backupdir(self, tree):
        MacUIUtils.select_nodes(self.browser_open, tree, 'AXTextField')
        MacUIUtils.click_button(self.btn_add)

    def click_OK_button(self):
        MacUIUtils.click_button(self.btn_OK)

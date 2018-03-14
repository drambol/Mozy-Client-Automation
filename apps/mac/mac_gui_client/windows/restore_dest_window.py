#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from apps.mac.mac_lib.mozy_ui_element import MacMozyUIBase, Element
from apps.mac.mac_lib.mac_ui_util import MacUIUtils


class RestoreDestWindow(MacMozyUIBase):
    """
    description:
    """
    app_bundle = 'com.mozypro.restore'
    parent_match = {'AXRole': 'AXWindow', 'AXTitle': 'Open'}
    elements =[]
    elements.append(Element("browser_open", {'AXRole': 'AXBrowser', 'AXIdentifier': "_NS:9"},
                            bundle=app_bundle, parent_matcher=parent_match))
    elements.append(Element("btn_choose", {'AXRole': 'AXButton', 'AXTitle': "Choose"},
                            bundle=app_bundle, parent_matcher=parent_match))
    elements.append(Element("pm_root", {'AXRole': 'AXPopUpButton'},
                            bundle=app_bundle, parent_matcher=parent_match))

    def __init__(self):
        super(RestoreDestWindow, self).__init__()

    def select_destination(self, dest):
        self.click_macintosh()
        MacUIUtils.select_nodes(self.browser_open, dest, 'AXTextField')
        MacUIUtils.click_button(self.btn_choose)

    def click_macintosh(self):
        root = MacUIUtils.get_root_volume_name()
        MacUIUtils.click_popmenu_item_by_value(self.pm_root, root)



if __name__ == '__main__':
    RestoreDestWindow().click_macintosh()





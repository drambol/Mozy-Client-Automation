#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from apps.mac.mac_lib.mozy_ui_element import MacMozyUIBase, Element
from apps.mac.mac_lib.mac_ui_util import MacUIUtils
from lib.platformhelper import PlatformHelper
if PlatformHelper.is_mac():
    from atomac import AXKeyCodeConstants


class RestoreAuthWindow(MacMozyUIBase):
    """
    description:
    """
    app_bundle = 'com.mozypro.restore'
    parent_match = {'AXRole': 'AXWindow'}

    elements =[]
    elements.append(Element("tf_password", {'AXRole': 'AXTextField', 'AXRoleDescription': "secure text field"},
                            60, bundle=app_bundle, parent_matcher=parent_match))
    elements.append(Element("btn_continue", {'AXRole': 'AXButton', 'AXTitle': "Continue"},
                            bundle=app_bundle, parent_matcher=parent_match))
    elements.append(Element("btn_cancel", {'AXRole': 'AXButton', 'AXTitle': "Cancel"},
                            bundle=app_bundle, parent_matcher=parent_match))

    def __init__(self):
        super(RestoreAuthWindow, self).__init__()

    def enter_passoword(self, password):
        """

        :param username:
        :param password:
        :return:
        """
        MacUIUtils.mouse_click_center(self.elements[0].root(wait_time=60))
        obj = self.tf_password
        if obj:
            obj.activate()
            MacUIUtils.make_focus(self.tf_password)
            MacUIUtils.input_text(self.tf_password, password)
            MacUIUtils.click_button(self.btn_continue)
        else:
            print("NO password window show")




if __name__ == "__main__":
    RestoreAuthWindow().enter_passoword('a')
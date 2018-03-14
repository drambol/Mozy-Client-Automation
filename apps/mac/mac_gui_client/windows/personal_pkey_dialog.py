#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from apps.mac.mac_lib.mozy_ui_element import MacMozyUIBase, Element


class Personal_Key_Dialog(MacMozyUIBase):
    """
    description:
    """

    parent_match = {'AXRole': 'AXWindow', 'AXTitle': "Save"}

    elements =[]
    elements.append(Element("btn_cancel", {'AXRole': 'AXButton', 'AXTitle': 'Cancel'}, parent_matcher=parent_match))

    def __init__(self):
        super(Personal_Key_Dialog, self).__init__()
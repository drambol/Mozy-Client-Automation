#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

from apps.mac.mac_lib.mozy_ui_element import MacMozyUIBase


class OptionTab(MacMozyUIBase):

    elements=[]

    def __init__(self):
        super(OptionTab, self).__init__()

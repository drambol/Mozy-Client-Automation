#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

import atomac

from apps.mac.mac_lib.mac_ui_util import MacUIUtils


class SystemPreference:

    @staticmethod
    def force_quit_system():
        test = atomac.launchAppByBundleId('com.apple.Preview')
        test



if __name__ == '__main__':
    SystemPreference.force_quit_system()
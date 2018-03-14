#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

from .mac_cmd import MacCmd


class UninstallCmd(MacCmd):

    def __init__(self):
        super(UninstallCmd, self).__init__()
        self.command = "uninstall"


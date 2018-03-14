#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

from .mac_cmd import MacCmd


class AuthCmd(MacCmd):

    def __init__(self):
        super(AuthCmd, self).__init__()
        self.command = "auth"
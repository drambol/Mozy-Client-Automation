#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from apps.mac.mac_cli_client.commands.mac_cmd import MacCmd


class ReadCmd(MacCmd):

    def __init__(self):
        super(ReadCmd, self).__init__()
        self.command = "read"

    def read(self, var):
        var = var.replace('_','.')
        result = self.exe_cmd(var)
        return result

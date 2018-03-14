#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from apps.mac.mac_cli_client.commands.mac_cmd import MacCmd


class WriteCmd(MacCmd):

    def __init__(self):
        super(WriteCmd, self).__init__()
        self.command = "write"

    def write_key_value(self, **param):
        # cmd = self.generate_str_from_kwargs(**param)
        # return self.exe_cmd(cmd)
        for (key, value) in param.items():
            self.write(key, value)

    def write(self, key, value):
        key = key.replace('_','.')
        cmd = "{key} {value}".format(key=key, value=value)
        result = self.exe_cmd(cmd)
        return result

#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

import re

from lib.cmdhelper import CmdHelper

class MacCmd(object):

    def __init__(self, brand=None):
        self.brand = brand or 'MozyProBackup'
        self.command = ''

    def exe_cmd(self, param=None):
        cmd = "{} {} ".format(self.brand, self.command)
        if param is not None:
            cmd = cmd + param

        return CmdHelper.run(cmd)


    @staticmethod
    def generate_str_from_kwargs(**kwargs):
        result = ""
        for (key,value) in kwargs.items():
            if key.find("_") >= 0:
                key = re.sub('_', ".", key)

            if value is not None:
                result += " {} {}".format(key, value)
            else:
                result += " {}".format(key)

        return result




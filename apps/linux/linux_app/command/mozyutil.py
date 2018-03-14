#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

import re

from lib.cmdhelper import CmdHelper
from lib.loghelper import LogHelper

class MozyutilCmd(object):

    _mozyutil = "mozyutil"
    _command_name = None

    @classmethod
    def exe_cmd(cls, param=None):
        cmd = "{} {}".format(cls._mozyutil, cls._command_name)
        if param is not None:
            cmd = cmd + param

	LogHelper.info("MozyUtil CMD: {cmd}".format(cmd=cmd))
        return CmdHelper.run(cmd)

    @staticmethod
    def generate_str_from_kwargs(**kwargs):
        result = ""
        for (key,value) in kwargs.items():
            if key.find("_") >= 0:
                key = re.sub('_', "-", key)

            if value is not None:
                result += " --{} {}".format(key, value)
            else:
                result += " --{}".format(key)

        return result





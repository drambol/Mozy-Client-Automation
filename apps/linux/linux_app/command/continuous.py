#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

import time

from apps.linux.linux_app.command.mozyutil import MozyutilCmd
from lib.cmdhelper import CmdHelper
from lib.singleton import Singleton


class ContinuousCmd(MozyutilCmd):

    __metaclass__ = Singleton
    CONTINUOUS = 1
    ON_DEMAND = 0

    _command_name = "continuous"

    @classmethod
    def set_continuous(cls):
        result = False
        cls.__run_continuous(cls.CONTINUOUS)
        time.sleep(1)
        if cls.get_mode() == cls.CONTINUOUS:
            result = True
        return result

    @classmethod
    def set_on_demand(cls):
        result = False
        cls.__run_continuous(cls.ON_DEMAND)
        if cls.get_mode() == cls.ON_DEMAND:
            result = True
        return result

    @classmethod
    def get_mode(cls):
        cmd = "{} {}".format(cls._mozyutil, cls._command_name)
        output = CmdHelper.run(cmd)
        result = None
        if output.lower().lstrip().rstrip() == 'on':
            result = cls.CONTINUOUS
        elif output.lower().lstrip().rstrip() == 'off':
            result = cls.ON_DEMAND

        return result

    @classmethod
    def __run_continuous(cls, mode):
        cmd = "{} {}".format(cls._mozyutil, cls._command_name)
        if mode == cls.CONTINUOUS:
            cmd += ' on'
        else:
            cmd += ' off'

        return CmdHelper.run(cmd)
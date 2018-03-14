#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

from apps.linux.linux_app.command.mozyutil import MozyutilCmd
from lib.singleton import Singleton


class ThrottleCmd(MozyutilCmd):

    __metaclass__ = Singleton
    _command_name = "throttle"

    def list_throttle(self):
        cmd = self.exe_cmd().lstrip().rstrip()
        return cmd

    def enable_throttle(self, bps=None, kps=None):
        if bps is not None:
            output = self.exe_cmd(self.generate_str_from_kwargs(op='enable', bps=bps))

        if kps is not None:
            output = self.exe_cmd(self.generate_str_from_kwargs(op='enable', kps=kps))

        return output

    def disable_throttle(self):
        output = self.exe_cmd(self.generate_str_from_kwargs(op='disable'))
        return output


    def is_throttle_on(self):
        output = self.list_throttle().lstrip().rstrip()

        if output.upper() == "Throttling is disabled".upper():
            result = False
        elif output.upper().find('PER SECOND') >= 0:
            result = True

        return result




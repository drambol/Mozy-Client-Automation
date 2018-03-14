#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from apps.linux.linux_app.command.mozyutil import MozyutilCmd
from lib.cmdhelper import CmdHelper
from lib.singleton import Singleton


class DecryptCmd(MozyutilCmd):
    __metaclass__ = Singleton
    _command_name = "decrypt"

    def decrypt(self, path=None, to=None, overwrite=True):
        kwargs = {

        }
        if path is not None:
            kwargs['from'] = path
        if to is not None:
            kwargs['to'] = to
        if overwrite is True:
            kwargs['overwrite'] = None

        cmd = self.generate_str_from_kwargs(**kwargs)
        output = self.exe_cmd(cmd)
        return output
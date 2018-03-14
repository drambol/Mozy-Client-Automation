#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

from apps.linux.linux_app.command.mozyutil import MozyutilCmd


class RemovebackupdirsCmd(MozyutilCmd):

    _command_name = "removebackupdirs"

    @classmethod
    def removebackupdirs(cls, path):
        cmd = cls.generate_str_from_kwargs(path=path)
        output = cls.exe_cmd(cmd)
        return output


#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

from apps.linux.linux_app.command.mozyutil import MozyutilCmd


class ClearbackupdirsCmd(MozyutilCmd):

    _command_name = "clearbackupdirs"

    @classmethod
    def clearbackupdirs(cls):
        output = cls.exe_cmd()
        return output
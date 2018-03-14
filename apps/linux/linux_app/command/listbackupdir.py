#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

from apps.linux.linux_app.command.mozyutil import MozyutilCmd


class ListBackupDirsCmd(MozyutilCmd):

    _command_name = "listbackupdirs"

    @classmethod
    def listbackupdirs(cls):
        dirs = []
        output = cls.exe_cmd()
        for dir in output.splitlines():
            if dir.startswith('/'):
                dirs.append(dir)
        return dirs

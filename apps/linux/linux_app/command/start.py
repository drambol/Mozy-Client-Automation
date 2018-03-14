#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from apps.linux.linux_app.command.mozyutil import MozyutilCmd


class StartCmd(MozyutilCmd):

    _command_name = "start"

    def start(self):
        return self.exe_cmd()


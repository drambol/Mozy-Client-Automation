#!/usr/bin/env python
#
# Copyright (c) Maginatics, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from apps.linux.linux_app.command.mozyutil import MozyutilCmd


class UnlinkCmd(MozyutilCmd):

    _command_name = "unlink"

    def unlink(self):
        return self.exe_cmd()


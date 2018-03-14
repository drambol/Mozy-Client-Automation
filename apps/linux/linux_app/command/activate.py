#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong



from apps.linux.linux_app.command.mozyutil import MozyutilCmd


class ActivateCmd(MozyutilCmd):

    _command_name = "activate"

    def activate(self, **kwargs):
        str = self.generate_str_from_kwargs(**kwargs)
        if str.find("--password") >=0 and str.find("--password-file") == -1:
            str = str.replace("--password", "--pass")
        output = self.exe_cmd(str)
        return output


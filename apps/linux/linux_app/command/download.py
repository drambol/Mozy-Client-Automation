#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from apps.linux.linux_app.command.mozyutil import MozyutilCmd


class DownloadCmd(MozyutilCmd):

    _command_name = "download"

    def download(self, **kwargs):
        str = self.generate_str_from_kwargs(**kwargs)
        output = self.exe_cmd(param=str)

        return output

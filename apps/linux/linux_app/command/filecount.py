#mozyutil filecount
#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

import re
from apps.linux.linux_app.command.mozyutil import MozyutilCmd


class FilecountCmd(MozyutilCmd):

    _command_name = "filecount"

    @classmethod
    def get_file_count(cls):
        output = cls.exe_cmd()
        retest = re.match(r"Number of files backed up: (\d+)", output)
        if retest:
            result = int(retest.groups()[0])
        else:
            result = None

        return result

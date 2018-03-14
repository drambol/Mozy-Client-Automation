#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


import re
from apps.linux.linux_app.command.mozyutil import MozyutilCmd



class LastBackupCmd(MozyutilCmd):
    _command_name = "lastbackup"

    '''
    root@ubuntu:~/Downloads/pycharm-2017.1.1/bin# mozyutil lastbackup --utc
Start Time: 16 May 2017 09:13:41 GMT
Completion Time: 16 May 2017 09:13:44 GMT
Result: SUCCESS
Last Successful Completion: 16 May 2017 09:13:44 GMT
    '''
    def parse_lastBackup(cls, **kwargs):
        result = {}
        cmd = cls.generate_str_from_kwargs(**kwargs)
        output = cls.exe_cmd(cmd)
        for line in output.splitlines():
            (key, value) = re.split(r':',line,1)
            key = key.lstrip().rstrip().lower().replace(' ','_')
            result[key] = value.lstrip().rstrip()
        return result

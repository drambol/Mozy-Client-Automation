#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

import re

from apps.linux.linux_app.command.mozyutil import MozyutilCmd
from lib.singleton import Singleton
from lib.loghelper import LogHelper


class HistoryCmd(MozyutilCmd):

    __metaclass__ = Singleton
    _command_name = "history"


    @classmethod
    def get_last_history(cls):
        param = {
         'limit': 1,
         'tabs': None
        }
        result = cls.get_history(**param)
        return result

    @classmethod
    def get_history(cls, **kwargs):
        cmd = cls.generate_str_from_kwargs(**kwargs)
        output = cls.exe_cmd(cmd)
        return output

    @classmethod
    def parse_history(cls, **kwargs):
        if not kwargs.get('tabs'):
            kwargs['tabs'] = None
        cmd = cls.generate_str_from_kwargs(**kwargs)
        output = cls.exe_cmd(cmd)
        result = HistoryResultObj.parse_history(output)
        return result

    @classmethod
    def get_continuous_mode_summary(cls):
        result = { }

        cli_output = cls.get_history(id=0)
        if cli_output=='': # No history available
            result = {
                'changes_processed': 0
            }
            return result
        for line in cli_output.splitlines():
            try:
                (key, value) = line.split(':')
                key = key.lstrip().rstrip().lower().replace(r' ', '_')
                value = value.lstrip().rstrip().lower()
                result[key] = value
            except ValueError as e:
                return result

        return result


class HistoryResultObj(object):

    def __init__(self,backup_id, start_time, end_time, backup_type, transfer_size, files_backuped, failures, result):
        self.backup_id =  backup_id or None
        self.start_time = start_time or None
        self.end_time= end_time or None
        self. backup_type = backup_type or None
        self. transfer_size =  transfer_size or None
        self.files_backuped =  files_backuped or None
        self.failures = failures or None
        self.result = result or None

    @classmethod
    def parse_history(cls, str, skip_continuous=True):
        result = []
        for line in str.splitlines():
            LogHelper.debug("process line %s" % line)
            if re.match("^\d", line):
                tokens = map(lambda x: x.lstrip().rstrip(), re.split(r'\t', line))
                try:
                     result.append(HistoryResultObj(tokens[0],tokens[1], tokens[2],tokens[3],tokens[4],tokens[5], tokens[6],tokens[7]))
                except:
                    raise Exception('Invalid history result, failed to parse')
            else:
                continue
        return result


if __name__ == '__main__':
    output = HistoryCmd.get_last_history()
    obj = HistoryResultObj.parse_history( output)
    print obj





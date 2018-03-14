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
from lib.filehelper import FileHelper
from apps.linux.linux_app.controller.lynx_controller import LynxCtrl


class BackupsetCmd(MozyutilCmd):

    _command_name = "backupset"

    def __init__(self):
        pass

    @classmethod
    def get_listallfiles_summary(cls, displaybytes=True):
        if displaybytes:
            cmd = cls.generate_str_from_kwargs(listallfiles=None, bytes=None)
        else:
            cmd = cls.generate_str_from_kwargs(listallfiles=None)
        output = cls.exe_cmd(cmd)
        lines = output.splitlines()
        summary_line = lines[-1]
        retest = re.match(r"Summary: (.*)", summary_line)
        if retest:
            result = retest.groups()[0]

        return result

    def refresh(self):
        output = self.exe_cmd(self.generate_str_from_kwargs(refresh=None))
        return output

    @staticmethod
    def is_file_included(path):
        pass

    @staticmethod
    def list_allfiles():
        cmd = BackupsetCmd.generate_str_from_kwargs(listallfiles=None)
        str_listfiles = BackupsetCmd.exe_cmd(cmd)
        result = []
        for line in str_listfiles.splitlines():
            if not re.match(r"Summary:", line):
                result.append(line)
        return result

    @staticmethod
    def dumpall():
        cmd = BackupsetCmd.generate_str_from_kwargs(dumpall=None)
        dump_str = BackupsetCmd.exe_cmd(cmd)
        return dump_str

    @staticmethod
    def clear_backup_set():
        BackupsetHelper.delete_json_file()


class BackupsetHelper(object):

    __metaclass__ = Singleton

    @staticmethod
    def delete_json_file(filename=None, conf_dir=None):
        if not conf_dir:
            conf_dir = LynxCtrl.conf_dir

        if not filename:
            filename = "*.json"

        files = FileHelper.find_file(conf_dir, filename)

        for file_to_delete in files:
            FileHelper.delete_file(file_to_delete)

        return files




if __name__ == "__main__":
    print    BackupsetCmd.list_allfiles()

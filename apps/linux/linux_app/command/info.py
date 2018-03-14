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


class InfoCmd(MozyutilCmd):
    """
    wrapper class for mozyutil info command
    """

    _command_name = "info"
    __metaclass__ = Singleton

    @staticmethod
    def get_info_str(**kwargs):
        cmd = InfoCmd.generate_str_from_kwargs(**kwargs)

        output = InfoCmd.exe_cmd(cmd)
        return output

    @staticmethod
    def get_info(path, version_table=True):
        if version_table:
            info_str = InfoCmd.get_info_str(path=path, version_table=None)
        else:
            info_str = InfoCmd.get_info_str(path=path)
        result = InfoResultParser().parse_info_from_str(info_str)
        return result

    @staticmethod
    def get_last_remote_info(path, version_table=True):
        return InfoCmd.get_remote_info_by_index(0, path, version_table)

    @staticmethod
    def get_remote_info_by_index(index, path, version_table=True):
        info_dict =InfoCmd.get_info(path, version_table)
        infos = info_dict.remote
        try:
            return infos[index]
        except Exception as e:
            return None

    @staticmethod
    def get_remote_infos(path, version_table=True):
        info_dict = InfoCmd.get_info(path, version_table)
        infos = info_dict.remote
        return infos

    @staticmethod
    def get_last_version(path, version_table=True):
        info = InfoCmd.get_last_remote_info(path, version_table)
        if info:
            return info.get('VERSION')
        else:
            return None


class InfoResultParser(object):

    def __init__(self):
        self.info_about = None
        self.local = {

        }
        self.remote = []

    def parse_info_from_str(self, str):
        re_info_about = re.compile("info about[ \t]+(.*)", re.IGNORECASE)
        re_local = re.compile(r"local file[ \t]+mtime:\s+(\d+)\s+size:\s+(.*)", re.IGNORECASE)
        re_remote = re.compile(r"(file|dir)[ \t]+[ \t]+(\w+)[ \t]+(\w+)[ \t]+(\w+)?[ \t]+(\w+)?[ \t]+\"(.*)\"",re.IGNORECASE)

        for line in str.splitlines():
            if len(line) == 0:
                continue
            info_about_test = re.match(re_info_about, line.lstrip())
            if info_about_test:
                info_about = info_about_test.groups(1)[-1]
                self.info_about = info_about
                continue

            local_test = re.match(re_local, line.lstrip())
            if local_test:
                mtime, size = local_test.groups()[-2], local_test.groups()[-1]
                self.local['MTIME'] = mtime
                self.local['SIZE'] = size
                continue

            if line.lower().find("file on server:") >=0:
                continue

            if line.lower().find("type") >= 0:
                continue

            remote_test = re.match(re_remote, line.lstrip())
            if remote_test:
                remote_dict = {}
                (REMOTE_TYPE, DELETE, VERSION, MTIME, SIZE, REMOTE_FROM) = remote_test.groups()
                remote_dict['REMOTE_TYPE'] = REMOTE_TYPE
                remote_dict['DELETE'] = DELETE
                remote_dict['VERSION'] = VERSION
                remote_dict['MTIME'] = MTIME
                remote_dict['SIZE'] = SIZE
                remote_dict['REMOTE_FROM'] = REMOTE_FROM
                self.remote.append(remote_dict)

        return self



if __name__ == '__main__':
    # output = InfoCmd.get_last_remote_info(path="/linux/backup/lin-484/lin_1.txt", version_table=True)
    # print output
    # # r = InfoCmd.get_last_version(path="/linux/backup/lin-532-1/lin-532_test_0.txt", version_table=True)
    # # print r

    str= """
    Info about	/linux/backup/lin-484/lin_1.txt
    Not found locally

    File on server:
    Type  	Delete	Version       	mtime     	Size          	From
    File  	Y     	1499316880    	          	              	"vagrant-ubuntu-trusty-64"
    File  	N     	1499316840    	1499316489	110B          	"vagrant-ubuntu-trusty-64"
    """
    result = InfoResultParser().parse_info_from_str(str)
    result



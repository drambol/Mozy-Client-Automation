#!/usr/bin/env python
#
# Copyright (c) Maginatics, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from subprocess import check_output, STDOUT, CalledProcessError, Popen, PIPE
from lib import singleton

class CmdHelper(object):

    __metaclass__ = singleton.Singleton

    @staticmethod
    def run(cmd, shell=True):
        try:
            result = check_output(cmd, shell=shell, stderr=STDOUT)

        except CalledProcessError as e:
            result = e.output
        return result

    @staticmethod
    def run_noblock(cmd):
        try:
            # result = Popen([cmd], stdout=PIPE)
            result = Popen(args=cmd, shell=True, stdout=PIPE, stderr=STDOUT)
            # Don't wait task finish
            returncode = result.communicate()
            print returncode
        except CalledProcessError as e:
            print e.output
        return returncode

    @staticmethod
    def runas_admin(cmd):
        #should only work for windows platform
        import win32com.shell.shell as shell
        try:
            result = shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c ' + cmd)
        except Exception as e:
            result = e.message
        return result

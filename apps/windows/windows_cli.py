#!/usr/bin/env python

import os
import time

import uuid

from lib.cmdhelper import CmdHelper
from lib.loghelper import LogHelper
from lib.singleton import Singleton
from configuration.global_config_loader import GLOBAL_CONFIG


class Windows_Cli(object):

    __metaclass__ = Singleton

    # TODO: Fetch from registry

    def __init__(self, oem="mozypro"):
        self.oem = oem

        self.install_path = "C:\\Program Files\\%s" %(oem)
        self.mozyutil = os.path.join(self.install_path, "%sutil.exe" % oem)


    # def activate(self, **kwargs):
    #     self._command_name = "activate"
    #     str = self.generate_str_from_kwargs(**kwargs)
    #     str = str.replace("--password", "--pass")
    #     output = self.exe_cmd(str)
    #     return output
    #
    # def backupset(self, **kwargs):
    #     self._command_name = "backupset"
    #
    #
    # def backup(self):
    #     pass

    # ('idle\r\n', None) ('backingup\r\n', None)
    # @staticmethod
    def current_state(self):
        cmd = '"' + self.mozyutil + '"' + " /currentstate 2>&1"

        # 'idle\r\n' | 'backingup\r\n'
        result = CmdHelper.run_noblock(cmd)
        # backingup | idle
        return result[0].strip('\n').strip('\r')

    # @staticmethod
    def create_backupset(self, targetFolder, backupsetname="automation", extension="NoExtension"):
        # Generate a backup set file based on a template
        LogHelper.info("Generating template file")
        backupset_file = os.path.join(os.getcwd(), "..", extension)

        guid = Windows_Cli.get_Guid()
        with open(backupset_file, 'w') as f:
            f.write("SET\n")
            f.write("name: %s\n" % backupsetname)
            f.write("guid: %s\n" % guid)
            f.write("selected: 1\n")
            f.write("excluded: 0\n")
            f.write("lock_rules: 0\n")
            f.write("lock_selection: 0\n")
            f.write("\n")
            f.write("PATHS\n")
            f.write("include: %s\n" % targetFolder)
            f.write("\n")

            if not (extension == "NoExtension"):
                f.write("RULES\n")
                f.write("extension \"%s\"\n" % extension)
                f.write("\n")

        LogHelper.info("Create backupset")
        cmd = '"' + self.mozyutil + '"' + " /addbackupset " + backupset_file
        print cmd
        result = CmdHelper.run(cmd)
        LogHelper.info("Create backupset %s successfully." % backupset_file)
        return result

    # @staticmethod
    def dump_backupset(self, backupsetname="smoke"):
        """
        SET
        name: test
        guid: 9d2dba17-b406-4557-ba8f-0327bfed61c3
        selected: 1
        excluded: 0
        lock_rules: 0
        lock_selection: 0

        PATHS
        include: C:\win_log

        RULES
        extension "log" "txt"
        :return: backupset schema
        """

        cmd = '"' + self.mozyutil + '"' + " /dumpbackupset " + backupsetname
        print cmd
        result = CmdHelper.run(cmd)
        LogHelper.info("Dump backupset %s." % result)
        return result

    # @staticmethod
    def remove_backupset(self, backupsetname="smoke"):
        cmd = '"' + self.mozyutil + '"' + " /rmbackupset " + backupsetname
        print cmd
        result = CmdHelper.run(cmd)
        LogHelper.info("Remove backupset %s." % result)
        return result

    # @staticmethod
    def start_backup(self):
        cmd = '"' + self.mozyutil + '"' + " /backup"
        print cmd
        result = CmdHelper.run(cmd)
        LogHelper.info("Starting Backup via CLI")
        return result

    # @staticmethod
    def cancel_backup(self):
        cmd = '"' + self.mozyutil + '"' + " /cancel"
        print cmd
        result = CmdHelper.run(cmd)
        LogHelper.info("Cancel Backup via CLI")
        return result

    # @staticmethod
    def activate_keyless(self, email, password, encryption_type="customkeytext", key=""):
        cmd = '"' + self.mozyutil + '"' + " /keylessactivate /email " + email + " /pass " + password + " /customkeytext " + key

        print cmd
        result = CmdHelper.run(cmd)

        if "Error" in result:
            LogHelper.error("Activation Failed with an Error: %s" % result)
            return False
        else:
            return True

    def activate_productkey(self, email, password, productkey):
        cmd = '"' + self.mozyutil + '"' + " /activate " + email + " " + password + " /productkey " + productkey
        print cmd
        result = CmdHelper.run(cmd)

        if "Error" in result:
            LogHelper.error("Activation Failed with an Error: %s" % result)
            return False
        else:
            return True

    def activate_auto(self, username):
        cmd = '"' + self.mozyutil + '"' + " /autoactivate " + username
        print cmd
        result = CmdHelper.run(cmd)

        if "Error" in result:
            LogHelper.error("Activation Failed with an Error: %s" % result)
            return False
        else:
            return True

    # @staticmethod
    def wait_for_state(self, state, timeout=None, granularity=None):
        """
        :param state:
        :param timeout:
        :param granularity:
        :return:
        """
        result = True

        if timeout is None:
            timeout = GLOBAL_CONFIG["TIMEOUT"]
        if granularity is None:
            granularity = GLOBAL_CONFIG["GRANULARITY"]

        expected_state = []

        if type(state) == str:
            expected_state.append(state.upper())
        else:
            expected_state = state

        print "Expected state: %s" % expected_state
        current = self.current_state()
        elapsed = 0
        while (current.upper() not in expected_state) and elapsed <= timeout:
            time.sleep(granularity)
            elapsed += granularity
            current = self.current_state()
        if elapsed > timeout or current.upper() not in expected_state:
            result = False

        return result

    @staticmethod
    def get_Guid():
        guid = uuid.uuid4()
        return guid

## End of Windows_Cli

if __name__ == '__main__':
    # windows_cli = Windows_Cli("MozyEnterprise")
    windows_cli = Windows_Cli("mozypro")
    windows_cli.create_backupset("c:\win_log3", "log")
    print windows_cli.current_state()

    if windows_cli.current_state() == "backingup":
        windows_cli.cancel_backup()
        windows_cli.wait_for_state("IDLE")

    elif windows_cli.current_state() == "idle":
        print "CLI start backup."
        windows_cli.start_backup()
        # print windows_cli.current_state()
        windows_cli.wait_for_state("BACKINGUP")
        print "Backup started."
        windows_cli.wait_for_state("IDLE")
        print "Backup finished."

    else:
        print windows_cli.current_state()
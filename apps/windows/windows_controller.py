#!/usr/bin/env python

import os
import re
import time

from lib.cmdhelper import CmdHelper
from lib.filehelper import FileHelper
from lib.loghelper import LogHelper
from lib.singleton import Singleton
from configuration.global_config_loader import GLOBAL_CONFIG
from lib.platformhelper import PlatformHelper
from lib.sqlitehelper import SqliteHelper
from apps.windows.win_lib.win_configuration import ConfigurationSetting
if PlatformHelper.is_win():
    from apps.qa_environment import QA_Environment

class Windows_Controller(object):

    __metaclass__ = Singleton

    # TODO: Fetch from registry
    # oem = "mozypro"
    # mozyutil_name = "mozyproutil"
    # service_name = "mozyprobackup"
    # install_path = "C:\\Program Files\\MozyPro"
    # config_dir = os.path.join(install_path, "Config")
    # data_dir = os.path.join(install_path, "data")
    # mozy_daemon = os.path.join(install_path, "mozyprobackup.exe")
    # mozyutil = os.path.join(install_path, "mozyproutil.exe")
    # configapp = os.path.join(install_path, "mozyproconf.exe")
    # statusapp = os.path.join(install_path, "mozyprostat.exe")
    # config_database = os.path.join(config_dir, "conf.dat")
    # manifest_database = os.path.join(data_dir, "manifest.dat")
    # state_database = os.path.join(data_dir, "state.dat")

    def __init__(self, oem="mozypro"):
        print oem

        self.oem = oem

        self.mozyutil_name = "%sutil" %(oem)
        self.service_name = "%sbackup" %(oem)
        self.install_path = "C:\\Program Files\\%s" % oem
        self.mozy_daemon = os.path.join(self.install_path, "%sbackup.exe" % oem)
        self.mozyutil = os.path.join(self.install_path, "%sutil.exe" % oem)
        self.configapp = os.path.join(self.install_path, "%sconf.exe" % oem)
        self.statusapp = os.path.join(self.install_path, "%sstat.exe" % oem)
        self.config_dir = os.path.join(self.install_path, "Config")
        self.data_dir = os.path.join(self.install_path, "data")
        self.log = os.path.join(self.data_dir, "%s.log" % oem)
        self.config_database = os.path.join(self.config_dir, "conf.dat")
        self.manifest_database = os.path.join(self.data_dir, "manifest.dat")
        self. state_database = os.path.join(self.data_dir, "state.dat")


    def is_client_running(self):
        """
        usage: check whether windows client is running
        :return: True if ruuning || False if not running
        """
        running = False

        status = Windows_Controller.get_service_status(servicename=self.service_name)

        if status == "RUNNING":
            running = True
        return running

    def is_activated(self):
        activate_status = QA_Environment(self.oem)
        if activate_status.set_env.read_configure_status() == 1:
            return True
        else:
            return False

    @staticmethod
    def get_service_status(servicename = "mozyprobackup"):
        servicestatus_cmd = "sc query %s" %servicename
        print servicestatus_cmd
        status = CmdHelper.run(servicestatus_cmd)

        if not status:
            return status
        else:
            match = re.search(r"(RUNNING|STOPPED|START_PENDING|STOP_PENDING)", status, re.IGNORECASE)

            if not match:
                return match
            else:
                return match.group(1)


    def is_client_installed(self):
        """
        usage: check whether windows client is installed
        :return: True if installed || False if not installed
        """
        result = False
        if FileHelper.dir_exist(self.install_path) and FileHelper.file_exist(self.mozyutil) and FileHelper.file_exist(self.configapp) and FileHelper.file_exist(self.statusapp):
            result = True
        else:
            LogHelper.error("ERROR: %s is installed." % self.install_path)

        return result

    # @staticmethod
    def start(self):
        """
        usage: start
        :return:
        """
        cmd_output = "error: could not determine how to start the service"
        if FileHelper.file_exist(self.mozy_daemon):
                cmd_output = self.start_upstart()
        return cmd_output


    # @staticmethod
    def start_upstart(self):
        cmd = "sc start %s" % self.service_name
        cmd_output = CmdHelper.run(cmd)
        return cmd_output

    # @staticmethod
    def stop(self):
        cmd_output = "error: could not determine how to stop the service"
        if FileHelper.file_exist(self.mozy_daemon):
                cmd_output = self.stop_upstart()
        return cmd_output

    # @staticmethod
    def stop_upstart(self):
        cmd = "sc stop %s" % self.service_name
        cmd_output = CmdHelper.run(cmd)
        return cmd_output


    # @staticmethod
    def restart(self):
        # cmd_output = "error: could not determine how to restart the service"
        # if FileHelper.file_exist(Windows_Controller.mozy_daemon):
        #     cmd_output = Windows_Controller.restart_upstart()
        # return cmd_output
        self.stop()
        self.start()

    # @staticmethod
    def restart_upstart(self):
        cmd = "sc restart %s" % self.service_name
        cmd_output = CmdHelper.run(cmd)
        return cmd_output

    @staticmethod
    def disable_uac():
        cmd = "REG ADD HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 0 /f"
        CmdHelper.run(cmd)

        cmd = "REG ADD HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 0 /f"
        CmdHelper.run(cmd)
        print "Disable UAC"

    def prepare_environment(self, env):
        qa_set = QA_Environment(self.oem)
        qa_set.set_qa_environment(env)

    def set_unconfigured_status(self):
        unconfigure = QA_Environment(self.oem)
        unconfigure.set_env.set_unconfigured()
        # self.stop_upstart()
        # self.kill_process("status")
        # self.kill_process("config")
        # self.start_upstart()

    def reset_reg(self, env):
        reset_setting = QA_Environment(self.oem)
        reset_setting.reset_qa_reg(env)

    def restart_services(self, force=False):
        self.kill_process("status")
        self.kill_process("config")
        if force:
            self.stop_upstart()
            self.start_upstart()

    def kill_process(self, process_name):
        if process_name == "status":
            processname = self.statusapp
        elif process_name == "config":
            processname = self.configapp
        close_cmd = 'taskkill /F /IM %s' % (processname)
        print close_cmd
        CmdHelper.run(close_cmd)

    def wipe_configuration(self):
        ConfigurationSetting(self.oem).clean_configuration()

    @staticmethod
    def wait_for_service_ready(service_name = "mozyprobackup", timeout=None, elapsed=0):
        result = False
        if not timeout:
            timeout = GLOBAL_CONFIG['TIMEOUT']

        sleep_time = GLOBAL_CONFIG.get('GRANULARITY')
        status = Windows_Controller.get_service_status(servicename = service_name)

        if status.upper() == "RUNNING":
            result = True

        while result is not True and elapsed <= timeout:

            elapsed += sleep_time
            time.sleep(sleep_time)

            status = Windows_Controller.get_service_status(servicename = service_name)

            if status.upper() == "RUNNING":
                result = True

        return result


    # @staticmethod
    # Get current client version
    def get_client_version(self):
        # 2.32.4.532
        # TBD
        result = SqliteHelper.find_machine_id(self.manifest_database)
        return result

    # Get current machine_id/container_id from DataBase
    def get_machine_id(self):
        result = SqliteHelper.find_machine_id(self.manifest_database)
        return result

    # WARNING: This will delete the conf.dat and state.dat. Be careful.
    def clear_config(self):
        if FileHelper.file_exist(self.config_database):
            FileHelper.delete_file(self.config_database)
        if FileHelper.file_exist(self.state_database):
            FileHelper.delete_file(self.state_database)

    def search_result_in_history(self):
        result = ConfigurationSetting(self.oem).search_result()
        return result

## End of Windows_Controller

if __name__ == '__main__':
    """
    Note: We need to run as Administrator
    """
    # windowsctl = Windows_Controller()
    # print windowsctl.mozyutil    # mozyproutil
    # print Windows_Controller.mozyutil    # mozyproutil
    # print windowsctl.service_name    # mozyprobackup
    # print Windows_Controller.service_name    # mozyprobackup
    # print Windows_Controller.is_client_installed()

    # windowsctl = Windows_Controller("MozyEnterprise")
    windowsctl = Windows_Controller("mozypro")
    print windowsctl.get_machine_id()

    windowsctl.disable_uac()
    print windowsctl.mozyutil_name    # MozyEnterpriseutil
    print windowsctl.service_name    # MozyEnterprisebackup

    print windowsctl.install_path

    print windowsctl.mozy_daemon
    print windowsctl.mozyutil

    print windowsctl.configapp
    print windowsctl.statusapp

    print windowsctl.is_client_installed()
    print windowsctl.is_client_running()
    # if windowsctl.is_client_running():
    #     print "Stop service"
    #     Windows_Controller.wait_for_service_ready(service_name = windowsctl.service_name)
    #     windowsctl.stop()
    #
    #     print windowsctl.is_client_running()  # STOPPED
    #
    # else:
    #     print windowsctl.start()
    #     print "Start service"
    #     Windows_Controller.wait_for_service_ready(service_name = windowsctl.service_name)
    #     print windowsctl.is_client_running()  # START
    #
    # print "Re-Start service"
    # print windowsctl.restart()             # Re-START
    # Windows_Controller.wait_for_service_ready(service_name = windowsctl.service_name)
    # print windowsctl.is_client_running()

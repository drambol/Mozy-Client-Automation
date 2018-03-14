#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong



import os
import time


from lib.cmdhelper import CmdHelper
from lib.singleton import Singleton
from lib.filehelper import FileHelper
from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.linux.lynx_config_loader import LYNX_CONFIG


class LynxCtrl(object):

    __metaclass__ = Singleton

    mozyutil = "mozyutil"
    mozyutil_daemon_path = "/usr/sbin/mozy-daemon"
    conf_filename = "/etc/mozybackup.conf"
    conf_dir = "/etc/mozybackup.conf.d"
    service_path_upstart = "/etc/init/mozybackup.conf"
    service_path_initd = "/etc/init.d/mozybackup"
    config_db_dir = "/var/lib/mozybackup/"
    log = "/var/log/mozy.log"
    config_database = "config.dat"
    state_database = "state.dat"
    metrics_database = "metrics.dat"

    @staticmethod
    def is_client_running():
        """
        usage: check whether linux cient is running
        :return: True if ruuning || False if not running
        """
        result = False
        cmd = "ps aux | grep mozy | grep -v grep"
        cmd_output = CmdHelper.run(cmd)

        for line in cmd_output.split(os.linesep):
            if line.find("mozy-daemon") >= 0:
                result = True

        return result

    @staticmethod
    def is_client_installed():
        """
        usage: check whether linux client is installed
        :return: True if installed || False if not installed
        """
        result = False
        if FileHelper.file_exist(LynxCtrl.service_path_upstart)  or FileHelper.file_exist(LynxCtrl.service_path_initd):
            if FileHelper.dir_exist(LynxCtrl.conf_dir):
                if FileHelper.file_exist(LynxCtrl.mozyutil_daemon_path):
                    result = True
                else :
                     print  "%s not present" %LynxCtrl.mozyutil_daemon_path
            else:
                print "%s not present" % LynxCtrl.conf_dir
        else:
            print "service control script not present at %s or %s" % (LynxCtrl.service_path_initd,LynxCtrl.service_path_upstart)

        return result

    @staticmethod
    def start():
        """
        usage: start
        :return:
        """
        cmd_output = "error: could not determine how to start the daemon"
        if FileHelper.file_exist(LynxCtrl.service_path_upstart):
                cmd_output = LynxCtrl.start_upstart()
        elif FileHelper.file_exist(LynxCtrl.service_path_initd):
                cmd_output = LynxCtrl.start_initd()
        return cmd_output


    @staticmethod
    def start_initd():
        cmd = "%s start" % LynxCtrl.service_path_initd
        cmd_output = CmdHelper.run(cmd)

        return  cmd_output


    @staticmethod
    def start_upstart():
        cmd = "service mozybackup start"
        cmd_output = CmdHelper.run(cmd)
        return cmd_output

    @staticmethod
    def stop():
        cmd_output = "error: could not determine how to restart the daemon"

        if FileHelper.file_exist(LynxCtrl.service_path_upstart):
            cmd_output = LynxCtrl.stop_upstart()
        elif FileHelper.file_exist(LynxCtrl.service_path_initd):
            cmd_output = LynxCtrl.stopinitd()

        return cmd_output

    @staticmethod
    def stop_upstart():
        cmd = "service mozybackup stop"
        cmd_output = CmdHelper.run(cmd)

        return cmd_output

    @staticmethod
    def stop_initd():
        cmd = "%s stop" % LynxCtrl.service_path_initd
        cmd_output = CmdHelper.run(cmd)

        return cmd_output


    @staticmethod
    def restart():
        cmd_output = "error: could not determine how to restart the daemon"

        if FileHelper.file_exist(LynxCtrl.service_path_upstart):
            cmd_output = LynxCtrl.restart_upstart()
        elif  FileHelper.file_exist(LynxCtrl.service_path_initd):
            cmd_output = LynxCtrl.restart_initd()
        return cmd_output

    @staticmethod
    def restart_upstart():
        cmd = "service mozybackup restart"
        cmd_output = CmdHelper.run(cmd)

        return cmd_output


    @staticmethod
    def restart_initd():
        cmd = "%s restart" % LynxCtrl.service_path_initd
        cmd_output = CmdHelper.run(cmd)

        return cmd_output



    @staticmethod
    def get_client_version():
        cmd = "%s --version" % LynxCtrl.mozyutil_daemon_path
        output = CmdHelper().run(cmd)
        return output



    @staticmethod
    def set_qa_environment(env):
        if env.upper() in GLOBAL_CONFIG["QA_ENVIRONMENT"].keys() :
           env_hash = GLOBAL_CONFIG["QA_ENVIRONMENT"][env.upper()]
        else:
            raise KeyError("unsupport environment")
        env_dict = {}
        for (key, value) in env_hash.items():
            if key.upper().startswith('MOZY') or key.upper().startswith('SSL'):
                env_dict[key] = value

        LynxCtrl.apply_conf(env_hash, "environment.conf", False)



    @staticmethod
    def add_conf(key, value, conf_file="qa_automation.conf", keep_old_conf_file = True):
        if not conf_file.endswith(".conf"):
            conf_file += ".conf"

        conf_file_path = os.path.join(LynxCtrl.conf_dir, conf_file)

        if not keep_old_conf_file:
            FileHelper.delete_file(conf_file_path)

        line = "%s = %s\n" % (key, value)

        with open(conf_file_path, 'aw') as f:
            f.write(line)



    @staticmethod
    def apply_conf(dict, conf_file="qa_automation.conf", keep_old_conf_file = True):

        if not conf_file.endswith(".conf"):
            conf_file += ".conf"

        conf_file_path = os.path.join(LynxCtrl.conf_dir, conf_file)

        if not keep_old_conf_file:
            FileHelper.delete_file(conf_file_path)

        for (key, value) in dict.items():
            LynxCtrl.add_conf(key, value, conf_file, True)

        LynxCtrl.restart()

    @staticmethod
    def wait_for_sock_ready(timeout=None, elapsed=0):
        result = False
        if not timeout:
            timeout = GLOBAL_CONFIG['TIMEOUT']

        sleep_time = GLOBAL_CONFIG.get('GRANULARITY')
        cmd = "netstat -an|grep mozy.sock"
        cmd_output = CmdHelper.run(cmd)
    
        if cmd_output.find('mozy.sock') >=0:
            result = True

        while result is not True and elapsed <= timeout:

            elapsed += sleep_time
            time.sleep(sleep_time)
            cmd_output = CmdHelper.run(cmd)

            if cmd_output.find('mozy.sock') >= 0:
                result = True

        return result

    #add custom config
    @staticmethod
    def add_custom_config():
        """
        add custom config
        :return:
        """
        config = LYNX_CONFIG.get('CUSTOMIZED_CONFIG')
        LynxCtrl.apply_conf(config, "custom_config.conf", False)

    @staticmethod
    def prepare_environment(env):
        LynxCtrl.add_custom_config()
        LynxCtrl.set_qa_environment(env)

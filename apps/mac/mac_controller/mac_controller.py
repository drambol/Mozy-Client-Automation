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
from lib.filehelper import FileHelper
from apps.mac.mac_cli_client.mac_cli_client import MacCliClient

from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.mac.mac_config_loader import MAC_CONFIG


class MacController:

    def __init__(self, codename=None):

        self.codename = codename or 'MozyProBackup'
        self.app_support_dir = "/Library/Application Support/MozyPro/"
        self.cache_dir = '/Library/Caches/MozyPro/'
        self.state_db = 'state.db'
        self.state_dump ='state.dump'
        self.history_db = 'history.db'
        self.network_db = 'network.db'
        self.backup_pid = 'backup.pid'
        self.bulletin_db ='bulletin.db'
        self.cache_db = 'cache.db'
        self.spbundleid = 'com.apple.systempreferences'
        self.restorebundleid = 'com.mozypro.restore'

    def prepare_environment(self, env):
        self.setup_qa_env(env)

    @staticmethod
    def setup_qa_env(env):
        if env.startswith('STD1') or env.startswith('PROD'):
            return

        env_dict = GLOBAL_CONFIG['QA_ENVIRONMENT'].get(env)
        if env_dict is not None:
            bushost = env_dict.get('mozy.bushost')
            authhost = env_dict.get('mozy.authhost')
            tritonhost = env_dict.get('mozy.tritonhost')

        if env.startswith("QA") and (not tritonhost.startswith("http://")):
            tritonhost = "http://" + tritonhost

        MacCliClient.write_cmd.write('bus_url', bushost)
        MacCliClient.write_cmd.write('oauth_host', authhost)
        MacCliClient.write_cmd.write('triton_url', tritonhost)

        MacController.kill_system_preference()

    @staticmethod
    def normalize_brand_name(brand):
        normalized_brand = ''
        str_brand = brand.lower()
        if str_brand.find('pro') != -1:
            normalized_brand = 'MozyPro'
        elif str_brand.find('ent') != -1:
            normalized_brand = 'Mozy Enterprise'
        elif str_brand.find('home') != -1:
            normalized_brand = 'MozyHome'
        elif str_brand.find('next') != -1:
            normalized_brand = 'MozyNext'
        else:
            normalized_brand = 'unknown brand'

        return normalized_brand

    @staticmethod
    def check_process_by_name(name):
        result = False

        pid = CmdHelper.run('ps aux | grep "{name}" | grep -v grep'.format(name=name))
        if pid:
            result = True

        return result

    @staticmethod
    def prefix_for_sudo():
        password = MAC_CONFIG.get("LOCAL_ADMIN_PASSWORD")
        prefix = 'echo "{password}" | '.format(password=password)
        return prefix

    @staticmethod
    def kill_system_preference():
        CmdHelper.run('killall "System Preferences"')

    def is_client_running(self):
        cmd = 'lsappinfo find bundleID={bundleId}'.format(bundleId=self.bundleid)
        output = CmdHelper.run(cmd)
        if output.find('ASN')>=0:
            result = True
        else:
            result = False
        return result

    @staticmethod
    def quit_system_preferences():
        cmd = "osascript -e \'quit app \"System Preferences\"\'"
        output = CmdHelper.run(cmd)

        return output

    def is_installed(self):
        return self.get_version() != 0

    def get_version(self):
        cmd = '{codename} --version'.format(codename=self.codename)
        output = CmdHelper.run(cmd)

        if output.find('command not found') >= 0:
            version = 0  # not installed
        else:
            version = output.split('.')[-1]

        time.sleep(5)
        return int(version)

    @staticmethod
    def restart_mozypro_pid():
        result = False
        cmd_ps = 'ps aux | grep MozyProBackup | grep -v grep'
        pid_before = CmdHelper.run(cmd_ps)
        if pid_before:
            pid_before_int = int(pid_before.split()[1])
        else:
            return result

        cmd = MacController.prefix_for_sudo() + 'sudo -S killall MozyProBackup'
        CmdHelper.run(cmd)

        cmd = 'killall "MozyPro Status"'
        CmdHelper.run(cmd)

        cmd = 'killall "MozyPro Restore"'
        CmdHelper.run(cmd)

        pid_after = CmdHelper.run(cmd_ps)
        w_time = 120
        sleep_time = 2
        while not pid_after and w_time > 0:
            time.sleep(sleep_time)
            pid_after = CmdHelper.run(cmd_ps)
            w_time -= sleep_time
        pid_after_int = int(pid_after.split()[1])

        w_time = 120
        while w_time > 0 and pid_after_int == pid_before_int:
            time.sleep(sleep_time)
            pid_after = CmdHelper.run(cmd_ps)
            w_time -= sleep_time
            if pid_after:
                pid_after_int = int(pid_after.split()[1])

        if pid_after_int != pid_before_int:
            result = True

        return result

    def __remove_db(self, db_name):
        file_full_path = os.path.join(self.app_support_dir, db_name)
        FileHelper.delete_file(file_full_path)

    def clean_db(self, state=True, history=True, network=True, bulletin_db=True):
        if state:
            self.__remove_db(self.state_db)
            self.__remove_db('state.dump')
        if history:
            self.__remove_db(self.history_db)
            self.__remove_db('history.dump')
        if network:
            self.__remove_db(self.network_db)
            self.__remove_db('network.dump')
        if bulletin_db:
            self.__remove_db(self.bulletin_db)
            self.__remove_db('bulletin.dump')

    def clean_all(self):
        entities = FileHelper.find_file(self.app_support_dir, '*')
        for entry in entities:
            if entry.find('backup.pid') >= 0:
                continue
            if entry.find('restore') >= 0 :
                continue
            if entry.find('network') >=0 :
                continue

            cmd = MacController.prefix_for_sudo() + 'sudo -S rm -rf "%s"' %entry
            CmdHelper.run(cmd)

        # cache_db_path = os.path.join(self.cache_dir, self.cache_db)
        # cmd = "sudo rm -rf '{path}'".format(path=cache_db_path)
        # CmdHelper.run(cmd)

        self.restart_mozypro_pid()

    def get_current_app_status(self):
        valid_status = ('NOT INSTLLAED', 'INSTLLAED')

    def start_mac_mozy(self):
        """
            launch app
            :return:
            """
        import atomac
        from apps.mac.mac_lib.mac_ui_util import MacUIUtils
        bundleId = MacController().spbundleid
        WindowName = 'MozyPro'
        try:
            atomac.launchAppByBundleId(bundleId)
        except RuntimeError as e:
            print e.message

        app = atomac.getAppRefByBundleId(bundleId)
        app.activate()

        window = MacUIUtils.wait_element(app, AXRole='AXWindow')
        btn_showall = MacUIUtils.wait_element(window, AXRole='AXButton', AXTitle='Show All')
        MacUIUtils.click_button(btn_showall)

        title = window.AXTitle
        if title == 'MozyPro':  # it is already mozy window
            mozy_window = window
        elif title == "System Preferences":
            btn_mozypro = MacUIUtils.wait_element(app, AXRole='AXButton', AXTitle=WindowName)
            btn_mozypro.Press()
            mozy_window = MacUIUtils.wait_element(app, AXRole='AXWindow', AXTitle=WindowName)

        return mozy_window


if __name__ == "__main__":
    MacController().clean_all()
    # prefix = MacController.prefix_for_sudo()
    # cmd = prefix + 'sudo -S killall MozyProBackup'
    # print cmd
    # CmdHelper.run(cmd)

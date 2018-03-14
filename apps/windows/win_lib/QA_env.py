import re
import os

from lib.platformhelper import PlatformHelper
from apps.windows.windows_cli import Windows_Cli
from lib.registryhelper import RegistryHelper
from lib.filehelper import FileHelper
from lib.hostshelper import HostsHelper
from configuration.windows.windows_config_loader import WIN_CONFIG
if PlatformHelper.is_win():
    from _winreg import HKEY_LOCAL_MACHINE, REG_DWORD, REG_SZ

class WindowsQAEnv(object):

    def __init__(self, oem):
        self.oem = oem
        if oem == "MozyEnterprise":
            self.path = r"SOFTWARE\MozyEnterprise"
        if oem == "mozypro":
            self.path = r"SOFTWARE\mozypro"
        if oem == "MozyHome":
            self.path = r"SOFTWARE\mozy"


    def set_environment(self, key, value):
        path = "\options"
        str = "ssl"
        res = re.search(str, key)
        if res is not None:
            self.insert_dword_value(path, key, value)
        else:
            self.insert_sz_value(path, key, value)


    def insert_table(self, dict, path):
        path = self.path + path
        print "%s" % (path)
        for key, value in dict.items():
            subs = "ssl"
            res = re.search(subs, key)
            registry = RegistryHelper()
            type = REG_SZ
            if res is not None:
                type = REG_DWORD
            registry.set_reg_value(HKEY_LOCAL_MACHINE, path, key, value, type)


    def insert_sz_value(self, path, key, value):
        path = self.path + path
        registry = RegistryHelper()
        registry.set_reg_value(HKEY_LOCAL_MACHINE, path, key, value, REG_SZ)

    def insert_dword_value(self, path, key, value):
        path = self.path + path
        registry = RegistryHelper()
        registry.set_reg_value(HKEY_LOCAL_MACHINE, path, key, value, REG_DWORD)

    def set_autoactivate_env(self, key, value):
        path = ""
        self.insert_sz_value(path, key, value)

    def set_assistedactivate_env(self, key, value):
        path1 = ""
        path2 = "\options"
        sub = "preferredactivationtype"
        if key == sub:
            self.insert_dword_value(path2, key, value)
        else:
            self.insert_sz_value(path1, key, value)

    def set_fedid_env(self, env):
        path = r'C:\WINDOWS\system32\drivers\etc'
        fedid_setting = HostsHelper(self.oem, path)
        fedid_setting.duplicate_hostfile()
        fedid_setting.add_hosts_to_file(env)
        self.set_fedid_ahost(env)


    def set_fedid_ahost(self, env):
        subkey = "ahost"
        host_reg = WIN_CONFIG["QA_ENVIRONMENT"][env.upper()]["fedid"]["ahost"]
        self.set_keyed_reg(subkey, host_reg)

    def clean_fedid_setting(self):
        self.reset_fedid_reg()
        self.reset_hosts_file()

    def reset_hosts_file(self):
        path = r'C:\WINDOWS\system32\drivers\etc'
        fedid_setting = HostsHelper(self.oem, path)
        if fedid_setting.remove_hostfile():
            fedid_setting.recover_hostfile()

    def reset_fedid_reg(self):
        path = "\state"
        key = "subdomain"
        value = RegistryHelper.get_reg_value(HKEY_LOCAL_MACHINE, self.path+path, key)
        if value is not None:
            self.insert_sz_value(path, key, "")
        else:
            print "The key is not exist."

    def set_keyed_reg(self, key, value):
        if key:
            self.change_host(key, value, fedid=True)
        else:
            print "No host needs to be changed."

    def change_host(self, key, value, fedid=True):
        if fedid:
            path = r"SOFTWARE" + "\\" + self.oem + "\options"
            RegistryHelper.set_reg_value(HKEY_LOCAL_MACHINE, path, key, value, REG_SZ)

    def clear_reg(self, subkey):
        path = self.path
        print path
        registry = RegistryHelper()
        registry.delete_key(HKEY_LOCAL_MACHINE, path, subkey)


    def set_unconfigured(self):
        path = self.path + "\state"
        key = "configured"
        RegistryHelper.set_reg_value(HKEY_LOCAL_MACHINE, path, key, 0, REG_DWORD)
        self.reset_fedid_reg()


    def clean_file(self):
        src = WIN_CONFIG["TESTDATA_PATH"]
        cli = Windows_Cli(self.oem)
        if os.path.isdir(src):
            if len(os.listdir(src)) == 0:
                cli.create_backupset(src)
            else:
                fi = FileHelper()
                fi.clean_dir(src)
                os.mkdir(src)
                cli.create_backupset(src)
        else:
            os.mkdir(src)
            cli.create_backupset(src)

    def read_configure_status(self):
        path = self.path + "\state"
        key = "configured"
        value = RegistryHelper.get_reg_value(HKEY_LOCAL_MACHINE, path, key)
        return value


if __name__ == '__main__':
    # WindowsQAEnv("MozyEnterprise").set_unconfigured_status()
    WindowsQAEnv("mozypro").set_assistedactivate_env("qa12")
    # WindowsQAEnv("mozypro").close_stat()
#!/usr/bin/env python
import os

import sys
import re

from lib.platformhelper import PlatformHelper
if PlatformHelper.is_win():
    import win32api
    import win32con
    from _winreg import ConnectRegistry, CreateKey, OpenKey, DeleteKey, SetValueEx, QueryValueEx, CloseKey, HKEY_LOCAL_MACHINE, KEY_READ, KEY_WRITE, REG_SZ, REG_DWORD

from lib.cmdhelper import CmdHelper
from lib.loghelper import LogHelper

class RegistryHelper(object):
    # def __init__(self):
    #     self.path = path


    @staticmethod
    def set_reg_value(hkey, subkey, name, value, type):
        result = False
        registry_key = RegistryHelper.get_key(hkey, subkey, KEY_WRITE, True)
        if registry_key:
            try:
                if PlatformHelper.is_64bit_machine():
                    win32api.RegSetValueEx(registry_key, name, 0, type, value)
                    result = True
                else:
                    SetValueEx(registry_key, name, 0, type, value)
                    result = True
            except WindowsError as e:
                LogHelper.error(str(e))
                result = False
            finally:
                RegistryHelper.close_key(registry_key)
        return result

    @staticmethod
    def get_reg_value(hkey, subkey, name):
        value = None
        registry_key = RegistryHelper.get_key(hkey, subkey, KEY_READ, False)
        if registry_key:
            try:
                if PlatformHelper.is_64bit_machine():
                    value, _ = win32api.RegQueryValueEx(registry_key, name)
                else:
                    value, _ = QueryValueEx(registry_key, name)
            except WindowsError as e:
                LogHelper.error(str(e))
                value = None
            finally:
                RegistryHelper.close_key(registry_key)
        return value

    # Usage: get_key(HKEY_LOCAL_MACHINE, subkey, KEY_READ, is_existed=True):
    @staticmethod
    def get_key(hkey, subkey, access, is_existed=True):
        registry_key = None
        try:
            if PlatformHelper.is_64bit_machine():
                registry_key = win32api.RegOpenKeyEx(hkey, subkey, 0,
                                                     win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS)
            else:
                registry_key = OpenKey(hkey, subkey, 0, access)
        except WindowsError:
            try:
                if is_existed:
                    registry_key = CreateKey(hkey, subkey)
                else:
                    registry_key = None
            except WindowsError as e:
                LogHelper.error(str(e))
                if registry_key:
                    RegistryHelper.close_key(registry_key)
                raise Exception('Fail to get Registry key.')
        return registry_key

    # TODO: not tested
    @staticmethod
    def delete_key(hkey, subkey, name):
        result = None
        registry_key = RegistryHelper.get_key(hkey, subkey, KEY_READ, False)
        print registry_key
        if registry_key:
            try:
                if PlatformHelper.is_64bit_machine():
                    result = win32api.RegDeleteKey(registry_key, name)
                else:
                    result = DeleteKey(registry_key, name)
                print result
            except WindowsError as e:
                print str(e)
                LogHelper.error(str(e))
                result = None
            finally:
                RegistryHelper.close_key(registry_key)
        return result

    @staticmethod
    def close_key(registry_key):
        closed = False
        if registry_key:
            try:
                if PlatformHelper.is_64bit_machine():
                    win32api.RegCloseKey(registry_key)
                    closed = True
                else:
                    CloseKey(registry_key)
                    closed = True
            except WindowsError as e:
                print str(e)
                LogHelper.error(str(e))
                closed = False
        return closed

    @staticmethod
    def write_reg_as_admin(hkey, name, value, type):
        cmd = 'REG ADD \"' + hkey + '\" /v ' + name + ' /t ' + type + ' /d ' + value + ' /f'
        CmdHelper.runas_admin(cmd)


if __name__ == '__main__':
    path = r"SOFTWARE\MozyEnterprise\options"

    assert RegistryHelper.get_reg_value(HKEY_LOCAL_MACHINE, path, "a_auth_host")==None
    assert RegistryHelper.get_reg_value(HKEY_LOCAL_MACHINE, path, "a_bus_host")==None
    assert RegistryHelper.get_reg_value(HKEY_LOCAL_MACHINE, path, "a_triton_host")==None

    RegistryHelper.set_reg_value(HKEY_LOCAL_MACHINE, path, "a_auth_host", "a.test.com", REG_SZ)
    RegistryHelper.set_reg_value(HKEY_LOCAL_MACHINE, path, "a_bus_host", "b.test.com", REG_SZ)
    RegistryHelper.set_reg_value(HKEY_LOCAL_MACHINE, path, "a_triton_host", "t.test.com", REG_SZ)
    RegistryHelper.set_reg_value(HKEY_LOCAL_MACHINE, path, "a_ssl.verifyhostname", 0, REG_DWORD)
    RegistryHelper.set_reg_value(HKEY_LOCAL_MACHINE, path, "a_ssl.verifypeercertificate", 0, REG_DWORD)
    assert RegistryHelper.get_reg_value(HKEY_LOCAL_MACHINE, path, "a_auth_host")=="a.test.com"
    assert RegistryHelper.get_reg_value(HKEY_LOCAL_MACHINE, path, "a_bus_host")=="b.test.com"
    assert RegistryHelper.get_reg_value(HKEY_LOCAL_MACHINE, path, "a_triton_host")=="t.test.com"
    assert RegistryHelper.get_reg_value(HKEY_LOCAL_MACHINE, path, "a_ssl.verifyhostname")==0
    assert RegistryHelper.get_reg_value(HKEY_LOCAL_MACHINE, path, "a_ssl.verifypeercertificate")==0




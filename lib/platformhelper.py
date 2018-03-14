#!/usr/bin/env python
#
# Copyright (c) Maginatics, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


import socket
import platform
import re
import os


from lib.singleton import Singleton
from lib.cmdhelper import CmdHelper



class PlatformHelper(object):
    __metaclass__ = Singleton

    @staticmethod
    def get_ip_address():
        try:
            '''
            If get 127.0.0.1 or 127.0.1.1 on Ubuntu, remember to check hostname and hosts
            e.g.
                10.237.111.5    ubuntu-monitor-agent01     ## /etc/hosts
            '''
            return socket.gethostbyname(PlatformHelper.get_hostfqdn())
        except Exception as e:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
            return s.getsockname()[0]

    @staticmethod
    def get_hostname():
        return socket.gethostname()

    @staticmethod
    def get_hostfqdn():
        # In case no FQDN is available, hostname from gethostname() is returned.
        return socket.getfqdn()

    @staticmethod
    def get_system():
        return platform.system()

    @staticmethod
    def get_release():
        return platform.release()

    @staticmethod
    def get_version():
        return platform.version()

    @staticmethod
    def is_win():
        """
        Test whether os is windows
        :return: True || False
        """
        result = False
        os = PlatformHelper.get_system()
        if os == "Windows":
            result = True
        return result

    @staticmethod
    def is_mac():
        result = False
        os = PlatformHelper.get_system()
        if os == "Darwin":
            result = True
        return result

    @staticmethod
    def is_Linux():
        result = False
        os = PlatformHelper.get_system()
        if os == "Linux":
            result = True
        return result

    @staticmethod
    def is_debian_dist():
        result = False
        cmd = "dpkg --version"
        output = CmdHelper.run(cmd)
        if not re.match(re.compile('.*not found.*'), output):
            result = True
        return result

    @staticmethod
    def is_rpm_dist():
        result = False
        cmd = "rpm --version"
        output = CmdHelper.run(cmd)
        if not re.match(r".*not found.*", output):
            result = True
        return result

    @staticmethod
    def get_dist():
        dist = ""
        if PlatformHelper.is_Linux():
            dist = "-".join(platform.dist())
        return dist

    @staticmethod
    def get_arch():
        """
        usage: get architecture for linux platform
        :return: rpm-32, rpm-64, deb-64, deb-32 or "UNKNOWN" if can not be determined
        """
        arch = "UNKNOWN"
        machine = PlatformHelper.get_machine()
        if PlatformHelper.is_debian_dist():
            if machine == "x86_64":
                arch = "deb-64"
            elif machine == "i386":
                arch = "deb-32"

        elif PlatformHelper.is_rpm_dist():
            if machine == "x86_64":
                arch = "rpm-64"
            elif machine == "i386":
                arch = "rpm-32"

        return arch

    @staticmethod
    def get_machine():
        return platform.machine()

    @staticmethod
    def is_64bit_machine():
        result = False
        machine = PlatformHelper.get_machine()
        if machine == "AMD64":
            result = True
        return result

    @staticmethod
    def is_win7():
        result = False
        release = PlatformHelper.get_release()
        if release == 7:
            result = True
        return result

    @staticmethod
    def get_os_release_info(os_type):
        r"""
        get os release info for worker
        :param os_type:
        :return:
        """
        if os_type.upper() == 'LINUX':
            os_info_file = '/etc'
            is_deb_based = os.path.isfile(os.path.join(os_info_file, 'os-release'))
            is_rpm_based = os.path.isfile(os.path.join(os_info_file, 'system-release'))
            if is_deb_based:

                cmd ="cat /etc/os-release"
                output = CmdHelper.run(cmd)

                for line in output.splitlines():
                    regex = re.match(r'(.*)=(.*)', line)
                    if regex and regex.group(1) == "ID":
                        id = regex.group(2).replace('"', '')
                    if regex and regex.group(1) == "VERSION_ID":
                        version_id = regex.group(2)
                        version_id = version_id.replace('"', '').replace('.',"_")
                result = '{id}_{version_id}'.format(id=id, version_id=version_id)
                return result.upper()
            elif is_rpm_based:
                cmd = "cat /etc/system-release"
                output = CmdHelper.run(cmd)
                result = output.replace(" ", "_").replace('(','').replace(')','').rstrip()
                return result.upper()
            else:
                result ='unknown versions'
                return result.upper()

        if os_type.upper()=='MAC':
            cmd = 'sudo sw_vers'
            output = CmdHelper.run(cmd)
            for line in output.splitlines():
                regex = re.match("ProductVersion:\s+(.*)", line)
                if regex:
                    version = regex.group(1)
                    product_version= version.strip().lstrip().replace('.', '_')
                    return product_version

        if os_type.upper() in ("WINDOWS", 'WIN'):
            # result = '{release}_{version}'.format(release=PlatformHelper.get_system()+PlatformHelper.get_release(), version=PlatformHelper.get_version())
            return platform.platform().replace('.', '_').replace('-', '_').upper()

    @classmethod
    def get_platform_info(cls):
        info = {}

        if cls.is_Linux():
            info['os'] = 'LINUX'
            info['os_version'] = '{version_id}_{arch}'.format(version_id=cls.get_os_release_info('LINUX').upper(), arch=cls.get_arch().upper())
            info['hostname'] = cls.get_hostname().upper()
            info['ip'] = cls.get_ip_address().upper()
            return info

        if cls.is_mac():
            info['os'] = 'MAC'
            info['os_version'] = cls.get_os_release_info('MAC').upper()
            info['hostname'] = cls.get_hostname().upper()
            info['ip'] = cls.get_ip_address().upper()
            return info

        if cls.is_win():
            info['os'] = 'WINDOWS'
            info['os_version'] = cls.get_os_release_info('WINDOWS').upper()
            info['hostname'] = cls.get_hostname().upper()
            info['ip'] = cls.get_ip_address().upper()
            return info

        return RuntimeError('something went wrong with platform info')


if __name__ == '__main__':
    print PlatformHelper.get_workername()
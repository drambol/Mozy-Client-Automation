#!/usr/bin/env python
#
# Copyright (c) EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

import re
from lib.jenkinshelper import JenkinsHelper
from lib.cmdhelper import CmdHelper
from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.linux.lynx_config_loader import LYNX_CONFIG
from lib.downloadhelper import Download_Helper
from configuration.config_adapter import ConfigAdapter


class LynxInstallerDpkg(object):

    def install(self, job, build, pattern, uninstall=True):

        if uninstall:
            self.uninstall()
        if job == "product":
            pattern = self.get_mozy_pattern(pattern)
            packages = self.download_from_mozy(pattern)
        else:
            packages = self.download(job, build, pattern)
        for package in packages:
            self._install_package(package)

    @staticmethod
    def download(job, build, pattern):
        jh = JenkinsHelper(GLOBAL_CONFIG["JENKINS"]["URL"], GLOBAL_CONFIG["JENKINS"]["USERNAME"], GLOBAL_CONFIG["JENKINS"]["KEY"])
        dest = ConfigAdapter.get_installer_path(product='LINUX')
        return jh.download_packages(jh.get_packages(job,build,pattern),dest=dest)


    @staticmethod
    def download_from_mozy(pattern):
        dl = Download_Helper(GLOBAL_CONFIG["MOZY.COM"]["URL2"])
        dest = ConfigAdapter.get_installer_path(product='LINUX')
        packages = []
        packages.append(dl.download_package(dl.get_download_url(pattern), dest=dest))
        return packages

    @staticmethod
    def _install_package(package):

        install_cmd = "dpkg -i %s 2>&1" %(package)
        install_cmd
        CmdHelper.run(install_cmd)

    @staticmethod
    def uninstall():
        uninstall_cmd = "dpkg -P mozybackup 2>&1"
        CmdHelper.run(uninstall_cmd)


    @staticmethod
    def get_mozy_pattern(pattern):
        m = re.search('deb',pattern)
        if m is not None:
            pattern = "%s.deb" % (pattern)
        else:
            pattern = "%s.rpm" % (pattern)
        return pattern





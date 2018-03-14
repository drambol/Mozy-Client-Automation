#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

import re

from lib.cmdhelper import CmdHelper
from lib.jenkinshelper import JenkinsHelper
from configuration.config_adapter import ConfigAdapter
from configuration.global_config_loader import GLOBAL_CONFIG

class LynxInstallerRpm(object):


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
        jh = JenkinsHelper(GLOBAL_CONFIG["JENKINS"]["URL"], GLOBAL_CONFIG["JENKINS"]["USERNAME"],
                           GLOBAL_CONFIG["JENKINS"]["KEY"])
        dest = ConfigAdapter.get_installer_path(product='LINUX')
        return jh.download_packages(jh.get_packages(job, build, pattern), dest=dest)


    @staticmethod
    def _install_package(package):
        install_cmd = "rpm -i %s 2>&1" % (package)
        output = CmdHelper.run(install_cmd)
        return output

    @staticmethod
    def uninstall():
        uninstall_cmd = "rpm -e mozybackup --allmatches 2>&1"
        output = CmdHelper.run(uninstall_cmd)
        return output

    @staticmethod
    def get_mozy_pattern(pattern):
        m = re.search('rpm', pattern)
        if not m:
            pattern = "%s.deb" % (pattern)
        else:
            pattern = "%s.rpm" % (pattern)
        return pattern


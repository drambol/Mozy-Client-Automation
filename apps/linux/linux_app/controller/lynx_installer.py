#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from apps.linux.linux_app.controller import lynx_installer_dpkg, lynx_installer_rpm
from lib.platformhelper import PlatformHelper
from apps.linux.linux_app.controller.lynx_controller import LynxCtrl


class LynxInstaller(object):

    default_job='lynx'
    default_pattern = 'mozypro'

    @classmethod
    def download_and_install(cls, build=-1, job='', pattern=r''):
        if build == 0:
            # keep current build
            return True

        if not pattern:
            pattern = cls.default_pattern

        if not job:
            job = cls.default_job

        installer = cls.create()
        lynx_controller = LynxCtrl()
        if job == "product":
            pattern = "mozypro-%ssetup" % (PlatformHelper.get_arch())
        else:
            #MozyEnterprise-rpm-64-1_5_0_5252.rpm
            pattern = "MozyEnterprise.*%s.*" % (PlatformHelper.get_arch())
        if not lynx_controller.is_client_installed():  # is client is not installed, then install
            print pattern
            installer.install(job, build, pattern)
        else:
            version = lynx_controller.get_client_version()
            if version.find("%s" % build) < 0:
                installer.uninstall()
                installer.install(job, build, pattern)



    @staticmethod
    def create():

        installer = None
        if PlatformHelper.is_debian_dist():
            installer = lynx_installer_dpkg.LynxInstallerDpkg()
        if PlatformHelper.is_rpm_dist():
            installer = lynx_installer_rpm.LynxInstallerRpm()

        return installer










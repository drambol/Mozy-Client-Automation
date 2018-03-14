#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

import re
import os

from lib.jenkinshelper import JenkinsHelper
from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.runner_config_loader import RUNNER_CONFIG
from configuration.config_adapter import ConfigAdapter
from lib.cmdhelper import CmdHelper
from lib.loghelper import LogHelper
from lib.filehelper import FileHelper
from apps.mac.mac_controller.mac_controller import MacController


class MacInstaller(object):
    """

    """

    default_job = "macmozy-release"
    default_pattern= ".*MozyPro.*"

    @classmethod
    def download_and_install(cls, build=-1, job='', pattern=r''):
        if build == 0:
            # keep current build
            return True

        if not pattern:
            pattern = cls.default_pattern

        if not job:
            job = cls.default_job

        version = MacController().get_version()
        LogHelper.info('Current build number is {}'.format(version))

        if version == 0: # not installed
            package = cls.download_package(job=job, build=build, pattern=pattern)
            result = cls.install_package(package[0])
        elif build == -1 or version != build:
            cls.uninstall_package()
            package = cls.download_package(job=job, build=build, pattern=pattern)
            result = cls.install_package(package[0])

        else:
            # not install happen
            result = True
        return result

    @classmethod
    def download_package(cls, job, build, pattern):
        """

        :return:
        """

        jh = JenkinsHelper(GLOBAL_CONFIG["JENKINS"]["URL"], GLOBAL_CONFIG["JENKINS"]["USERNAME"],
                           GLOBAL_CONFIG["JENKINS"]["KEY"])
        dest = ConfigAdapter.get_installer_path(product='MAC')

        # Delete existing images before downloading
        import glob
        images = glob.glob(dest + '/*.dmg')
        for path in images:
            FileHelper.delete_file(path)

        package = jh.get_packages(job, build, pattern)
        return jh.download_packages(package, dest=dest)

    @classmethod
    def install_package(cls, package):
        """
        package: local dmg path
        :return: result
        """
        volume = cls.__mount_image(package)
        pkg_path = os.path.join(volume, 'MozyPro Installer.pkg')

        result = cls.__silent_install(pkg_path)

        LogHelper.debug("un-mount volume")
        cls.__unmount_image(volume)

        return result

    @classmethod
    def install_from_volumes(cls):
        volumes = cls.__find_mounted_volume('Mozy')
        if len(volumes) > 1:
            LogHelper.error("Multiple Mozy volumes found, something went wrong")
            return False

        if len(volumes) == 1:
            pkg_path = os.path.join(volumes[0], 'MozyPro Installer.pkg')
        else:
            image_path = cls.__get_downloaded_image()
            if image_path is None:
                raise StandardError('Package was not downloaded successfully')

            volume = cls.__mount_image(image_path=image_path)
            pkg_path = os.path.join(volume, 'MozyPro Installer.pkg')

        result = cls.__silent_install(pkg_path)
        return result

    @classmethod
    def uninstall_package(cls, removeconfig=True):
        """
        :return:
        """
        result = False
        uninstall_cmd = MacController.prefix_for_sudo() + "sudo -S MozyProBackup uninstall"

        if removeconfig:
            uninstall_cmd += " --removeconfig"

        output = CmdHelper.run(uninstall_cmd)
        if output.find('Uninstall thread done') > 0:
            result = True
            LogHelper.debug("Uninstall mozypro successfully")
        else:
            LogHelper.error("something went wrong with uninstall")

        return result

    @classmethod
    def mount_image_and_launch_installer(cls):
        if MacController.check_process_by_name('Installer'):
            cmd = MacController.prefix_for_sudo() + "sudo -S killall Installer"
            CmdHelper.run(cmd)

        cls.eject_images('Mozy')
        image_path = cls.__get_downloaded_image()
        if image_path is None:
            raise StandardError('Package was not downloaded successfully')

        volume = cls.__mount_image(image_path=image_path)
        pkg_path = os.path.join(volume, 'Mozy.pkg')

        LogHelper.info("Launch GUI installer")
        launch_cmd = 'open "{pkg}"'.format(pkg=pkg_path)
        CmdHelper.run(launch_cmd)

        if not MacController.check_process_by_name('Installer'):
            raise StandardError('Installer was not launched successfully')

        return True

    @classmethod
    def eject_images(cls, pattern):
        result = True
        mounted_volumes = cls.__find_mounted_volume(pattern)
        # print mounted_volumes
        for path in mounted_volumes:
            result = cls.__unmount_image(path)

        return result

    @classmethod
    def files_installed(cls, brand):
        path_app_support = "/Library/Application Support/{brand}".format(brand=brand)
        path_prefpane = "/Library/PreferencePanes/{brand}.prefPane".format(brand=brand)
        path_cache = "/Library/Caches/{brand}/cache.db".format(brand=brand)
        path_log = "/Library/Logs/{brand}.log".format(brand=brand)

        result = FileHelper.dir_exist(path_app_support) and FileHelper.dir_exist(path_prefpane) and FileHelper.file_exist(path_cache) and FileHelper.file_exist(path_log)

        return result

    @classmethod
    def __find_mounted_volume(cls, pattern):
        mounted_volumes = []
        ls_cmd = 'ls /Volumes'
        output = CmdHelper.run(ls_cmd)
        LogHelper.debug("volume under /Volumes have {output}".format(output=output))
        mounted_volumes = [volume for volume in output.splitlines() if re.compile(pattern).match(volume)]
        mounted_volumes = map(lambda x: "/Volumes/{volume}".format(volume=x), mounted_volumes)
        return mounted_volumes

    @classmethod
    def __mount_image(cls, image_path):
        LogHelper.debug("check that package is existed")
        if not FileHelper.file_exist(image_path):
            raise StandardError('file {package} is not existed'.format(package=image_path))

        LogHelper.debug("mount dmg")
        mount_cmd = MacController.prefix_for_sudo() + 'sudo -S hdiutil attach {package}'.format(package=image_path)
        output = CmdHelper.run(mount_cmd)
        LogHelper.debug("mount result is {output}".format(output=output))

        mounted_volumes = cls.__find_mounted_volume(pattern='.*MozyPro.*')

        if len(mounted_volumes) > 1:
            LogHelper.error("More than one volume deteched, something went wrong")

        mounted_volume = mounted_volumes[-1]

        return mounted_volume

    @classmethod
    def __unmount_image(cls, image_path):
        result = False
        unmount_cmd = "diskutil unmountDisk force \"{image_path}\"".format(image_path=image_path)
        output = CmdHelper.run(unmount_cmd)
        LogHelper.debug(output)
        if output.find('successful') >0 :
            LogHelper.debug("install successfull")
            result = True
        else:
            LogHelper.error("install failed")

        return result

    @classmethod
    def __get_downloaded_image(cls):
        result = None

        import glob
        installer_path = ConfigAdapter.get_installer_path(product='MAC')
        build = RUNNER_CONFIG.get("BUILD")
        images = glob.glob(installer_path + '/*{build}*.dmg'.format(build=build))

        if len(images) != 0:  # == 0:
            # raise StandardError('Package was not downloaded successfully')
            result = images[0]
        else:
            job = RUNNER_CONFIG.get("JOB")
            if job is None or job == 'null':
                job = cls.default_job

            brand = RUNNER_CONFIG.get("OEM_CLIENT")
            if brand is None or brand == 'null':
                pattern = cls.default_pattern
            else:
                pattern = ".*" + MacController.normalize_brand_name(brand) + ".*"

            packages = cls.download_package(job, build, pattern)
            if len(packages) != 0:
                result = packages[0]

        return result

    @classmethod
    def __silent_install(cls, pkg_path):
        LogHelper.info("start to install")
        install_cmd = MacController.prefix_for_sudo() + "sudo -S /usr/sbin/installer -pkg \"{path}\" -target {dest}".format(
            path=pkg_path, dest="/")
        output = CmdHelper.run(install_cmd)

        LogHelper.debug(output)
        if output.find('successful') > 0:
            LogHelper.debug("Install successfully")
            result = True
        else:
            LogHelper.error("Install failed")
            result = False

        return result


if __name__ == '__main__':
    """
    cd /Volumes/DarwinPorts-1.2/

    sudo installer -pkg DarwinPorts-1.2.pkg -target "/"

    hdiutil detach /Volumes/DarwinPorts-1.2/
    """
  #   mi = MacInstaller()
  #   package = mi.download_package(job='macmozy-release', build=1648, pattern=r'.*MozyPro.*')
  #
  # #  package= "/mac_installer/mozy-macmozy_2.16.1.1648-MozyPro.dmg"
  #   result = mi.install_package(package[0])
  #   #mi.uninstall_package()

    MacInstaller.uninstall_package()

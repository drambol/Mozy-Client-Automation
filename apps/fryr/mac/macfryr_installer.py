# import time, re
import os
import shutil

from lib.jenkinshelper import JenkinsHelper
from lib.cmdhelper import CmdHelper
from lib.loghelper import LogHelper
from lib.filehelper import FileHelper

from configuration.config_adapter import ConfigAdapter
from configuration.global_config_loader import GLOBAL_CONFIG


class MacFryR_Installer(object):

    @classmethod
    def uninstall(cls):
        pass

    @classmethod
    def download_and_install(cls, build, job):

        volume_name = cls.get_subdir()
        if volume_name is not None:
            CmdHelper.run("diskutil eject '" + volume_name + "'")

        LogHelper.info("Prepare download Mozy Restore Manager from jenkins, build number is " + job)
        jh = JenkinsHelper(GLOBAL_CONFIG["JENKINS"]["URL"], GLOBAL_CONFIG["JENKINS"]["USERNAME"], GLOBAL_CONFIG["JENKINS"]["KEY"])
        dest = ConfigAdapter.get_installer_path('MACFRYR')

        LogHelper.info('Clean up existing files')
        for file in FileHelper.find_file(dest, '*'):
            LogHelper.debug('Delete file %s' %file)
            FileHelper.delete_file(file)
        pattern = 'mozy-fryr'
        packages = jh.download_packages(jh.get_packages(job, build, pattern), dest=dest)

        TARGET_APP = '/Applications/Mozy Restore Manager.app'
        if os.path.exists(TARGET_APP):
            shutil.rmtree(TARGET_APP)
        image_path = packages[0]

        mount_cmd = 'sudo hdiutil attach {package}'.format(package=image_path)
        CmdHelper.run(mount_cmd)

        volume_name = cls.get_subdir()
        ORIGIN_APP = '/Volumes/' + volume_name + '/Mozy Restore Manager.app'
        shutil.copytree(ORIGIN_APP, TARGET_APP)

    @staticmethod
    def get_subdir():
        ls_cmd = 'ls /Volumes'
        output = CmdHelper.run(ls_cmd)
        LogHelper.debug("volume under /Volumes have {output}".format(output=output))
        mounted_volumes = [volume for volume in output.splitlines() if volume.find('Restore Manager') != -1]
        result = None
        if len(mounted_volumes) != 0:
            result = mounted_volumes[0]
        # print result
        return result

import time
from lib.jenkinshelper import JenkinsHelper
from configuration.config_adapter import ConfigAdapter
from configuration.global_config_loader import GLOBAL_CONFIG
from lib.cmdhelper import CmdHelper
from lib.loghelper import LogHelper
from lib.filehelper import FileHelper

class WinFryR_Installer(object):

    @classmethod
    def uninstall(cls, bool):
        if bool is True:
            LogHelper.info("Prepare to uninstall Mozy Restore Manager, it will take about 1 minute.")
            commands = 'wmic product where name="Mozy Restore Manager x64" call uninstall'
            CmdHelper.runas_admin(commands)
            time.sleep(60)
        else:
            LogHelper.info("Skip the uninstalling process.")

    @classmethod
    def download_and_install(cls, build, job):
        # pass
        WinFryR_Installer.uninstall(False)
        LogHelper.info("Prepare download Mozy Restore Manager from jenkins, build number is " + job)
        jh = JenkinsHelper(GLOBAL_CONFIG["JENKINS"]["URL"], GLOBAL_CONFIG["JENKINS"]["USERNAME"], GLOBAL_CONFIG["JENKINS"]["KEY"])
        dest = ConfigAdapter.get_installer_path('WINFRYR')
        LogHelper.info('Clean up existing files')
        for file in FileHelper.find_file(dest, '*'):
            LogHelper.debug('Delete file %s' %file)
            FileHelper.delete_file(file)
        pattern = 'mozy-fryr'
        packages = jh.download_packages(jh.get_packages(job, build, pattern), dest=dest)
        for package in packages:
            if str(package).endswith('setup.exe'):
                LogHelper.info("Prepare to install Mozy Restore Manager.")
                install_cmd = "%s" % (package)
                CmdHelper.run(install_cmd)
                break

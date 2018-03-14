import os
from lib.jenkinshelper import JenkinsHelper
from lib.cmdhelper import CmdHelper
from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.windows.windows_config_loader import WIN_CONFIG
from lib.downloadhelper import Download_Helper
from lib.platformhelper import PlatformHelper
if PlatformHelper.is_win():
    from pywinauto.application import Application

class Windows_Installer(object):


    def __init__(self, oem):
       self.oem = oem
       self.UI = False

    def download_and_install(self, build, job):
        oem = self.oem
        print "job is %s, build is %s" % (job, build)
        if build is None:
            print "Use current build."
            pass
        else:
            self.create(job, build, oem)

    def set_UI(self, UI):
        self.UI = UI
        print UI

    def create(self, job, build, oem):
        pattern = oem
        UI = self.UI
        dest = WIN_CONFIG["INSTALLER_PATH"]
        if oem == "mozypro":
            pattern = "MozyPro"
        elif oem == "MozyHome":
            pattern = "Mozy"
        self.end_process(dest, pattern, build)
        if job == "product":
            packages = self.download_from_mozy(pattern)
        else:
            build = int(build)
            packages = self.download(job, build, pattern)
        if not UI:
            self.install_silent(packages)
        else:
            self.install(packages)

    def install_silent(self, packages):
        for package in packages:
            self._install_package_silent(package)

    def install(self, packages):
        for package in packages:
            self._install_package(package)

    def end_process(self, dest, pattern, build):
        processname = self.get_processname(dest, pattern, build)
        if processname:
            if self.check_process_by_name(processname):
                tskill_cmd = "taskkill /f /t /im %s" % (processname)
                print tskill_cmd
                CmdHelper.run(tskill_cmd)

    def get_processname(self, dest, pattern, build):
        if os.path.isdir(dest):
            list_files = os.listdir(dest)
            for filename in list_files:
                print filename
                if filename.startswith(pattern) and filename.split('.')[-2] == str(build):
                    print filename
                    processname = filename
                    return processname

    @staticmethod
    def download(job, build, pattern):
        jh = JenkinsHelper(GLOBAL_CONFIG["JENKINS"]["URL"], GLOBAL_CONFIG["JENKINS"]["USERNAME"], GLOBAL_CONFIG["JENKINS"]["KEY"])
        dest = WIN_CONFIG["INSTALLER_PATH"]
        pattern = "%s.*.%d.exe" %(pattern, build)
        return jh.download_packages(jh.get_packages(job, build, pattern), dest=dest)

    @staticmethod
    def download_from_mozy(pattern):
        dl = Download_Helper(GLOBAL_CONFIG["MOZY.COM"]["URL1"])
        dest = WIN_CONFIG["INSTALLER_PATH"]
        pattern = "%ssetup.exe" % (pattern.lower())
        packages = []
        packages.append(dl.download_package(dl.get_download_url(pattern), dest=dest))
        return packages

    @staticmethod
    def check_process_by_name(processname):
        result = False
        processname = processname.replace('.exe','')
        cmd = "tasklist|find \"%s\"" % (processname)
        search_result = CmdHelper.run(cmd)
        print search_result
        if search_result:
            result = True
        return result

    @staticmethod
    def _install_package(package):
        Application().start(package)
        # install_cmd = "%s" % (package)
        # print install_cmd
        # CmdHelper.run(install_cmd)

    @staticmethod
    def _install_package_silent(package):
        install_silent = "%s /verysilent /sp" %(package)
        CmdHelper.run(install_silent)



if __name__ == '__main__':
    Windows_Installer("mozypro")._install_package('C:\windows_installer\MozyPro_setup_2.32.5.538.exe')


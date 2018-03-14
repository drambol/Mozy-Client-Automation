import os, urllib2
import yaml
import re
import time

from lib.platformhelper import PlatformHelper
from lib.cmdhelper import CmdHelper
from lib.loghelper import LogHelper
from lib.filehelper import FileHelper
from configuration.config_adapter import ConfigAdapter

class FilebeatHelper(object):

    filebeat_config = ""
    package_name = ""
    product = ""

    @classmethod
    def setup_fb(cls, config, product):
        cls.product=product

        # Check if FB is installed
        if not cls.is_fb_installed():
            cls.install_fb()

            cls.config_fb(config)

        # Check if FB service is started
        if not cls.is_fb_running():
            cls.start_fb()


    @classmethod
    def is_fb_running(cls):
        result = False

        if PlatformHelper.is_Linux():
            cmd = "service filebeat status"
            cmd_output = CmdHelper.run(cmd)
            LogHelper.debug(cmd_output)
            if cmd_output.find("running") >= 0:
                result = True

        if PlatformHelper.is_mac():
            cmd = "ps aux | grep 'filebeat -c' | grep -v 'grep'"
            output = CmdHelper.run(cmd)
            if output.find("filebeat") >= 0:
                result = True

        if PlatformHelper.is_win():
            cmd = "sc query filebeat"
            output = CmdHelper.run(cmd)
            if output.find("RUNNING") >= 0:
                result = True

        if result:
            LogHelper.debug("filebeat is running")
        else:
            LogHelper.info("filebeat is not running")

        return result

    @classmethod
    def is_fb_installed(cls):
        result = False

        if PlatformHelper.is_Linux():
            cmd = "service filebeat status"

        if PlatformHelper.is_mac():
            cmd = "ps aux | grep 'filebeat -c' | grep -v 'grep'"

        if PlatformHelper.is_win():
            cmd = "sc query filebeat"

        output = CmdHelper.run(cmd)
        LogHelper.debug(output)
        match = re.search(r"(FAILED)", output, re.IGNORECASE)

        if match:
            LogHelper.info("filebeat is not installed")
        else:
            result = True
            LogHelper.debug("filebeat is installed")

        return result

    @classmethod
    def start_fb(cls):

        if PlatformHelper.is_mac():
            fb_binary_dir = os.path.join(cls.config_path, cls.package_name.split(".tar.gz")[0])
            os.chdir(fb_binary_dir)
            cmd = "./filebeat -c filebeat.yml &"
            output = os.system(cmd)

        if PlatformHelper.is_Linux():
            cmd = "service filebeat start"
            output = CmdHelper.run(cmd)

        if PlatformHelper.is_win():
            cmd = "sc start filebeat"

            # This is to make sure filebeat service can be started after install
            time.sleep(1)
            output = CmdHelper.run(cmd)

            # service = "Get-WmiObject -ClassWin32_Service-Filter name='filebeat'"
            # service.StartService()
            # service.StopService()

        LogHelper.info("start filebeat result %s" % output)
        return output

    @classmethod
    def kill_fb(cls):
        """
        kill file beat process
        :return:
        """
        result = False

        if PlatformHelper.is_mac() or PlatformHelper.is_Linux():
            cmd = "ps aux | grep 'filebeat -c' | grep -v 'grep'"
            output = CmdHelper.run(cmd)
            process_id = output.split()[1]
            kill_fb_cmd = "kill -9 %s" % process_id
            output = CmdHelper.run(kill_fb_cmd)

        if PlatformHelper.is_win():
            cmd = "sc stop filebeat"
            output = CmdHelper.run(cmd)

        LogHelper.debug(output)
        if cls.is_fb_running():
            LogHelper.error("filebeat service CAN NOT be stopped successfully.")
        else:
            LogHelper.info("filebeat service is stopped")
            result = True

        return result


    @classmethod
    def restart(cls):
        cls.kill_fb()
        cls.start_fb()


    @classmethod
    def download_fb(cls, product=None,dry_run=False, ):

        current_platform = PlatformHelper.get_system()
        fb_site = "https://artifacts.elastic.co/downloads/beats/filebeat/"
        package_name = ""

        if current_platform == "Linux" and PlatformHelper.get_arch() == "deb-64":
            package_name = 'filebeat-5.2.0-amd64.deb'

        if current_platform == "Linux" and PlatformHelper.get_arch() == "deb-32":
            package_name = 'filebeat-5.2.0-i386.deb'

        if current_platform == "Windows":
            package_name = 'filebeat-5.2.0-windows-x86_64.zip'

        if current_platform == "Darwin":
            package_name = 'filebeat-5.2.0-darwin-x86_64.tar.gz'

        installer_dir = ConfigAdapter.get_installer_path(product)

        cls.package_name = package_name
        installer_path = os.path.join(installer_dir, package_name)
        url = fb_site + package_name
        LogHelper.info("installer_path is " + installer_path)
        LogHelper.info("package url is " + url)

        if not FileHelper.dir_exist(installer_dir):
            FileHelper.create_directory(installer_dir)

        if FileHelper.file_exist(installer_path):
            FileHelper.delete_file(installer_path)

        if not dry_run:
            downloaded_package = urllib2.urlopen(url)
            LogHelper.info("download result is %s" % downloaded_package)
            with open(installer_path, 'wb') as output:
                output.write(downloaded_package.read())

        return installer_path

    @classmethod
    def install_fb(cls):
        installer = cls.download_fb()
        LogHelper.info("start to install")

        if PlatformHelper.is_Linux() and PlatformHelper.get_arch() == "deb-64":
            install_cmd = "dpkg -i %s" %installer
            cls.__set_fb_path("/etc/filebeat/")

        if PlatformHelper.is_Linux() and PlatformHelper.get_arch() == "deb-32":
            install_cmd = "rpm -vi %s" %installer
            cls.__set_fb_path("/etc/filebeat/")

        if PlatformHelper.is_win():
            import zipfile
            win_fb_dir = "C:\\filebeat"
            target = os.path.join(win_fb_dir, "filebeat-5.2.0-windows-x86_64")
            installcommnd = os.path.join(target, "install-service-filebeat.ps1")

            zip_ref = zipfile.ZipFile(installer, 'r')
            zip_ref.extractall(win_fb_dir)
            zip_ref.close()
            # FileHelper.rename()

            install_cmd = "powershell.exe %s" %(installcommnd)

            cls.__set_fb_path(target)

            cmd_output = CmdHelper.runas_admin(install_cmd)
            return cmd_output
            # # TODO: Unzip to start" service
            # install_cmd = "to be implemented"
            # win_fb_dir = "C:\\filebeat"
            # if not FileHelper.dir_exist(win_fb_dir):
            #     FileHelper.create_directory(win_fb_dir)
            # cls.__set_fb_path(win_fb_dir)
            # install_cmd = "unzip %s -C %s" % (installer, win_fb_dir)

        if PlatformHelper.is_mac():
            mac_fb_dir = "/filebeat"
            if not FileHelper.dir_exist(mac_fb_dir):
                FileHelper.create_directory(mac_fb_dir)

            cls.__set_fb_path(mac_fb_dir)

            install_cmd = "tar xzvf %s -C %s" % (installer, mac_fb_dir)

        cmd_output = CmdHelper.run(install_cmd)
        LogHelper.info(cmd_output)

    @classmethod
    def config_fb(cls, new_config={}):
        if PlatformHelper.is_mac():
            cls.filebeat_config = os.path.join(cls.config_path, cls.package_name.split(".tar.gz")[0], "filebeat.yml")

        if PlatformHelper.is_Linux() or PlatformHelper.is_win():
            cls.filebeat_config = os.path.join(cls.config_path, 'filebeat.yml')

        # yaml_file = open(cls.filebeat_config, 'r')
        # config = yaml.load(yaml_file)
        # print config

        with open(cls.filebeat_config, 'w') as f:
            config_dict = yaml.dump(new_config, f)

            return config_dict

    @classmethod
    def __set_fb_path(cls, path):
        cls.config_path = path


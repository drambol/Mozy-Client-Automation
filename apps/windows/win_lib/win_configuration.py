from lib.sqlitehelper import SqliteHelper
from lib.registryhelper import RegistryHelper
from lib.filehelper import FileHelper
from lib.loghelper import LogHelper
from lib.platformhelper import PlatformHelper
if PlatformHelper.is_win():
    from _winreg import HKEY_LOCAL_MACHINE

class ConfigurationSetting(object):

    def __init__(self, oem):
        self.oem = oem
        if oem == "MozyEnterprise":
            self.path = r"SOFTWARE\MozyEnterprise"
        if oem == "mozypro":
            self.path = r"SOFTWARE\mozypro"
        if oem == "MozyHome":
            self.path = r"SOFTWARE\mozy"

    def clean_configuration(self):
        """
        this completely and utterly wipes out the configuration
        USE WITH CAUTION!
        :return:
        """
        self.clean_conf()
        self.clean_catch()

    def clean_conf(self):
        path = self.get_configuration_path()
        data_path = path + "conf.dat"
        print data_path
        if FileHelper.file_exist(data_path):
            db = SqliteHelper(data_path)
            db.execute("delete from rules")
            db.execute("delete from filesystem")
            db.execute("delete from fsitems")
            db.execute("delete from set_names")
            db.execute("delete from sets")
            db.close()
        else:
            LogHelper.error("ERROR:Could not find conf to reset. Terminating")


    def clean_catch(self):
        path = self.get_catch_path()
        data_path = path + "cache.dat"
        print data_path
        try:
            db = SqliteHelper(data_path)
            db.execute("delete from files")
            db.close()
        except Exception as e:
            LogHelper.warn("WARN:Cache is Empty, ignoring")
            LogHelper.warn(e.message)


    def get_configuration_path(self):
        path = self.path
        key = "ConfigPath"
        value = RegistryHelper.get_reg_value(HKEY_LOCAL_MACHINE, path, key)
        print value
        return value


    def get_catch_path(self):
        path = self.path
        key = "DataPath"
        value = RegistryHelper.get_reg_value(HKEY_LOCAL_MACHINE, path, key)
        print value
        return value

    def search_result(self):
        path = self.get_catch_path()
        result = SqliteHelper.search_history_result(path)
        return result

if __name__ == '__main__':
    ConfigurationSetting("mozypro").search_result()
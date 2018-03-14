import os

from configuration.runner_config_loader import RUNNER_CONFIG
from configuration.windows.windows_config_loader import WIN_CONFIG
from configuration.linux.lynx_config_loader import LYNX_CONFIG
from configuration.android.android_config_loader import ANDROID_CONFIG
from configuration.ios.ios_config_loader import IOS_CONFIG
from configuration.mac.mac_config_loader import MAC_CONFIG
from configuration.fryr.fryr_config_loader import FRYR_CONFIG, MACFRYR_CONFIG
from configuration.mac_macfryr.mac_macfryr_loader import MAC_MACFRYR_CONFIG
from configuration.mts.mts_config_loader import MTS_CONFIG
from lib.platformhelper import PlatformHelper


class ConfigAdapter(object):
    """
    usage: adapter to access product based configuration vars
    for example: log_path, installer_path, testlink_project_prefix
    """

    @classmethod
    def get_var(cls, key, product=None):
        """
        :param key:
        :param product:
        :return:
        """
        result = None
        if product:
            product=product.upper()
        if not product:
            if RUNNER_CONFIG:
                product = RUNNER_CONFIG.get('PRODUCT').upper()

        # LogHelper.info("product is %s" % product)
        if product == "WINDOWS":
            result = WIN_CONFIG.get(key)

        elif product == "LINUX":
            result = LYNX_CONFIG.get(key)

        elif product == "MAC":
            result = MAC_CONFIG.get(key)

        elif product == "IOS":
            result = IOS_CONFIG.get(key)

        elif product == "ANDROID":
            result = ANDROID_CONFIG.get(key)

        elif product == "WINFRYR":
            result = FRYR_CONFIG.get(key)

        elif product == "MACFRYR":
            result = MACFRYR_CONFIG.get(key)

        elif product == "MAC_MACFRYR":
            result = MAC_MACFRYR_CONFIG.get(key)

        elif product == 'MTS':
            result = MTS_CONFIG.get(key)

        else:
            Exception("product type not implemented %s" % product)

        # LogHelper.debug("result is %s" % result)

        return result

    @classmethod
    def log_path(cls, product=None):
        """
        get log_path
        """
        log_path = cls.get_var('LOG_PATH', product)
        if log_path.startswith('~'):
            log_path = os.path.expanduser(log_path)
        return log_path

    @classmethod
    def get_log_path(cls):
        if PlatformHelper.is_Linux():
            logger_path = ConfigAdapter.log_path("LINUX")
        elif PlatformHelper.is_win():
            logger_path = ConfigAdapter.log_path("WINDOWS")
        elif PlatformHelper.is_mac():
            logger_path = ConfigAdapter.log_path("MAC")
        return logger_path

    @classmethod
    def get_win_log_path(cls):
        return cls.get_log_path("WINDOWS")

    @classmethod
    def get_linux_log_path(cls):
        return cls.get_log_path("LINUX")

    @classmethod
    def get_mac_log_path(cls):
        return cls.get_log_path("MAC")

    @classmethod
    def get_installer_path(cls, product=None):
        """
         get installer_path
        """
        installer_path = cls.get_var('INSTALLER_PATH', product)
        if installer_path.startswith('~'):
            installer_path = os.path.expanduser(installer_path)
        return installer_path

    @classmethod
    def get_testdata_path(cls, product=None):
        """
        get testdata root path
        """
        output = cls.get_var('TESTDATA_PATH', product)
        if output.startswith('~'):
            output = os.path.expanduser(output)
        return output

    @classmethod
    def get_output_path(cls, product=None):
        """
        get output path
        """
        output = cls.get_var('OUTPUT_PATH', product)
        if output.startswith('~'):
            output = os.path.expanduser(output)
        return output

    @classmethod
    def get_download_path(cls, product=None):
        """
        get download path for web-restore
        :param product:
        :return:
        """
        output = cls.get_var('DOWNLOAD_PATH', product)
        if output.startswith('~'):
            output = os.path.expanduser(output)
        return output

    @classmethod
    def get_restore_path(cls, product=None):
        """
        get output path for web-restore
        :param product:
        :return:
        """
        output = cls.get_var('RESTORE_PATH', product)
        if output.startswith('~'):
            output = os.path.expanduser(output)
        return output

    @classmethod
    def get_testlink_prefix(cls, product=None):
        """
        get testlink prefix
        """
        return cls.get_var("TESTLINK_PRJ", product)

    @classmethod
    def get_credential(cls, product=None):
        Exception("not implemented yet")

    @classmethod
    def get_testdata_pros(cls, product=None):
        """
        get testdata property
        return:
         {
          PREFIX:
          SIZE:
          EXT:
         }
        """
        return cls.get_var('TESTDATA_PROPERTY', product)


if __name__ == '__main__':
    pros = ('windows', 'mac', 'linux', 'android', 'ios')
    for pro in pros:
        print pro
        print ConfigAdapter.get_installer_path(product=pro)
        print ConfigAdapter.get_testdata_path(product=pro)
        print ConfigAdapter.get_output_path(product=pro)
        print ConfigAdapter.get_log_path()

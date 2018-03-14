from configuration.global_config_loader import GLOBAL_CONFIG
from lib.platformhelper import PlatformHelper
if PlatformHelper.is_win():
    from apps.windows.win_lib.QA_env import WindowsQAEnv

class QA_Environment(object):


    def __init__(self, oem):
        self.oem = oem
        self._set_env = WindowsQAEnv(self.oem)
        ahost = ""
        bhost = ""
        thost = ""

    def set_qa_env(self):
        pass

    @property
    def set_env(self):
        return self._set_env

    def set_qa_environment(self, env):
        self.get_host(env)

    def get_host(self, env):
        if env.upper() in GLOBAL_CONFIG["QA_ENVIRONMENT"].keys():
           env_hash = GLOBAL_CONFIG["QA_ENVIRONMENT"][env.upper()]
        else:
            raise KeyError("unsupport environment")
        ahost = env_hash.get('mozy.authhost')
        bhost = env_hash.get('mozy.bushost')
        thost = env_hash.get('mozy.tritonhost')
        ssl_verifyhostname = env_hash.get('ssl.verifyhostname')
        ssl_verifypeercertificate = env_hash.get('ssl.verifypeercertificate')
        self.set_ahost(ahost)
        self.set_bhost(bhost)
        self.set_thost(thost)
        self.set_ssl_verifyhostname(ssl_verifyhostname)
        self.set_ssl_verifypeercertificate(ssl_verifypeercertificate)


    def set_ahost(self, ahost):
        key = "ahost"
        value = ahost
        self.set_value_of_key(key, value)

    def set_bhost(self, bhost):
        key = "bhost"
        value = bhost
        self.set_value_of_key(key, value)

    def set_thost(self, thost):
        key = "thost"
        value = thost
        self.set_value_of_key(key, value)

    def set_ssl_verifyhostname(self, ssl_verifyhostname):
        key = "ssl.verifyhostname"
        value = ssl_verifyhostname
        self.set_value_of_key(key, value)

    def set_ssl_verifypeercertificate(self, ssl_verifypeercertificate):
        key = "ssl.verifypeercertificate"
        value = ssl_verifypeercertificate
        self.set_value_of_key(key, value)

    def set_value_of_key(self, key, value):
        self._set_env.set_environment(key, value)

    def get_autoactivate_env(self, env):
        if env.upper() in GLOBAL_CONFIG["QA_ENVIRONMENT"].keys():
           auto_hash = GLOBAL_CONFIG["QA_ENVIRONMENT"][env.upper()]["autoactivate"]
        else:
            raise KeyError("unsupport environment")
        domain_id = auto_hash.get('domain_id')
        ou = auto_hash.get('OU')
        licensetype = auto_hash.get('licensetype')
        self.set_domain_id(domain_id)
        self.set_ou(ou)
        self.set_licensetype(licensetype)

    def set_domain_id(self, domian_id):
        key = "domain_id"
        value = domian_id
        self._set_env.set_autoactivate_env(key, value)

    def set_ou(self, ou):
        key = "OU"
        value = ou
        self._set_env.set_autoactivate_env(key, value)

    def set_licensetype(self, licensetype):
        key = "licensetype"
        value = licensetype
        self._set_env.set_autoactivate_env(key, value)

    def get_assistedactivate_env(self, env):
        if env.upper() in GLOBAL_CONFIG["QA_ENVIRONMENT"].keys():
           assis_hash = GLOBAL_CONFIG["QA_ENVIRONMENT"][env.upper()]["assistactivate"]
        else:
            raise KeyError("unsupport environment")
        domain_id = assis_hash.get('domain_id')
        ou = assis_hash.get('OU')
        licensetype = assis_hash.get('licensetype')
        preferredactivationtype = assis_hash.get('preferredactivationtype')
        self.set_domain_id(domain_id)
        self.set_ou(ou)
        self.set_licensetype(licensetype)
        self.set_preferredactivationtype(preferredactivationtype)

    def set_preferredactivationtype(self, preferredactivationtype):
        key = "preferredactivationtype"
        value = preferredactivationtype
        self._set_env.set_assistedactivate_env(key, value)

    def reset_qa_reg(self, env):
        self.set_domain_id("")
        self.set_licensetype("")
        self.set_ou("")
        self._set_env.clear_reg("options")
        self._set_env.clean_fedid_setting()
        self.set_qa_environment(env)

if __name__ == '__main__':
    # QA_Environment("mozypro").get_assistedactivate_env("qa12")
    QA_Environment("mozypro").recover_to_qa("assistactivate", "qa12")
from lib.singleton import Singleton
from apps.mac.mac_cli_client.commands.auth_cmd import AuthCmd
from apps.mac.mac_cli_client.commands.read_cmd import ReadCmd
from apps.mac.mac_cli_client.commands.rules_cmd import RuleCmd
from apps.mac.mac_cli_client.commands.start_cmd import StartCmd
from apps.mac.mac_cli_client.commands.stop_cmd import StopCmd
from apps.mac.mac_cli_client.commands.write_cmd import WriteCmd


class MacCliClient:

    __metaclass__ = Singleton

    auth_cmd = AuthCmd()
    read_cmd = ReadCmd()
    rule_cmd = RuleCmd()
    start_cmd = StartCmd()
    stop_cmd = StopCmd()
    write_cmd = WriteCmd()

    def __init__(self):
        pass

    @classmethod
    def auto_activation(cls, guid, ou, username):
        para = "--auto-activation --guid={guid} --ou={ou} --username={username}".format(guid=guid, ou=ou, username=username)
        print para
        return cls.auth_cmd.exe_cmd(para)


if __name__ == "__main__":
    from configuration.mac.mac_config_loader import MAC_CONFIG
    import time
    expected_credential = MAC_CONFIG.get('AUTO_ACTIVATION').get("QA12_mozypro")
    guid = "{" + expected_credential.get('DOMAIN_ID') + "}"
    ou = expected_credential.get('OU')
    username_prefix = expected_credential.get('USERNAME_PREFIX')
    str_time = time.strftime("%y%m%d%H%M", time.gmtime())
    username = username_prefix + str_time + "@email.com"
    result = MacCliClient.auto_activation(guid, ou, username)
    print result

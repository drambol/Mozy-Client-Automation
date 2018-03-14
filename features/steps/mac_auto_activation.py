import time
import re
from behave import *

from apps.mac.mac_controller.mac_controller import MacController
from apps.mac.mac_cli_client.mac_cli_client import MacCliClient
from apps.mac.mac_gui_client.mac_gui_client import MacGUIClient

from configuration.mac.mac_config_loader import MAC_CONFIG
from configuration.runner_config_loader import RUNNER_CONFIG


@When('I auto-activate client with credential "{cred}"')
def step_impl(context, cred):
    key_cred_oc = re.sub(r"{oemclient}", RUNNER_CONFIG.get('OEM_CLIENT'), cred)
    key_cre_oc_env = re.sub(r"{env}", RUNNER_CONFIG.get('ENVIRONMENT'), key_cred_oc)
    expected_credential = MAC_CONFIG.get('AUTO_ACTIVATION').get(key_cre_oc_env)
    guid = "{" + expected_credential.get('DOMAIN_ID') + "}"
    ou = expected_credential.get('OU')
    username_prefix = expected_credential.get('USERNAME_PREFIX')
    str_time = time.strftime("%y%m%d%H%M", time.gmtime())
    username = username_prefix + str_time + "@email.com"
    context.username = username
    result = MacCliClient.auto_activation(guid, ou, username)

    activated = False
    if result.find("Saving configuration") != -1:
        activated = True
    activated.should.equal(True)


@Then('I shall see the activated username in summary tab')
def step_impl(context):
    if not MacController.check_process_by_name("System Preferences"):
        MacGUIClient().start_app()
    username = MacGUIClient().summary_tab.get_current_username()
    username.should.equal(context.username)

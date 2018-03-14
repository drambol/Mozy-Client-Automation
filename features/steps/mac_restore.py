import os

from behave import *

from lib.filehelper import FileHelper
from lib.cmdhelper import CmdHelper
from configuration.config_adapter import ConfigAdapter
from configuration.runner_config_loader import RUNNER_CONFIG
# from configuration.mac.mac_config_loader import MAC_CONFIG
from apps.mac.mac_lib.mac_ui_util import MacUIUtils
from apps.mac.mac_controller.mac_controller import MacController
from apps.mac.mac_gui_client.mac_gui_client import MacGUIClient


@When('I click restore button')
def step_impl(context):
    MacUIUtils.click_button(MacGUIClient().summary_tab.btn_restore)
    # cre = '{}_{}'.format(RUNNER_CONFIG.get('ENVIRONMENT'), RUNNER_CONFIG.get('OEM_CLIENT'))
    # expected_credential = MAC_CONFIG.get('CREDENTIAL').get(cre)
    # #password = expected_credential.get('PASSWORD')
    password = context.user.password
    MacGUIClient().restore_auth_window.enter_passoword(password)


@When('I restore last backup files to dest "{dest}"')
def step_impl(context, dest):
    full_destination = os.path.join(ConfigAdapter.get_output_path(), dest)
    if FileHelper.dir_exist(full_destination):
        FileHelper.delete_directory(full_destination)
    FileHelper.create_directory(full_destination)
    cmd = MacController.prefix_for_sudo() + 'sudo -S chmod -R 0777 {0}'.format(full_destination)
    CmdHelper.run(cmd)

    MacGUIClient().view_restore_window.click_browse_button()
    MacGUIClient().restore_dest_window.select_destination(full_destination)
    MacGUIClient().view_restore_window.restore_last_backup()


@When('I close Mozy Restore application')
def step_impl(context):
    brand = RUNNER_CONFIG.get('OEM_CLIENT')
    restore_app_name = MacController.normalize_brand_name(brand) + " Restore"
    cmd = 'killall "{app}"'.format(app=restore_app_name)
    CmdHelper.run(cmd)

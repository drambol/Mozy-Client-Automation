
from behave import *

from lib.loghelper import LogHelper
from lib.filehelper import FileHelper

from configuration.runner_config_loader import RUNNER_CONFIG
from configuration.windows.windows_config_loader import WIN_CONFIG
from configuration.config_adapter import ConfigAdapter
from apps.windows.windows_client import Windows_Client


@Then('I download files')
def step_impl(context):
    winclient = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro"))
    winclient.gui.restore_panel.selectinrestore(ConfigAdapter.get_output_path())
    winclient.gui.restore_panel.startrestore()
    winclient.gui.restore_panel.apply()

@Then('I search by date to download files')
def step_impl(context):
    winclient = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro"))
    import time
    time.sleep(10)
    winclient.gui.restore_panel.select_restore_by_date(ConfigAdapter.get_output_path())
    winclient.gui.restore_panel.startrestore()
    winclient.gui.restore_panel.apply()

@Then('I expect "{restore_dir}" is the same with "{backup_dir}"')
def step_impl(context, restore_dir, backup_dir):

    result = FileHelper.is_dir_same(restore_dir, backup_dir)

    if result:
        for diff in result:
            LogHelper.error("diff files found {path}".format(path=diff))

    len(result).should.equal(0)

@Then('Windows restore successfully')
def step_impl(context):
    backup_dir = WIN_CONFIG.get('TESTDATA_PATH', "c:/test_data")
    output_dir = WIN_CONFIG.get('OUTPUT_PATH', "C:/output")

    step_str = 'Then I expect "{output_dir}" is the same with "{backup_dir}"'
    context.execute_steps(unicode(step_str))
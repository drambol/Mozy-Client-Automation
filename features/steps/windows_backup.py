
from behave import *

from lib.loghelper import LogHelper
from configuration.runner_config_loader import RUNNER_CONFIG
from apps.windows.windows_client import Windows_Client


@When('I {action} windows backup via {func}')
def step_impl(context, action, func):
    winclient = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro"))
    if func.upper() == "CLI":
        if action.upper() == "START":
            winclient.cli.start_backup()
        elif action.upper() == "CANCEL":
            winclient.cli.cancel_backup()
    elif func.upper() == "UI":
        if action.upper() == "START":
            winclient.gui.status_window.startbackup()
        elif action.upper() == "CANCEL":
            winclient.gui.status_window.cancelbackup()
    else:
        LogHelper.error("ERROR: Only support start backup from MozyUTIL or UI.")


@Then('Windows backup successfully')
def step_impl(context):
    winclient = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro"))
    result = winclient.controller.search_result_in_history()
    if result[0] == 0:
        LogHelper.info("backup successfully")
    else:
        LogHelper.error("backup failed")



@Then('Windows backup is cancelled successfully')
def step_impl(context):
    winclient = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro"))
    result = winclient.controller.search_result_in_history()
    if result[0] == -9:
        LogHelper.info("backup is cancelled successfully")
    else:
        LogHelper.error("backup is cancelled unsuccessfully")
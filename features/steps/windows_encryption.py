
from behave import *

from configuration.runner_config_loader import RUNNER_CONFIG
from apps.windows.windows_client import Windows_Client


@When('I {action} change encryption')
def step_impl(context, action):
    winclient = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro"))
    if action.upper() == "APPLY":
        winclient.gui.login_dialog.change_encrption(apply=True)
    else:
        winclient.gui.login_dialog.change_encrption(apply=False)

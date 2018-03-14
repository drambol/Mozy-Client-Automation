from behave import *
from lib.platformhelper import PlatformHelper
if PlatformHelper.is_win():
    from apps.windows.windows_controller import Windows_Controller

from configuration.runner_config_loader import RUNNER_CONFIG


@When ('I reset configration by {client} Client')
def step_impl(context, client):
    if client == "windows":
        winclient = Windows_Controller(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro"))
        winclient.set_unconfigured_status()
        winclient.reset_reg(RUNNER_CONFIG.get('ENVIRONMENT', "QA12"))
        winclient.restart_services(force = True)
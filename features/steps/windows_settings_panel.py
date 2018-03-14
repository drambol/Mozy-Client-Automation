
from behave import *
import time
from configuration.runner_config_loader import RUNNER_CONFIG
from apps.windows.windows_client import Windows_Client

@When('I select {panelname} panel in Settings')
def stem_impl(context, panelname):
    time.sleep(2)
    winclient = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro"))
    winclient.gui.settings_window.select_panel(panelname)
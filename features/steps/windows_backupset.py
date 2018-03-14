
from behave import *

from lib.loghelper import LogHelper
from configuration.windows.windows_config_loader import WIN_CONFIG
from configuration.runner_config_loader import RUNNER_CONFIG

from apps.windows.windows_client import Windows_Client


@When('I create windows backupset as {backupsetname} via {func}')
def step_impl(context, backupsetname, func):
    root_path = WIN_CONFIG.get('TESTDATA_PATH', "c:/testdata")
    if func == "CLI":
        Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).cli.create_backupset(root_path, backupsetname)
    elif func.upper() == "UI":
        # TODO: Further invesigate pywinauto to support right click popup menu
        pass
    else:
        LogHelper.error("ERROR: Only support start backup from MozyUTIL or UI.")

@When('I open {windowname} window')
def step_impl(context, windowname):
    if windowname.upper() == "Welcome".upper():
        Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).gui.setup_window.open_setupwindow()
    else:
        Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).gui.status_window.open(windowname)

@When('I select files in settings filesystem')
def step_impl(context):
    testdata_folder = WIN_CONFIG.get('TESTDATA_PATH', "c:/test_data")
    winclient = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro"))
    winclient.gui.filesystem_panel.selectinfilesystem(root_path=testdata_folder)
    winclient.gui.settings_window.applychange()

@when("I generate clean configuration of windows Client")
def step_impl(context):
    win_controller = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).controller
    win_controller.wipe_configuration()
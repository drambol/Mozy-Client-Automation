

from behave import *


from apps.linux.linux_app.linux_gui_client import LinuxGUIClient
from lib.loghelper import LogHelper


@When('I stop backup')
def step_impl(context):
    LinuxGUIClient.stop_cmd.stop()



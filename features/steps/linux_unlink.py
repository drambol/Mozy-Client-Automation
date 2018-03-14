from behave import *

from apps.linux.linux_app.linux_gui_client import LinuxGUIClient


@When('I unlink machine')
def step_impl(context):
    LinuxGUIClient.unlink_cmd.unlink()
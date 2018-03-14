
from behave import *


from apps.linux.linux_app.linux_gui_client import LinuxGUIClient


@When('I start backup')
def step_impl(context):
    LinuxGUIClient.start_cmd.start()

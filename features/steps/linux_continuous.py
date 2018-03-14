from behave import *


from apps.linux.linux_app.linux_gui_client import LinuxGUIClient
from lib.loghelper import LogHelper


@When('I set backup mode as "{mode}"')
def step_impl(context, mode):
    if mode.lower() == 'continuous':
        LogHelper.info('set continuous mode')
        LinuxGUIClient.continuous_cmd.set_continuous()
    elif mode.lower() == 'on-demand':
        LogHelper.info('set on-demand mode')
        LinuxGUIClient.continuous_cmd.set_on_demand()
    else:
        ValueError('unexpected mode %s' % mode)


@Then('I expect continuous output is {result}')
def query_continuous_result(context, result):
    actual_result = LinuxGUIClient.continuous_cmd.get_mode()

    if result.upper() == "ON":
        expect_result = LinuxGUIClient.continuous_cmd.CONTINUOUS

    if result.upper() == 'OFF':
        expect_result = LinuxGUIClient.continuous_cmd.ON_DEMAND

    expect_result.should.equal(actual_result)





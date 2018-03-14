import re
import sure, time

from behave import *


from apps.linux.linux_app.linux_gui_client import LinuxGUIClient
from apps.linux.linuxclient import LinuxClient
from lib.loghelper import LogHelper


@When('I wait state to be "{expected_state}"')
def step_impl(context, expected_state):
    LinuxClient().cli.state_cmd.wait_state(expected_state)


@When('I wait for sock ready')
def step_impl(context):
    if not LinuxClient().controller.wait_for_sock_ready():
        LogHelper.error('linux sock is not ready')
        context.execute_steps('When I restart Linux Client')


@Then('I expect state be one of "{expected_status}"')
@When('I wait state be one of "{expected_status}"')
def step_impl(context, expected_status):
    LogHelper.debug("checked expected be one of %s" %expected_status)
    expected = [state.strip().strip() for state in re.split(r",|;|:", expected_status.upper())]
    LinuxClient().cli.state_cmd.wait_state(expected)


@When('Linux Client is ready for backup at "{expected_mode}" mode')
@When('Linux Client is running at "{expected_mode}" mode')
def step_impl(context, expected_mode):
    if expected_mode.upper() == 'ON-DEMAND':
        LinuxGUIClient.continuous_cmd.set_on_demand()
        LinuxClient().controller.restart()
        context.execute_steps(unicode('When I wait state be one of "IDLE,AUTHENTICATED"'))
    if expected_mode.upper() == 'CONTINUOUS':
        LinuxGUIClient.continuous_cmd.set_continuous()
        if LinuxGUIClient.state_cmd.current_state().upper() not in ('RUNNING'):
            LinuxClient().controller.restart()
            context.execute_steps(unicode('When I wait state be one of "RUNNING"'))


@When('I wait backup running')
def step_impl(context):
    timeout = 300
    sleep_time = 5
    current_time = 0
    current_state = LinuxGUIClient.state_cmd.current_state()
    while current_state.upper().find('RUNNING')<0 and current_time <= timeout:
        time.sleep(sleep_time)
        current_state = LinuxGUIClient.state_cmd.current_state()
        current_time += sleep_time
    if current_state.upper().find('RUNNING') <0 or current_time >= timeout:
        raise Exception('time out')


@Then('State should be {expected_state}')
def step_impl(context, expected_state):
    expected_state.upper()
    LogHelper.debug("expected status is %s" % expected_state)
    actual_status = LinuxGUIClient.state_cmd.current_state().upper()
    LogHelper.debug("actual_status status is %s" % actual_status)
    try:
        expected_state.upper().should.equal(actual_status.upper())
    except AssertionError as e:
        LogHelper.error(e.message)
        raise e


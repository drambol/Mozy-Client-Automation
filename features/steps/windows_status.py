from behave import *


from configuration.runner_config_loader import RUNNER_CONFIG
from apps.windows.windows_client import Windows_Client


@Then('Windows state is "{state}"')
def step_impl(context, state):
    status = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).cli.wait_for_state(state.upper())
    status.should.equal(True)


@When('I wait windows backup state "{state}"')
def step_impl(context, state):
    status = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).cli.wait_for_state(state.upper())
    status.should.equal(True)

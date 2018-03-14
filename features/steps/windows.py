from behave import *


from configuration.runner_config_loader import RUNNER_CONFIG
from apps.windows.windows_client import Windows_Client


@When('I get current machine id')
def step_impl(context):
    machine_id = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).controller.get_machine_id()
    context.machine_id = machine_id
    return context.machine_id

@When('I check current machine backup performance log')
def step_impl(context):
    # Send machine_id to triton
    context.machine_id
    pass

@Then('I encrypt data with {encryptiontype} successfully')
def step_impl(context, encryptiontype):
    # context.execute_steps(unicode('When I log in BUS console to select my restore machine'))
    context.execute_steps(unicode('When I get current machine id'))

    step_str = 'Then Machine {machine} is encrypted with {encryptiontype}'.format(machine=context.machine_id, encryptiontype=encryptiontype)
    context.execute_steps(unicode(step_str))
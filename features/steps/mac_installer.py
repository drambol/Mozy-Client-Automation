from behave import *
import sure


from apps.mac.mac_controller.mac_controller import MacController
@When('Mac Client is installed')
def step_impl(context):
    result = MacController().is_client_running()
    result.should.equal(True)
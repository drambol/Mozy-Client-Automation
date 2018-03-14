from behave import *

from apps.linux.linux_app.linux_gui_client import LinuxGUIClient


@When('I disable throttle')
def disable_throttle(context):
    output = LinuxGUIClient.throttle_cmd.disable_throttle()
    return output


@Then('I expect throttle is {throttle_status}')
def check_throttle_status(context, throttle_status):
    result = LinuxGUIClient.throttle_cmd.is_throttle_on()

    if throttle_status.upper() == "ENABLED":
        expect_result = True
    if throttle_status.upper() == 'DISABLED':
        expect_result = False

    expect_result.should.eql(result)

@When('I enable throttle to {unit} {value}')
def set_throttle(context, unit, value):
    if unit.upper()== 'BPS':
        LinuxGUIClient.throttle_cmd.enable_throttle(bps=int(value))
    if unit.upper() == 'KPS':
        LinuxGUIClient.throttle_cmd.enable_throttle(kps=int(value))


@Then('I expect throttle value is "{expect_value}"')
def verify_throttle_value(context, expect_value):

    result = LinuxGUIClient.throttle_cmd.list_throttle().rstrip().lstrip()

    expect_value.should.equal(result)



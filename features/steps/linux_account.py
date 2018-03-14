from behave import *


from apps.linux.linux_app.linux_gui_client import LinuxGUIClient
from lib.loghelper import LogHelper


@Then('I expect account details with')
def step_impl(context):
    account_dict = LinuxGUIClient().account_cmd.get_account_details()
    headings = context.table.headings
    for row in context.table.rows:
        for item in headings:
            expected_value = row.get(item)
            actual_value = account_dict.get(item)
            LogHelper.info("compare {item}: expected value {ex} and actual value {ac}".format(item=item, ex=expected_value,
                                                                                              ac=actual_value))

            try:
                actual_value.should.equal(expected_value)
            except AssertionError as e:
                LogHelper.error(e.message)
                raise e


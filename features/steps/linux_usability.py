import sure
from behave import *

from apps.linux.linux_app.linux_gui_client import LinuxGUIClient
from lib.loghelper import LogHelper

@Then('I expect backup filecount is {expected_filecount}')
@When('I expect backup filecount is {expected_filecount}')
def step_impl(context, expected_filecount):
    int_expected_filecount = int(expected_filecount)
    actual_file_count = LinuxGUIClient.filecount_cmd.get_file_count()
    try:
        LogHelper.info("compare actural_file_count %d ith expect %d" % (actual_file_count , int_expected_filecount))
        actual_file_count.should.be.greater_than_or_equal_to(int_expected_filecount)
    except AssertionError as e:
        LogHelper.error(e.message)
        raise e


@Then('I expect last backup status with')
@When('I expect last backup status with')
def step_impl(context):
    result = LinuxGUIClient.lastbackup_cmd.parse_lastBackup(utc=None)
    for key in context.table.headings:
        for row in context.table.rows:
            expected_result = row.get(key.lower())
            actual_result = result.get(key.lower())
            LogHelper.info('expected %s and actual is %s' % (expected_result, actual_result))
            try:
                LogHelper.info("compare expected %s with actual result %s")
                actual_result.should.equal(expected_result)
            except AssertionError as e:
                LogHelper.error(e.message)
                raise e



@when('test')
def step_impl(context):
    raise Exception('error ')

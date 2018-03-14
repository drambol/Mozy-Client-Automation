

import time

import sure
from behave import *

from lib.loghelper import LogHelper
from apps.linux.linux_app.linux_gui_client import LinuxGUIClient


@When('I check current files proccessed')
def step_impl(context):
    result = LinuxGUIClient.history_cmd.get_continuous_mode_summary()
    change_processed = result.get('changes_processed')
    LogHelper.info("changes proccessed is %s" % change_processed)
    if change_processed is not None:
        context.change_processed_before = int(change_processed)
    else:
        context.change_processed_before = 0
    print(context.change_processed_before)


@Then('I expect current files proccessed increased greater than {number}')
def step_impl(context, number):
    if context.change_processed_before is not None:
        expected_number = int(context.change_processed_before) + int(number)
    else:
        raise ValueError('unexpected ')

    current_change_process = LinuxGUIClient.history_cmd.get_continuous_mode_summary().get('changes_processed') or -1
    current_change_process = int(current_change_process)
    LogHelper.info("current changes process is %d" % current_change_process)
    delta = expected_number - int(current_change_process)
    try:
        LogHelper.debug("check changes process number")
        delta.should.be.greater_than_or_equal_to(0)
    except AssertionError as e:
        LogHelper.error(e.message)
        raise e


@Then('I expected last backup result in history is as below')
def step_impl(context):
    result = LinuxGUIClient.history_cmd.parse_history(limit=1)
    if result:
        history = result[-1]
    else:
        LogHelper.error("no history returned")
        raise Exception('No history detected')
    headings = context.table.headings
    for row in context.table.rows:
        for item in headings:
            LogHelper.info('checking history result for %s' %item)
            expected_item = row[item]
            LogHelper.info('expected result is %s' % expected_item)
            actual_value = getattr(history,item)
            LogHelper.info('acutal result is %s' % actual_value)
            try:
                actual_value.should.equal(expected_item)
            except AssertionError as e:
                LogHelper.error(e.message)
                raise e


@When('I check last history result')
def check_last_history_result(context):
    last_history_result = LinuxGUIClient.history_cmd.parse_history(limit=1, tabs=None).pop()
    context.last_history_result = last_history_result


@Then('I expect last history result {is_changed}')
def is_last_history_changed(context, is_changed):
    previous_history_result = context.last_history_result

    if is_changed.upper() == 'CHANGED':
        pass

    if is_changed.upper() == 'UNCHANGED':
        last_history_result = LinuxGUIClient.history_cmd.parse_history(limit=1, tabs=None).pop()
        last_history_result.should.equal(previous_history_result)

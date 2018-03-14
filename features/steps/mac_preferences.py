import time
from behave import *

from apps.mac.mac_controller.mac_controller import MacController
from apps.mac.mac_gui_client.mac_gui_client import MacGUIClient
from apps.mac.mac_gui_installer.mac_gui_installer import AppUIElement

# from configuration.runner_config_loader import RUNNER_CONFIG


@When('I click the "Back Up Now" button')
def step_impl(context):
    step_str = 'When I visit "summary" tab'
    context.execute_steps(unicode(step_str))
    MacGUIClient().summary_tab.click_backup()


@Then('I shall see the text on the "Back Up Now" button changes to "{text}"')
def step_impl(context, text):
    result = True
    time.sleep(2)
    # btn_text = MacGUIClient().summary_tab.get_title_btn_backup()
    # btn_text.should.equal(text)
    matcher = {'AXRole': 'AXButton'}
    matcher['AXTitle'] = text
    btn_backup = AppUIElement.from_bundle(MacController().spbundleid, matcher)
    if btn_backup is None:
        result = False
    result.should.equal(True)


@When('I click the "History..." button')
def step_impl(context):
    step_str = 'When I visit "summary" tab'
    context.execute_steps(unicode(step_str))
    MacGUIClient().summary_tab.click_history()


@Then('I shall see a sheet containing the backup history is pulled down')
def step_impl(context):
    result = True
    matcher = {'AXRole': 'AXSheet'}
    sheet_history = AppUIElement.from_bundle(MacController().spbundleid, matcher)
    if sheet_history is None:
        result = False
    result.should.equal(True)

    matcher = {'AXRole': 'AXRow', 'AXSubrole': 'AXTableRow'}
    first_entry = sheet_history.find_child(matcher)
    first_entry.left_click()
    time.sleep(1)
    matcher = {'AXRole': 'AXStaticText', 'AXValue': '1 / 1'}
    text_file_sent = sheet_history.find_child(matcher)
    if text_file_sent is None:
        result = False
    matcher = {'AXRole': 'AXStaticText', 'AXValue': 'Success'}
    text_result = sheet_history.find_child(matcher)
    if text_result is None:
        result = False
    result.should.equal(True)

    matcher = {'AXRole': 'AXButton', 'AXTitle': 'Done'}
    btn_done = sheet_history.find_child(matcher)
    btn_done.click()


@When('I select the recommended backup sets "{backup_set_name}"')
def step_impl(context, backup_set_name):
    step_str = 'When I visit "Files & Folders" tab'
    context.execute_steps(unicode(step_str))
    # MacCliClient().rule_cmd.remove_all_rules()
    files_folder_tab = MacGUIClient().files_folder_tab
    files_folder_tab.click_advance_button()
    files_folder_tab.show_suggested_backup_sets()

    matcher = {'AXRole': 'AXTextField'}
    matcher['AXValue'] = backup_set_name + "*"
    tr_text_doc = AppUIElement.from_bundle(MacController().spbundleid, matcher)
    matcher = {'AXRole': 'AXCheckBox'}
    tr_checkbox_doc = AppUIElement(tr_text_doc.get_native_parent(), matcher)
    tr_checkbox_doc.left_click()
    matcher = {'AXRole': 'AXButton', 'AXTitle': 'OK'}
    btn_ok = AppUIElement(tr_text_doc.get_native_ancestor(level=4), matcher)
    btn_ok.click()

    time.sleep(5)
    files_folder_tab.click_OK_button()


@Then('I expected the selected files are shown by "{field}"')
def step_impl(context, field):
    step_str = 'When I visit "summary" tab'
    context.execute_steps(unicode(step_str))

    table = MacGUIClient().summary_tab.get_summary_table()
    result = True
    current_value = table.get(field)
    current_time = 0
    wait_time = 120
    sleep_time = 5
    while current_value.find("0 files") >= 0 and current_time < wait_time:
        time.sleep(sleep_time)
        current_time += sleep_time
        table = MacGUIClient().summary_tab.get_summary_table()
        current_value = table.get(field)

    if current_value.find("0 files") >= 0:
        result = False
    result.should.equal(True)

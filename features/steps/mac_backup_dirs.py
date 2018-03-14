import os
import time

from behave import *

from apps.mac.mac_gui_client.mac_gui_client import MacGUIClient

from configuration.config_adapter import ConfigAdapter


@When('I add backup dirs as')
def step_impl(context):
    step_str = 'When I visit "Files & Folders" tab'
    context.execute_steps(unicode(step_str))
    # MacCliClient().rule_cmd.remove_all_rules()
    files_folder_tab = MacGUIClient().files_folder_tab
    files_folder_tab.click_advance_button()
    testdata_root = ConfigAdapter.get_testdata_path()
    for row in context.table:
        files_folder_tab.show_add_files_browser()
        time.sleep(1)
        files_folder_tab.select_root_dest()
        time.sleep(1)
        entity = row.get('include_dirs') or row.get('include_files')
        backup_full_path = os.path.join(testdata_root, entity)
        from lib.filehelper import FileHelper
        w_time = 60
        while not FileHelper.dir_exist(backup_full_path) and w_time > 0:
            w_time -= 5
        files_folder_tab.select_backupdir(backup_full_path)
    files_folder_tab.click_OK_button()

from behave import *

from apps.mac.mac_gui_client.mac_gui_client import MacGUIClient
from apps.mac.mac_controller.mac_controller import MacController
from apps.mac.status_menu.status_menu import StatusMenu
from configuration.runner_config_loader import RUNNER_CONFIG

from lib.loghelper import LogHelper

import sure
import time


@When('I start backup from GUI')
def step_impl(context):
    step_str = 'When I visit "summary" tab'
    context.execute_steps(unicode(step_str))
    MacGUIClient().summary_tab.backup_now()


@When('I wait to backup finished')
def step_impl(context):

    table = MacGUIClient().summary_tab.get_summary_table()

    eslaped_time = 0
    sleep_time = 10
    while table.get('Next Backup:') == 'in progress' and eslaped_time < 300:
        time.sleep(sleep_time)
        eslaped_time += sleep_time
        table = MacGUIClient().summary_tab.get_summary_table()


@Then('I shall see the status menu gets updated and says {number} files backed up')
def step_impl(context, number):
    brand = RUNNER_CONFIG.get('OEM_CLIENT')
    status_app_name = MacController.normalize_brand_name(brand) + " Status"
    status_menu = StatusMenu(status_app_name)
    status_menu.expand()
    title = status_menu.get_menu_text_by_index(0)
    str_number = format(int(number), ',')
    str_backedup = 'Backed Up: {number} files'.format(number=str_number)
    result = title.startswith(str_backedup)
    result.should.equal(True)

    if title.find('--') != -1:
        result = False
    result.should.equal(True)
    status_menu.collapse()


@Then('I expected "{field}" is {check_value} files')
def step_impl(context, field, check_value):
    step_str = 'When I visit "summary" tab'
    context.execute_steps(unicode(step_str))
    current_value = ''

    table = MacGUIClient().summary_tab.get_summary_table()
    current_value = table.get(field)
    current_time = 0
    wait_time = 60
    sleep_time = 5
    while current_value.find(check_value) < 0 and current_time < wait_time:
        time.sleep(sleep_time)
        current_time += sleep_time
        table = MacGUIClient().summary_tab.get_summary_table()
        current_value = table.get(field)

    current_value


@When('I close Mac Client')
def step_impl(context):
    MacGUIClient().close_app()
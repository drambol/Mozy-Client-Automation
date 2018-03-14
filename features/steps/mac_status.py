import time
from behave import *

from apps.mac.mac_controller.mac_controller import MacController
from apps.mac.status_menu.status_menu import StatusMenu

from configuration.runner_config_loader import RUNNER_CONFIG


@When('I click the status icon')
def step_impl(context):
    brand = RUNNER_CONFIG.get('OEM_CLIENT')
    status_app_name = MacController.normalize_brand_name(brand) + " Status"
    status_menu = StatusMenu(status_app_name)
    context.status_menu = status_menu
    status_menu.left_click()


@When('I right-click the status icon')
def step_impl(context):
    brand = RUNNER_CONFIG.get('OEM_CLIENT')
    status_app_name = MacController.normalize_brand_name(brand) + " Status"
    status_menu = StatusMenu(status_app_name)
    context.status_menu = status_menu
    status_menu.right_click()


@Then('The following menu items are present')
def step_impl(context):
    time.sleep(1)
    status_menu = context.status_menu
    result = True
    for row in context.table:
        menuname = row['name']
        if status_menu.find_menu_item_by_name(menuname) is None:
            result = False
    result.should.equal(True)

    status_menu.collapse()


@When('I click the menu item "{menuname}"')
def step_impl(context, menuname):
    brand = RUNNER_CONFIG.get('OEM_CLIENT')
    status_app_name = MacController.normalize_brand_name(brand) + " Status"
    status_menu = StatusMenu(status_app_name)
    context.status_menu = status_menu

    status_menu.expand()
    time.sleep(1)
    status_menu.click_menu_item(menuname)
    status_menu.collapse()

    if menuname == 'Pause Backup':
        time.sleep(10)


@Then('I shall see the action field displays as "{menuname}"')
def step_impl(context, menuname):
    time.sleep(1)
    status_menu = context.status_menu
    status_menu.expand()

    result = False
    if status_menu.find_menu_item_by_name(menuname) is not None:
        result = True
    result.should.equal(True)

    status_menu.collapse()


@Then('I shall see the pending status field displays as "{menuname}"')
def step_impl(context, menuname):
    status_menu = context.status_menu
    status_menu.expand()

    result = False
    wait_t = 180
    while result is False and wait_t > 0:
        if status_menu.find_menu_item_by_name(menuname) is not None:
            result = True
        wait_t -= 1
    result.should.equal(True)

    status_menu.collapse()


@When('The backup is {number} percent left')
def step_impl(context, number):
    step_str = 'When I click the status icon'
    context.execute_steps(unicode(step_str))
    status_menu = context.status_menu
    status_menu.expand()

    file_size = context.file_size
    size = float(file_size) / (1024.0 * 1024.0)
    size_to_left = size * float(number)
    size_left = status_menu.get_left_size()
    while size_left > size_to_left:
        time.sleep(1)
        size_left = status_menu.get_left_size()

    status_menu.collapse()

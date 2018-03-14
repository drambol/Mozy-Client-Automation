from behave import *
from apps.ios.iOS_installer import iOS_Installer
from apps.ios.iOS_controller import iOS_Controller
from apps.ios.ios_gui.my_mozy_view import My_Mozy_View
from apps.ios.ios_gui.all_files import All_Files_View
from apps.ios.ios_gui.sync_folder import Sync_View
from apps.ios.ios_gui.backup_machine import Machine_View
from apps.ios.appium_driver import Driver

@When('I start iOS simulator and install Mozy iOS APP')
def step_impl(context):
    # Driver.restart_appium_server()
    # iOS_Installer.create_driver()
    pass # All these steps are implemented in runner.py (native_client.controller.prepare_environment(environment))

@Then('I log in Mozy iOS App with default account')
def step_impl(context):
    iOS_Controller.login()

@Then('I view My Mozy tab and check all elements in Mozy iOS')
def step_impl(context):
    My_Mozy_View.navigate_to()
    My_Mozy_View.verify_history()
    My_Mozy_View.verify_recent()
    My_Mozy_View.verify_photos()
    My_Mozy_View.verify_documents()
    My_Mozy_View.verify_music()
    My_Mozy_View.verify_videos()

@Then('I view All Files tab and check all elements in Mozy iOS')
def step_impl(context):
    All_Files_View.navigate_to()
    All_Files_View.verify_sync()
    All_Files_View.verify_backups()

@Then('I view the files in Sync folder in Mozy iOS')
def step_impl(context):
    Sync_View.navigate_to()
    Sync_View.verify_sync_files()

@Then('I search file in Sync folder with keyword {keyword} in Mozy iOS')
def step_impl(context, keyword):
    Sync_View.navigate_to()
    Sync_View.verify_search_function(keyword)

@Then('I click into each backup machine and search with keyword {keyword} in Mozy iOS')
def step_impl(context, keyword):
    machine_quantity = Machine_View.get_machine_quantity()
    for i in range(machine_quantity):
        Machine_View.navigate_to(i)
        Machine_View.verify_ui()
        Machine_View.verify_search_function(keyword)

@Then('I verify Mozy iOS APP version is {app_version}')
def step_impl(context, app_version):
    iOS_Controller.verify_version(app_version)

@Then('I logout Mozy iOS APP')
def step_impl(context):
    iOS_Controller.logout()

@Then('I close iOS simulator and appium server')
def step_impl(context):
    iOS_Controller.tearDown()
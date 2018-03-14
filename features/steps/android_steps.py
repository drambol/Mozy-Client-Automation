from behave import *
from apps.android.android_installer import Android_Installer
from apps.android.android_controller import Android_Controller
from apps.android.android_gui.my_mozy_view import My_Mozy_View
from apps.android.android_gui.all_files import All_Files_View
from apps.android.android_gui.sync_folder import Sync_View
from apps.android.android_gui.backup_machine import Machine_View

@When('I start Android simulator and appium server')
def step_impl(context):
    # Android_Client.start_simulator()
    pass

@Then('I install Mozy Client to the Android Simulator')
def step_impl(context):
    Android_Installer.create_driver()

@Then('I log in Mozy Android App with default account')
def step_impl(context):
    Android_Controller.login()

@Then('I sign out Mozy Android App')
def step_impl(context):
    Android_Controller.logout()

@Then('I verify Mozy Android APP version')
def step_impl(context):
    Android_Controller.verify_version()

@Then('I view My Mozy tab and check all elements')
def step_impl(context):
    My_Mozy_View.navigate_to()
    My_Mozy_View.verify_downloaded()
    My_Mozy_View.verify_recent()
    My_Mozy_View.verify_photos()
    My_Mozy_View.verify_documents()
    My_Mozy_View.verify_music()
    My_Mozy_View.verify_videos()

@Then('I view All Files tab and check all elements')
def step_impl(context):
    All_Files_View.navigate_to()
    All_Files_View.verify_sync()
    All_Files_View.verify_backups()

@Then('I view the files in Sync folder')
def step_impl(context):
    Sync_View.navigate_to()
    Sync_View.verify_sync_files()

@Then("I search file in Sync folder with keyword '{keyword}'")
def step_impl(context, keyword):
    Sync_View.navigate_to()
    Sync_View.verify_search_function(keyword)

@Then("I click into each backup machine and search with keyword '{keyword}'")
def step_impl(context, keyword):
    machine_quantity = Machine_View.get_machine_quantity()
    for i in range(machine_quantity):
        Machine_View.navigate_to(i)
        Machine_View.verify_ui()
        Machine_View.verify_search_function(keyword)

@Then('I close Android simulator and appium server')
def step_impl(context):
    Android_Controller.tearDown()
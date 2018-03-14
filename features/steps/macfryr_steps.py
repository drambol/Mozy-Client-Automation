from behave import *
from apps.fryr.mac.macfryr_controller import MacFryR_Controller
from apps.fryr.test_data import Test_Data


@Then("I use Mac Restore Manager to restore the selected files with Useremail '{email}' and Password '{password}'")
def step_impl(context, email, password):
    MacFryR_Controller.launch_restore_manager()
    MacFryR_Controller.login(email, password)
    MacFryR_Controller.public_restore_flow()


@Then("I use Mac Restore Manager to restore the selected files with useremail and password")
def step_impl(context):
    MacFryR_Controller.launch_restore_manager()
    MacFryR_Controller.login(context.table[0].get('user_email'), context.table[0].get('password'))
    MacFryR_Controller.public_restore_flow(context.table[0].get('encrypt_type'), context.table[0].get('encrypt_key'))


@Then("I use Mac Restore Manager to restore the selected files by double clicking .mzd file")
def step_impl(context):
    Test_Data.clear_restore_folder('auto_restore')
    MacFryR_Controller.run_mzd()
    MacFryR_Controller.public_restore_flow()


@Then("I use Mac Restore Manager to decrypt the package by archive restore")
def step_impl(context):
    Test_Data.clear_restore_folder('auto_restore')
    MacFryR_Controller.launch_restore_manager()
    MacFryR_Controller.archive_restore()


@When('I launch MacFryr Client from GUI')
def step_impl(context):
    MacFryR_Controller.launch_restore_manager()


@When('I login MacFryr with current user')
def step_impl(context):
    username = context.user.username
    password = context.user.password
    MacFryR_Controller.login(username, password)


@When('I restore last mzd to directory "{output}"')
def step_impl(context, output):
    personal_key = context.user.pk or None
    MacFryR_Controller.run_mzd_restore(output, personal_key)


@When('I close Mac Fryr')
def step_impl(context):
    MacFryR_Controller.close_app()

@Then("I check the Mac restore job finished successfully")
def step_impl(context):
    assert (MacFryR_Controller.verify_restore_completed() == True)
    MacFryR_Controller.check_restore_files()
    MacFryR_Controller.close_app()

@Then("I use Mac Restore Manager to decrypt the file with personal key '{key_value}'")
def step_impl(context, key_value):
    Test_Data.clear_restore_folder('auto_restore')
    MacFryR_Controller.launch_restore_manager()
    MacFryR_Controller.decrypt_file(key_value)

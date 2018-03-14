from behave import *
from apps.fryr.win.winfryr_controller import WinFryR_Controller
from apps.fryr.win.winfryr_lsh_controller import WinFryR_LSH_Controller

@Then("I use Windows Restore Manager to restore the selected files with Useremail '{email}' and Password '{password}'")
def step_impl(context, email, password):
    WinFryR_Controller.clear_restore_folder('auto_restores')
    WinFryR_Controller.launch_restore_manager()
    WinFryR_Controller.login(email, password)
    WinFryR_Controller.restore_by_username()

@Then("I use Windows Restore Manager to restore the selected files by double clicking .mzd file")
def step_impl(context):
    WinFryR_Controller.clear_restore_folder('auto_restores')
    context.execute_steps(unicode('When I log WinFryr "MZD Restore" KPI start time'))
    WinFryR_Controller.restore_by_mzd()
    context.execute_steps(unicode('When I log WinFryr "MZD Restore" KPI end time'))

@Then("I check the restore job finished successfully")
def step_impl(context):
    assert (WinFryR_Controller.verify_restore_completed() == True)
    WinFryR_Controller.check_restore_files()
    WinFryR_Controller.close_app()

@Then("I use Windows Restore Manager to decrypt the package by archive restore")
def step_impl(context):
    WinFryR_Controller.clear_restore_folder('auto_restores')
    WinFryR_Controller.launch_restore_manager()
    context.execute_steps(unicode('When I log WinFryr "Archive Restore" KPI start time'))
    WinFryR_Controller.archive_restore()
    context.execute_steps(unicode('When I log WinFryr "Archive Restore" KPI end time'))

@Then("I use Windows Restore Manager to decrypt the file")
def step_impl(context):
    WinFryR_Controller.clear_restore_folder('auto_restores')
    WinFryR_Controller.launch_restore_manager()
    context.execute_steps(unicode('When I log WinFryr "Decrypt" KPI start time'))
    WinFryR_Controller.decrypt_file()
    context.execute_steps(unicode('When I log WinFryr "Decrypt" KPI end time'))

@Then("I use Windows Restore Manager to decrypt the folder '{folder_name}'")
def step_impl(context, folder_name):
    WinFryR_Controller.clear_restore_folder('auto_restores')
    WinFryR_Controller.launch_restore_manager()
    WinFryR_Controller.decrypt_folder(folder_name)

@Then("I check the decrypt job finished successfully")
def step_impl(context):
    assert (WinFryR_Controller.verify_restore_completed() == True)
    WinFryR_Controller.check_decrypted_files()
    WinFryR_Controller.close_app()

@When('I launch Windows Restore Manager from GUI')
def step_impl(context):
    WinFryR_Controller.launch_restore_manager()

@When('I login Windows Restore Manager with current user')
def step_impl(context):
    username = context.user.username
    password = context.user.password
    context.execute_steps(unicode('When I log WinFryr "Login" KPI start time'))
    WinFryR_Controller.login(username, password)
    context.execute_steps(unicode('When I log WinFryr "Login" KPI end time'))

@Then('I close Windows Restore Manager from GUI')
def step_impl(context):
    WinFryR_Controller.close_app()

@Then('I use Windows Restore Manager to export files from the .mzdx seed')
def step_impl(context):
    WinFryR_LSH_Controller.clear_restore_folder('auto_restores')
    WinFryR_LSH_Controller.restore_by_mzdx()

@Then('I kick off an export job without waiting for it completed')
def step_impl(context):
    WinFryR_LSH_Controller.clear_restore_folder('auto_restores')
    WinFryR_LSH_Controller.restore_by_mzdx(wait_for_export_completed=False)

@Then('I use Windows Restore Manager to add an export job in queue')
def step_impl(context):
    WinFryR_LSH_Controller.add_queue_job()

@When('I clear database folder of Mozy Restore Manager')
def step_impl(context):
    WinFryR_LSH_Controller.delete_all_jobs()

@Then("I verify the export job status is '{job_status}'")
def step_impl(context, job_status):
    actual_job_status = WinFryR_LSH_Controller.get_job_status()
    assert actual_job_status == job_status

@Then("I expand action panel and click '{command}' button to job '{job_name}'")
def step_impl(context, command, job_name):
    if job_name == 'default job':
        WinFryR_LSH_Controller.click_action_panel(command)
    else:
        WinFryR_LSH_Controller.click_action_panel(command, job_name)

@Then("I export EDRM file with version '{edrm_version}'")
def step_impl(context, edrm_version):
    WinFryR_LSH_Controller.export_edrm(version=edrm_version)

@Then('I archive the export job and check it in archived job list')
def step_impl(context):
    WinFryR_LSH_Controller.return_to_job_list()
    WinFryR_LSH_Controller.archive_job()

@Then('I close LSH Windows Restore Manager from GUI')
def step_impl(context):
    WinFryR_LSH_Controller.close_app()

@Then('I verify the confirm dialog will display about the cancel action and click action button')
def step_impl(context):
    WinFryR_LSH_Controller.check_message(context.table[0].get('message'))
    WinFryR_LSH_Controller.confirm_quit(context.table[0].get('action'))
from behave import *
from apps.fryr.test_data import Test_Data
from apps.web_support.bus_page import BusPage
from apps.web_support.dashboard import DashboardPage
from apps.web_support.freyja_page import FreyjaPage
from apps.web_support.machine_page import MachinePage
from apps.web_support.bus_report_builder import BusReportBuilderPage
from apps.web_support.bus_add_new_pro_plan import BusAddNewProPlanPage
from apps.web_support.bus_add_new_role import BusAddNewRolePage


@When('I log in BUS console')
def step_impl(context):
    BusPage.openbrowser()
    BusPage.visit()
    BusPage.login()

@When('I navigate to Dashboard')
def step_impl(context):
    DashboardPage.visit()
    BusPage.start_use_mozy()

@When('I log in BUS console to select my restore machine')
def step_impl(context):
    context.execute_steps(unicode('When I log in BUS console'))

    # useremail = context.user.name or ""
    # if context.table == None:
    #     pass
    # else:
    #     if context.table[0].get('user_email'):
    #         useremail = context.table[0].get('user_email')
    if context.table[0].get('user_email'):
        useremail = context.table[0].get('user_email')
    BusPage.search_user(useremail)
    BusPage.select_folder()

@Then('I navigate to Freyja page to request a mzd restore')
def step_impl(context):
    Test_Data.clear_download_folder()
    FreyjaPage.select_restore(context.table)
    FreyjaPage.create_mzd()
    FreyjaPage.close_browser()


@Then('I navigate to Freyja page to request an archive restore')
def step_impl(context):
    Test_Data.clear_download_folder()
    FreyjaPage.select_restore(context.table)
    FreyjaPage.create_archive()
    FreyjaPage.close_browser()

@Then('I navigate to Freyja page to download an encrypted file/folder directly')
def step_impl(context):
    Test_Data.clear_download_folder()
    FreyjaPage.direct_download(context.table)
    FreyjaPage.close_browser()

@Then('I navigate to Freyja page to request to search and export files')
def step_impl(context):
    BusPage.go_to_eDiscovery()
    Test_Data.clear_download_folder()
    FreyjaPage.define_lsh_search(context.table[0].get('keyword'))
    FreyjaPage.create_mzdx()
    FreyjaPage.close_browser()

@When('I visit cas host to be authenticated to do direct download from freyja site')
def step_impl(context):
    #context.execute_steps(unicode('When I log web "CAS Response" KPI start time'))
    BusPage.visit_cas()
    #context.execute_steps(unicode('When I log web "CAS Response" KPI end time'))


@Then("I delete all files in '{product_name}' installer folder")
def step_impl(context, product_name):
    Test_Data.clear_installer_folder(product_name)

@When('I log in BUS console to select my partner info')
def step_impl(context):
    context.execute_steps(unicode('When I log in BUS console'))

    BusPage.search_partner(context.table[0].get('partner name'))
    BusPage.act_as_partner()

@When('I act as partner')
def step_impl(context):
    # Goto Dashboard Page directly
    DashboardPage.visit()

    BusPage.search_partner(context.table[0].get('partner name'))
    BusPage.act_as_partner()

@When('I add a new pro plan for the partner')
def step_impl(context):
    for row in context.table:
        name = row.get('name') or "default"
        periods = row.get('periods') or "monthly"
        server_license_price = row.get('server licenses price') or "1"
        server_min_licenses = row.get('server min licenses') or "1"
        server_quota_price = row.get('server quota price') or "1"
        server_min_quota = row.get('server min quota') or "1"
        desktop_license_price = row.get('desktop licenses price') or "1"
        desktop_min_licenses = row.get('desktop min licenses') or "1"
        desktop_quota_price = row.get('desktop quota price') or "1"
        desktop_min_quota = row.get('desktop min quota') or "1"
        BusAddNewProPlanPage.create_proplan(name,periods,server_license_price,server_min_licenses,server_quota_price,server_min_quota,desktop_license_price,desktop_min_licenses,desktop_quota_price,desktop_min_quota)

@When('I add a new role for the partner')
def step_impl(context):
    for row in context.table:
        name = row.get('name') or "default"
        include_all = False
        if row.get('include all') and str(row.get('include all')) == "true":
            include_all = True
        BusAddNewRolePage.create_role(name,include_all=include_all)
        context.root_role_id = BusAddNewRolePage.get_role_id(name)
        BusPage.quit()

@When('I create a new client config and uncheck backup set')
def step_impl(context):
    BusPage.click_client_configuration()
    BusPage.find_or_create_client_configuration(context.table[0].get('name'), context.table[0].get('type'))
    BusPage.uncheck_all_backup_sets(context.table[0].get('backup sets'))
    if context.table[0].get('user group'):
        BusPage.assign_user_group_to_configuration(context.table[0].get('user group'))
    BusPage.save_client_configuration()
    BusPage.quit()

@Then('I create a report')
def step_impl(context):
    BusReportBuilderPage(BusPage.bus_driver).create_report(context.table[0].get('report type'))
    BusReportBuilderPage(BusPage.bus_driver).save_report(context.table[0].get('report name'))
    BusPage.quit()

@When('I create client config with')
def step_impl(context):
    context.multiencryption = False
    if context.table[0].get('multi_encryption'):
        context.multiencryption = True

    BusPage.click_client_configuration()

    BusPage.find_or_create_client_configuration(context.table[0].get('name'), context.table[0].get('type'))

    if context.table[0].get('encryption'):
        # BusPage.switch_to_tab("Preferences")
        BusPage.choose_encryption(context.table[0].get('encryption'))

    BusPage.uncheck_all_backup_sets(context.table[0].get('backup sets'))

    if context.table[0].get('user group'):
        BusPage.assign_user_group_to_configuration(context.table[0].get('user group'))

    BusPage.save_client_configuration()
    # BusPage.quit()

@When ('I change encryption type in client config')
def step_impl(context):
    BusPage.click_client_configuration()

    BusPage.find_or_create_client_configuration(context.table[0].get('name'), context.table[0].get('type'))

    if context.table[0].get('encryption'):
        # BusPage.switch_to_tab("Preferences")
        BusPage.choose_encryption(context.table[0].get('encryption'))
        BusPage.enforce_encryption()

    BusPage.save_client_configuration()
    # BusPage.quit()

@Then ('Machine {machineid} is encrypted with {encryptiontype}')
def step_impl(context, machineid, encryptiontype):
    # BusPage.visit()
    # BusPage.login()
    MachinePage.visit(machineid)
    assert (MachinePage.validate_machine_ecnryption(encryptiontype) == True)
import os
from time import strftime, gmtime
import datetime

from behave import *

from apps.web_support.base_page import Page
from apps.web_support.bus_page import BusPage
from apps.web_support.freyja_page import FreyjaPage
from configuration.config_adapter import ConfigAdapter
from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.runner_config_loader import RUNNER_CONFIG

from lib.platformhelper import PlatformHelper
from lib.loghelper import LogHelper
from lib.kpi import KPI

@When('I access BUS console')
def step_impl(context):
    BusPage.openbrowser()

    # context.execute_steps(unicode('When I log web "BUS Login" KPI start time'))
    context.kpi = KPI(testcase=context.tc.name, category="Web",
                      start_time=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()),
                      name="BUS Login", result="Fail",
                      hostname=context.tc.machine_hostname, ip=context.tc.machine_ip, env=context.env)

    result = BusPage.visit()

    try:
        (result).should_not.be(False)
    except AssertionError:
        context.kpi.end_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
        context.kpi.result = "TIMEOUT"

        LogHelper.info(context.kpi.write_to_elasticsearch())
        context.kpi = None



@When('I log in BUS')
def step_impl(context):
    context.kpi = KPI(testcase=context.tc.name, category="Web",
                      start_time=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()),
                      name="BUS Login", result="Fail",
                      hostname=context.tc.machine_hostname, ip=context.tc.machine_ip, env=context.env)

    result = BusPage.visit()
    try:
        (result).should_not.be(False)
    except AssertionError:
        context.kpi.end_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
        context.kpi.message = "Can't access BUS."

        context.kpi.write_to_elasticsearch(context.senddb)
        context.kpi = None
        Page.quit()
    else:
        env = RUNNER_CONFIG.get('ENVIRONMENT') or 'QA12'
        username = GLOBAL_CONFIG.get('QA_ENVIRONMENT').get(env).get('bus_admin')
        password = GLOBAL_CONFIG.get('QA_ENVIRONMENT').get(env).get('bus_admin_password')
        result = BusPage.login(username, password)
        try:
            (result).should.be(True)
        except AssertionError:
            context.kpi.message = "Fail to Login BUS."
            Page.quit()
        else:
            context.kpi.result = "SUCCESS"
        finally:
            context.kpi.end_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
            context.kpi.write_to_elasticsearch(context.senddb)
            context.kpi = None

@When('I search current user')
def step_impl(context):
    username = context.user.username or "nathan+pro+qa12@mozy.com"
    LogHelper.info('Search User %s' %username)
    # context.execute_steps(unicode('When I log web "BUS Search User" KPI start time'))
    context.kpi = KPI(testcase=context.tc.name, category="Web",
                      start_time=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()),
                      name="BUS Search User", result="Fail",
                      hostname=context.tc.machine_hostname, ip=context.tc.machine_ip, env=context.env)
    result = BusPage.search_user(username)
    try:
        (result).should.be(True)
    except AssertionError:
        context.kpi.message = "Fail to search user."
        Page.quit()
    else:
        context.kpi.result = "SUCCESS"
    finally:
        context.kpi.end_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
        context.kpi.write_to_elasticsearch(context.senddb)
        context.kpi = None


@When('I view machine list')
def step_impl(context):
    context.kpi = KPI(testcase=context.tc.name, category="Web",
                      start_time=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()),
                      name="Frejya Response", result="Fail",
                      hostname=context.tc.machine_hostname, ip=context.tc.machine_ip, env=context.env)

    result = BusPage.go_to_freya()

    try:
        (result).should.be(True)
    except AssertionError:
        context.kpi.message = "Fail to open Freyja."
        Page.quit()
    else:
        context.kpi.result = "SUCCESS"
    finally:
        context.kpi.end_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
        context.kpi.write_to_elasticsearch(context.senddb)
        context.kpi = None


@When('I view current user machine details')
def step_impl(context):
    context.execute_steps(unicode("When I search current user"))
    context.execute_steps(unicode("When I view machine list"))


@When('I logon Freyja through BUS console')
def step_impl(context):
    context.execute_steps(unicode("When I log in BUS"))
    context.execute_steps(unicode("When I wait 5 seconds"))
    context.execute_steps(unicode("When I search current user"))
    context.execute_steps(unicode("When I view machine list"))


@When('I click backup files for current machine')
def step_impl(context):
    host = PlatformHelper.get_hostname().upper()

    context.kpi = KPI(testcase=context.tc.name, category="Web",
                      start_time=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()),
                      name="Frejya View Machine", result="Fail",
                      hostname=context.tc.machine_hostname, ip=context.tc.machine_ip, env=context.env)

    result = FreyjaPage.click_machine(host)

    try:
        (result).should.be(True)
    except AssertionError:
        context.kpi.message = "Frejya fail to view machine."
        FreyjaPage.quit()
    else:
        context.kpi.result = "SUCCESS"
    finally:
        context.kpi.end_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
        context.kpi.write_to_elasticsearch(context.senddb)
        context.kpi = None
    context.execute_steps(unicode("When I wait 5 seconds"))


@When('I select below files to generate mzd')
def step_impl(context):
    #Generate dir full path
    LogHelper.info('Generate directory full path')
    root = ConfigAdapter.get_testdata_path()
    for row in context.table:
        dir_name = row.get('entity')
        full_path = os.path.join(root, dir_name)
        #remve unwanted empty string
        drill_down_list = filter(lambda x: len(x) > 0, full_path.split(os.path.sep))
        if RUNNER_CONFIG.get('PRODUCT').upper() in ('MAC', "LINUX", 'MAC_MACFRYR'):
            drill_down_list.insert(0, os.path.sep)

        # Drill down folders
        result = FreyjaPage.drill_down_folders(drill_down_list[0:-1])
        try:
            (result).should.be(True)
        except AssertionError:
            LogHelper.error("Frejya fail to Expand folder.")
            FreyjaPage.quit()
        else:
            # Select folder checkbox
            result = FreyjaPage.check_entity(full_path)
            try:
                (result).should.be(True)
            except AssertionError:
                LogHelper.error("Frejya fail to check folder checkbox.")
                FreyjaPage.quit()

            else:
                context.kpi = KPI(testcase=context.tc.name, category="Web",
                                  start_time=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()),
                                  name="Frejya Create MZD", result="Fail",
                                  hostname=context.tc.machine_hostname, ip=context.tc.machine_ip, env=context.env)

                result = FreyjaPage.create_mzd()
                try:
                    (result).should.be(True)
                except AssertionError:
                    context.kpi.message = "Frejya fail to create MZD."
                    FreyjaPage.quit()
                else:
                    context.kpi.result = "SUCCESS"
                finally:
                    context.kpi.end_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
                    context.kpi.write_to_elasticsearch(context.senddb)
                    context.kpi = None
                    Page.quit()


@When('I select below files to direct download')
def step_impl(context):
    #Generate dir full path
    LogHelper.info('Generate directory full path')
    root = ConfigAdapter.get_testdata_path()
    for row in context.table:
        dir_name = row.get('entity')
        full_path = os.path.join(root, dir_name)
        #remve unwanted empty string
        drill_down_list = filter(lambda x: len(x) > 0, full_path.split(os.path.sep))
        if RUNNER_CONFIG.get('PRODUCT').upper() in ('MAC', "LINUX", 'MAC_MACFRYR'):
            drill_down_list.insert(0, os.path.sep)

        try:
            starttime = datetime.datetime.now()
            result = FreyjaPage.drill_down_folders(drill_down_list[0:-1])
            endtime = datetime.datetime.now()
            expand_folder_time = (endtime - starttime).seconds

            context.kpi = KPI(testcase=context.tc.name, category="Web",
                              start_time=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()),
                              name="Frejya Direct Download", result="Fail",
                              message="Expand file: %s" % expand_folder_time,
                              hostname=context.tc.machine_hostname, ip=context.tc.machine_ip, env=context.env)
            LogHelper.info("Expand file complete.")
            (result).should.be(True)
        except AssertionError:
            context.kpi.write_to_elasticsearch(context.senddb)
            FreyjaPage.quit()

        else:
            cb_target = '//tr[contains(@id, "{entity_name}")]//span[contains(@class, "check")]'.format(entity_name=drill_down_list[-1])
            FreyjaPage.locate_element(cb_target, 30).click()

            #FreyjaPage.check_entity(drill_down_list[-1])
            # context.execute_steps(unicode('When I log web "Frejya Direct Download" KPI start time'))

            context.kpi = KPI(testcase=context.tc.name, category="Web",
                              start_time=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()),
                              name="Frejya Direct Download", result="Fail",
                              hostname=context.tc.machine_hostname, ip=context.tc.machine_ip, env=context.env)
            result = FreyjaPage.download_now()

            try:
                (result).should.be(True)
            except AssertionError:
                context.kpi.message = "Frejya fail to direct download."
            else:
                context.kpi.result = "SUCCESS"
            finally:
                context.kpi.end_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
                context.kpi.write_to_elasticsearch(context.senddb)
                context.kpi = None
                Page.quit()


@When('I select below files to generate tarball')
def generate_tarball(context):
    LogHelper.info('Generate directory full path')
    root = ConfigAdapter.get_testdata_path()
    for row in context.table:
        dir_name = row.get('entity')
        full_path = os.path.join(root, dir_name)
        # remve unwanted empty string
        drill_down_list = filter(lambda x: len(x) > 0, full_path.split(os.path.sep))
        if RUNNER_CONFIG.get('PRODUCT').upper() in ('MAC', "LINUX", 'MAC_MACFRYR'):
            drill_down_list.insert(0, os.path.sep)

        result = FreyjaPage.drill_down_folders(drill_down_list[0:-1])
        try:
            (result).should.be(True)
        except AssertionError:
            LogHelper.error("Frejya fail to Expand folder.")
            FreyjaPage.quit()
            #FreyjaPage.check_entity(drill_down_list[-1])

        else:
            result = FreyjaPage.check_entity(full_path)
            try:
                (result).should.be(True)
            except AssertionError:
                LogHelper.error("Frejya fail to select folder checkbox.")
                FreyjaPage.quit()

            else:
                context.kpi = KPI(testcase=context.tc.name, category="Web",
                                  start_time=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()),
                                  name="Frejya Create Archive", result="Fail",
                                  hostname=context.tc.machine_hostname, ip=context.tc.machine_ip, env=context.env)

                result = FreyjaPage.create_archive()
                try:
                    (result).should.be(True)
                except AssertionError:
                    context.kpi.message = "Frejya fail to create archive."
                    FreyjaPage.quit()
                else:
                    context.kpi.result = "SUCCESS"
                finally:
                    context.kpi.end_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
                    context.kpi.write_to_elasticsearch(context.senddb)
                    context.kpi = None
                    Page.quit()




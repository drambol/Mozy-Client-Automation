
import os
import sure

from behave import *

from apps.linux.linuxclient import LinuxClient
from configuration.runner_config_loader import RUNNER_CONFIG
from lib.loghelper import LogHelper
from lib.filehelper import FileHelper


@When('I restart Linux Client')
def step_impl(context):
    LinuxClient().controller.restart()
    context.execute_steps(u"""When I wait for sock ready""")


@When('Linux Client is not installed')
def step_impl(context):
    if LinuxClient().controller.is_client_installed():
        LogHelper.info('Linux Client is installed, uninstall Linux Client')
        LinuxClient().installer.create().uninstall()
    is_uninstalled = LinuxClient().controller.is_client_installed()
    LogHelper.info("Check Whether Linux Client uninstalled successfully")
    try:
        is_uninstalled.should.equal(False)
    except AssertionError as e:
        LogHelper.error(e.message)
        raise e


@When('I install linux client with')
def step_impl(context):

    if context.table.rows[0].get('job'):
        jenkins_job =context.table.rows[0]['job']
    else:
        jenkins_job = 'lynx'
    LogHelper.info("jenkin job is %s" %jenkins_job)

    if context.table.rows[0].get('build'):
        build = int(context.table.rows[0]['build'])
    else:
        build = -1

    if context.table.rows[0].get('oem'):
        oem = context.table.rows[0]['oem']
    else:
        oem = 'mozypro'

    LinuxClient().installer.download_and_install(build, job=jenkins_job, pattern=oem)


@Then('Linux Client should be installed')
def step_impl(context):
    is_installed = LinuxClient().controller.is_client_installed()
    LogHelper.info("Check Whether Linux Client Installed successfully")
    try:
        is_installed.should.equal(True)
    except AssertionError as e:
        LogHelper.error(e.message)
        raise e


@Then('I setup environment')
@When('I setup environment')
def step_impl(context):
    environment = RUNNER_CONFIG.get('ENVIRONMENT') or 'QA12'
    LogHelper.info('setup environment')
    LinuxClient().controller.prepare_environment(environment)


@When('I cleanup local {db} database')
def step_impl(context, db):
    database_dir = LinuxClient().controller.config_db_dir

    state_db = os.path.join(database_dir,LinuxClient().controller.state_database)

    if FileHelper.file_exist(state_db):
        FileHelper.delete_file(state_db)
    metric_db =  os.path.join(database_dir,LinuxClient().controller.metrics_database)
    if FileHelper.file_exist(metric_db):
        FileHelper.delete_file(metric_db)
    # config_db = LinuxClient().controller.config_database
    # if FileHelper.file_exist(config_db):
    #     FileHelper.delete_file(config_db)

    context.execute_steps(unicode('When I restart Linux Client'))


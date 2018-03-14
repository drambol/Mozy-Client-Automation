import os
import hashlib
import behave
from time import strftime, gmtime, localtime
from behave.log_capture import capture
from lib.testcase import TestCase
from lib.platformhelper import PlatformHelper
from lib.loghelper import LogHelper
from lib.filehelper import FileHelper
from lib.cmdhelper import CmdHelper
from lib.kpihelper import KPIHelper

from configuration.runner_config_loader import RUNNER_CONFIG
from configuration.config_adapter import ConfigAdapter

from apps.nativeclient import NativeClientFactory
from apps.mac.mac_cli_client.mac_cli_client import MacCliClient
from apps.mac.mac_controller.mac_controller import MacController


def before_scenario(context, scenario):

    testrun = RUNNER_CONFIG.get('TESTRUN') or 'testrun'
    context.log_starttime = strftime("%Y-%m-%dT%H:%M:%SZ", localtime())
    start_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    hostname = PlatformHelper.get_hostname()
    ip = PlatformHelper.get_ip_address()

    product = RUNNER_CONFIG.get("PRODUCT")
    build = RUNNER_CONFIG.get('BUILD')
    context.senddb = RUNNER_CONFIG.get('DATABASE_ENABLED')
    context.env = RUNNER_CONFIG.get('ENVIRONMENT')

    logger_path = os.path.join(ConfigAdapter.get_log_path(), testrun)
    tc_prefix = ConfigAdapter.get_testlink_prefix(product)

    match = filter(lambda x: x.find(tc_prefix) >= 0, scenario.tags)

    if len(match)>0:
        # differentiate scenarios in scenario outline
        if hasattr(context, 'active_outline') and type(context.active_outline) == behave.model.Row:
            suffix = match.pop()
            for example_key in context.active_outline:
                suffix += ".%s" % (example_key)
            tc_id = testrun + "_" + suffix
        else:
            tc_id = testrun + "_" + match.pop()
    else:
        #no test link project id foud
        tc_id = hashlib.md5(testrun + "_" + scenario.name.encode()).hexdigest()

    if not FileHelper.dir_exist(logger_path):
        FileHelper.create_directory(logger_path)
    logger_filename = "%s.log" % (tc_id)
    logfile = os.path.join(logger_path, logger_filename)

    client_ip = PlatformHelper.get_ip_address()

    LogHelper.create_logger(logfile, fmt=client_ip+" %(asctime)s %(levelname)s " + product+" | %(message)s |")

    tc = TestCase(testrun=testrun, start_time=start_time, hostname=hostname, product=product,
                  ip=ip, summary=scenario.name, feature=scenario.filename, tags=scenario.tags, logfile=logfile, _id=tc_id, build=build)
    context.tc = tc

    LogHelper.info("test start: " + scenario.name)

@capture()
def after_scenario(context, scenario):
    context.tc.end_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    context.tc.duration = int(scenario.duration)
    context.tc.test_result = scenario.status

    if context.senddb:

        if not (RUNNER_CONFIG.get("PRODUCT") or '').lower() == 'mts':
            native_client = NativeClientFactory.get_client(product=RUNNER_CONFIG.get("PRODUCT"),
                                                           oem=RUNNER_CONFIG.get("OEM_CLIENT"))

            KPIHelper.testcase = context.tc.name
            KPIHelper.extract_kpi(native_client.controller.log, starttime=context.log_starttime, hostname=context.tc.machine_hostname, ip=context.tc.machine_ip, env=context.env)

        if "-" in KPIHelper.thost:
            context.tc.thost = KPIHelper.thost.split("-")[1]     # tds06-ut4.triton.mozy.com
        else:
            context.tc.thost = KPIHelper.thost        # ut4.triton.mozy.com

        context.tc.write_to_elasticsearch()

    log = context.log_capture
    for line in log.getvalue().splitlines():
        if line.find("ERROR") >=0:
            LogHelper.error(line)




def before_step(context, step):
    context.start_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    LogHelper.info("step start %s" % step)

def after_step(context,step):
    context.end_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    #end_time = strptime(context.end_time, "%Y-%m-%dT%H:%M:%SZ")
    #start_time = strptime(context.start_time, "%Y-%m-%dT%H:%M:%SZ")
    #step_duration = int(end_time - start_time)
    #LogHelper.info("step finished at %s" % context.end_time)



def before_tag(context, tag):
    if tag == "cleanup":
        testdata = ConfigAdapter.get_testdata_path()
        output = ConfigAdapter.get_output_path()
        installer_path = ConfigAdapter.get_installer_path()
        FileHelper.delete_directory(testdata)
        FileHelper.delete_directory(output)
        FileHelper.delete_directory(installer_path)

    if tag == "cleandownload":
        downloadpath = ConfigAdapter.get_output_path()
        FileHelper.delete_directory(downloadpath)

    if tag == "mac_setup":
        MacCliClient().rule_cmd.remove_all_rules()
        MacController().restart_mozypro_pid()


def after_tag(context, tag):
    if tag == "mac_teardown":
        cmd = str('''osascript -e 'tell application "System Preferences" to quit' ''')
        output = CmdHelper.run(cmd)
        LogHelper.info(output)
        # cmd = str('''osascript -e 'tell application "MozyPro Restore" to quit' ''')
        # output = CmdHelper.run(cmd)

    if tag.lower() == 'web_teardown':
        pass

    if tag.lower() == 'macfryr_teardown':
        cmd = str('sudo pkill "Mozy Restore Manager"')
        output = CmdHelper.run(cmd)
        LogHelper.info(output)

    if tag.lower() == 'winfryr_teardown':
        close_fryr = 'taskkill /F /IM MozyRestoreManager.exe'
        output = CmdHelper.run(close_fryr)
        LogHelper.info(output)
        close_ff = 'taskkill /F /IM firefox.exe'
        output = CmdHelper.run(close_ff)
        LogHelper.info(output)

    if tag.lower() == 'winfryr_lsh_teardown':
        close_lsh_fryr = 'taskkill /F /IM MozyLshRestoreManager.exe'
        try:
            output = CmdHelper.run(close_lsh_fryr)
        except Exception:
            LogHelper.info(output)

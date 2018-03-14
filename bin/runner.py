import os
import sys
import yaml
import time
import logging

lib_dir = os.path.abspath(os.path.join(os.path.dirname(__file__) + "/.."))
if lib_dir not in sys.path:
    sys.path.append(lib_dir)

from argparse import ArgumentParser
from apps.nativeclient import NativeClientFactory
from configuration.config_adapter import ConfigAdapter
from configuration.global_config_loader import GLOBAL_CONFIG
from lib.cmdhelper import CmdHelper
from lib.platformhelper import PlatformHelper
from lib.loghelper import LogHelper
from lib.jenkinshelper import JenkinsHelper
from lib.filehelper import FileHelper
from lib.celeryhelper import CeleryHelper
from lib.elasticsearchhelper import ElasticsearchHelper

from lib.testrun import TestRun

#from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

"""
This is the entry to execute behave testcase on worker,

1. Setup Client
    1.1 Download build from jenkins or www.mozy.com if build is not 0
    1.2 If build number is -1, download last stable build from jenkins
    1.3 install build
    1.4 Config Client to proper QA Testing environment
2. setup file beat
3. Write runner options to runner_config.yaml
4. Execute test case (include schedule)
"""

class upper(list):
    def __contains__(self, other):
        return super(upper,self).__contains__(other.upper())

opt = ArgumentParser(prog='PROG')

opt.add_argument('-p', "--product", dest="product", choices=upper(["LINUX", "MAC", "WINDOWS", "WINFRYR", "MACFRYR", "IOS", "ANDROID", "MAC_MACFRYR","WINDOWS_WINFRYR", "MTS"]),
               help="(Required) Product Name: windows, mac, linux, winfryr, macfryr, iOS, android, mac_macfryr, windows_winfryr, mts", required=True)

opt.add_argument('-f', '--features', dest="features", action="store", help="feature files filepath")

opt.add_argument('-o', "--oem_client", dest="oem_client",
               help="OEM Client: mozypro, MozyEnterprise, MozyHome, BDS, MozyNext",
               default="mozypro")

opt.add_argument('-j', "--jobname", dest="job", action="store", help="""where to download build,
                                                                      if jobname=product download build from www.mozy.com,
                                                                       else download job from jenkins job""")

opt.add_argument('-b', "--build", dest="build", action="store", help="""build number to install /n
                                                                    if not  specified, default to latest build""")

opt.add_argument('-d', "--database", dest="database_enabled", action="store_true",
               help="Write test result to database", default=False)

opt.add_argument("-u", "--run_by", dest="run_by", action="store", help="user name or email", default="clientqaautomation@emc.com")

opt.add_argument('-t', "--tags", dest="tags", help="tags")

opt.add_argument('-r', "--testrun", dest="testrun", action="store", help="test run name")

opt.add_argument("-e", "--environment", dest="environment", action="store", choices=upper(['QA12', 'STD1', 'STD2', 'PROD']), help="Environment: QA12, STD1, STD2, PROD",
               default="QA12")  # QA12_ENT

opt.add_argument("-l", "--language", dest="language", action="store", help="language")
opt.add_argument("--rerun", dest="rerun", action="store_true", default=False)
opt.add_argument("--taskid", dest="taskid", action="store")
opt.add_argument("--dry_run", dest="dry_run", action="store_true", help="dryrun automation", default=False)

auth_group = opt.add_argument_group('authentication')
auth_group.add_argument('-a', "--activate", choices=upper(['KEYLESS', 'KEYED', 'AUTO', 'ASSIST', 'FEDID']), help="Activate type: keyless, keyed, auto, assist, fedid", default="keyless")
auth_group.add_argument("-c", "--credential", dest="credential", action="store", help="credential")

opt.add_argument("-s", "--schedule", dest="schedule", choices=upper(['CRON', 'INTERVAL']), action="store", help="Trigger: Cron | Interval")

cron_schedule_group = opt.add_argument_group('cronjob')
cron_schedule_group.add_argument("-y", "-year", dest="year", type=int, action="store", help="4-digit year")
cron_schedule_group.add_argument("-m", "-month", dest="month", type=int, action="store", help="month (1-12)")
cron_schedule_group.add_argument("-day", "-day", dest="day", type=int, action="store", help="day of the (1-31)")
cron_schedule_group.add_argument("-w", "-week", dest="week", action="store", help="ISO week (1-53)")
cron_schedule_group.add_argument("-dayofweek", dest="dayofweek", action="store", help="number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)")
cron_schedule_group.add_argument("-hour", dest="hour", action="store", help="hour (0-23)")
cron_schedule_group.add_argument("-minute", dest="minute", action="store", help="minute (0-59)")
cron_schedule_group.add_argument("-second", dest="second", action="store", help="second (0-59)")

interval_schedule_group = opt.add_argument_group('intervaljob')
interval_schedule_group.add_argument("-waitweeks", type=int, dest="waitweeks", action="store", help="number of weeks to wait")
interval_schedule_group.add_argument("-waitdays", type=int, dest="waitdays", action="store", help="number of days to wait")
interval_schedule_group.add_argument("-waithours", type=int, dest="waithours", action="store", help="number of hours to wait")
interval_schedule_group.add_argument("-waitminutes", type=int, dest="waitminutes", action="store", help="number of minutes to wait")
interval_schedule_group.add_argument("-waitseconds", type=int, dest="waitseconds", action="store", help="number of seconds to wait")

opt.add_argument("-start_date", dest="start_date", action="store", help="earliest possible date/time to trigger on (inclusive)")
opt.add_argument("-end_date", dest="end_date", action="store", help="earliest possible date/time to trigger on (inclusive)")


options = opt.parse_args()
#opt.print_help()

product = options.product.upper()

oem_client = options.oem_client or 'mozypro'

build = options.build or None

job = options.job or None
if product in ("LINUX", "MAC", "WINDOWS", "WINFRYR", "MACFRYR", "IOS", "ANDROID") and build:
    build = int(build)
if product in ('MAC_MACFRYR', 'WINDOWS_WINFRYR') and build:
    # build = build.split('_')
    # build = map(lambda x: int(x), build)
    if build == '-1':
        build = [-1, -1]
    if len(build) != 2:
        opt.error("-b should specify two build number, example: -b xxx_xxx")
    if job:
        job = job.split('_')
        if len(job) != 2:
            opt.error("should specify two jobs,example: -j xxx_xxx")


features = options.features or None
if features is None:
    features = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "features", product.lower()))


environment = options.environment.upper()

start_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
testrun = options.testrun
if not testrun:
    id_timestamp = start_time.replace(":", "_").replace("-", "_")
    testrun = "%s_%s_%s_%s" % (options.product, options.oem_client, options.environment, id_timestamp)
    testrun = testrun.upper()
    options.testrun = testrun

scheduletype = options.schedule or None
waitweeks = options.waitweeks or 0
waitdays = options.waitdays or 0
waithours = options.waithours or 0
waitminutes = options.waitminutes or 0
waitseconds = options.waitseconds or 0


def verify_options():
    global environment, job, build, oem_client

    LogHelper.info("check jenkins job name")
    if job is None:
        LogHelper.info("jenkins job is not define")
        if product == 'WINDOWS':
            job = "kalypso-release"
        if product == 'MAC':
            job = "macmozy-release"
        if product == 'LINUX':
            job = "lynx"
        if product == 'ANDROID':
            job = "mozymobile-android-release"
        if product == 'WINFRYR':
            job = "winrestore-release"
        if product == 'MACFRYR':
            job = "macrestore-release"
        if product == 'WINDOWS_WINFRYR':
            job = ["kalypso-release", "winrestore-release"]
        if product == 'MAC_MACFRYR':
            job = ["macmozy-release", "macrestore-release"]
        LogHelper.info("jenkins job is %s" % job)

    if build == -1:
        LogHelper.info("get last stable build")
        jh = JenkinsHelper(GLOBAL_CONFIG["JENKINS"]["URL"], GLOBAL_CONFIG["JENKINS"]["USERNAME"],
                           GLOBAL_CONFIG["JENKINS"]["KEY"])
        build = jh.get_last_successful_build_number(job)
        LogHelper.info("use last stable build %s" % build)
        options.build = build

    #for end to end test case, if contains build -1
    if product in ('MAC_MACFRYR', 'WINDOWS_WINFRYR') and build:
        index = 0
        for app in job:
            if build[index] == -1:
                LogHelper.info("get last stable build")
                jh = JenkinsHelper(GLOBAL_CONFIG["JENKINS"]["URL"], GLOBAL_CONFIG["JENKINS"]["USERNAME"],
                                   GLOBAL_CONFIG["JENKINS"]["KEY"])
                actual_build = jh.get_last_successful_build_number(app)
                LogHelper.info("use last stable build %s" % actual_build)
                build[index] = actual_build
            index += 1

    environment = options.environment
    if environment in ("QA12", "STD1", "STD2", "PROD"):
        environment = options.environment
    else:
        environment = "QA12"
    LogHelper.info("environment is %s" % environment)


def create_runner_log():
    # ----create log files for runner-----
    logger_path = os.path.join(ConfigAdapter.get_log_path(), testrun)
    logfile = os.path.join(logger_path, "runner_logger.log")
    LogHelper.create_logger(logfile,
                            fmt=PlatformHelper.get_ip_address() + " %(asctime)s %(levelname)s " + product + " | %(message)s |")


def dump_options_to_config(filename="runner_config.yaml"):
    """
    dump options dict to a yaml file
    :return:
    """
    LogHelper.info("start to dump runner options to %s" % filename)
    if not filename.endswith(".yaml"):
        filename = filename + ".yaml"

    config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "configuration"))
    config_file = os.path.join(config_dir, filename)

    if FileHelper.file_exist(config_file):
        LogHelper.info("delete config file %s" % config_file)
        FileHelper.delete_file(config_file)

    data = dict((k.upper(), v) for k, v in options.__dict__.items())

    with open(config_file, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

def automation_listener(event):
    if event.exception:
        print('Current job is CRASHED.')
    else:
        print('Current job works correctly.')

def execute():
    # By default, run initial task
    run()
    # Then run schedule task if need
    if scheduletype is not None:
        start_schedule()

def start_schedule():
    # schedule = BackgroundScheduler()
    schedule = BlockingScheduler(timezone="Asia/Shanghai")

    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.INFO)  # DEBUG

    fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)

    if scheduletype.upper() == "INTERVAL":
        schedule.add_job(
            run,
            "interval",
            weeks = waitweeks,
            days = waitdays,
            hours = waithours,
            minutes = waitminutes,
            seconds = waitseconds,
            start_date = options.start_date,
            end_date = options.start_date
        )
    elif scheduletype.upper() == "CRON":
        schedule.add_job(
            run,
            "cron",
            year = options.year,
            month = options.month,
            week = options.week,
            day = options.day,
            day_of_week = options.dayofweek,
            hour = options.hour,
            minute = options.minute,
            second = options.second,
            start_date = options.start_date,
            end_date = options.end_date
        )

    # jobs = schedule.get_jobs()

    schedule.add_listener(automation_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    schedule.print_jobs()
    schedule.start()
    try:
        schedule.start()
    except (KeyboardInterrupt, SystemExit):
        schedule.shutdown()
        print('Exit Schedule Job!')


def run():
    if options.database_enabled:
        id = testrun.upper()+start_time.replace(":", "_").replace("-", "_")
        tr = TestRun(id, start_time, qa_env=options.environment,
                     build=options.build, client=options.product,
                     oem=options.oem_client,
                     branch=options.job, runby="clientqaautomation@emc.com")

        LogHelper.debug("Start to write TestRun to ES")
        tr.save_to_elasticsearch()
        LogHelper.debug("Finish to write TestRun to ES")

    create_runner_log()
    verify_options()
    if product == 'MAC_MACFRYR':
        LogHelper.debug("MAC_MACFRYR Test Case")
        mac_client = NativeClientFactory.get_client(product='MAC', oem=oem_client)
        if build:
            mac_client.installer.download_and_install(build[0], job[0])
        mac_client.controller.prepare_environment(environment)

        macfryr_client = NativeClientFactory.get_client(product='MACFRYR', oem=oem_client)
        if build:
            macfryr_client.installer.download_and_install(build[1], job[1])
        macfryr_client.controller.prepare_environment(environment)

        LogHelper.info('Install MacFryr Client')
        LogHelper.info('Prepare MacFryr Client Environment')

    elif product == 'WINDOWS_WINFRYR':
        LogHelper.debug("WINDOWS_WINFRYR Test Case")
        win_client = NativeClientFactory.get_client(product='WINDOWS', oem=oem_client)
        LogHelper.info('Load Configuration')
        if build:
            win_client.installer.download_and_install(build[0], job[0])
        win_client.controller.prepare_environment(environment)
        LogHelper.info('Install WINDOWS Client')
        LogHelper.info('Prepare WINDOWS Client Environment')

        winfryr_client = NativeClientFactory.get_client(product='WINFRYR', oem=oem_client)
        if build:
            winfryr_client.installer.download_and_install(build[1], job[1])
        winfryr_client.controller.prepare_environment(environment)
        LogHelper.info('Install WINFRYR Client')
        LogHelper.info('Prepare WINFRYR Client Environment')
    elif product == 'MTS':
        LogHelper.info("No need to install anything to test against MTS.")
    #TODO
    else:
        LogHelper.info("Standalone app ")
        native_client = NativeClientFactory.get_client(product=product, oem=oem_client)
        if build:
            native_client.installer.download_and_install(build, job)
        native_client.controller.prepare_environment(environment)

    dump_options_to_config()

    if options.taskid:
        print ("update task record after execution")
        CeleryHelper.update_task_status(options.taskid, testrun, result='STARTED')

    behave_cmd = "behave %s --no-capture --no-capture-stderr" % features
    LogHelper.info(behave_cmd)
    if options.tags:
        behave_cmd += " --tags %s" %(options.tags)

    dry_run = options.dry_run
    if dry_run:
            behave_cmd += ' --dry-run'

    output = CmdHelper.run(behave_cmd)
    print output

    if options.database_enabled:
        # TestRun Finish.
        tr.end_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        tr.save_to_elasticsearch()


    rerun_failed = options.rerun
    if rerun_failed and FileHelper.file_exist("rerun_failing.features"):
        LogHelper.info('Rerun failed feature')
        behave_cmd = "behave @rerun_failing.features"
    	behave_output = CmdHelper.run(behave_cmd)
    	print behave_output


    final_result = 'COMPLETED'
    if options.taskid:
        LogHelper.debug("update task status in databsae")
        CeleryHelper.update_task_status(options.taskid, testrun, result=final_result)
        time.sleep(2)
        LogHelper.debug("check testrun status")
        query_body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "testrun_id": testrun
                            }
                        }
                    ],
                    "must_not": [
                        {
                            "match": {
                                "status": final_result
                            }
                        }
                    ]
                }
            }
        }

        result = ElasticsearchHelper().search_document(index='task', doc_type='task', body=query_body)
        uncompleted_tasks = result.get('hits').get('total')
        LogHelper.debug("%d tasks is uncompleted" % uncompleted_tasks)
        if uncompleted_tasks == 0:
            print "all tasks are completed"
            LogHelper.debug("all tasks are done for testrun %s" % testrun)
            output = CeleryHelper.detach_from_queue(testrun)
            print output
            LogHelper.debug(output)

execute()






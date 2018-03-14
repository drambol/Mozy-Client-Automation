import os, sys
import time
import re

from argparse import ArgumentParser

lib_dir = os.path.abspath(os.path.join(os.path.dirname(__file__) + "/.."))
if lib_dir not in sys.path:
    sys.path.append(lib_dir)


from configuration.config_adapter import ConfigAdapter
from lib.filehelper import FileHelper
from lib.platformhelper import PlatformHelper
from lib.testrun import TestRun
from lib.loghelper import LogHelper
from lib.celeryhelper import CeleryHelper


"""
This is the entry to create request, send the simple executable task to coordinator(broker)

1. Generate testrun
2. Prepare simple task include testrun info
3. Send the task to coordinator
4. Finialize testrun

"""
class upper(list):
    def __contains__(self, other):
        return super(upper,self).__contains__(other.upper())

opt = ArgumentParser(prog='PROG')


opt.add_argument('-p', "--product", dest="product", choices=upper(["LINUX", "MAC", "WINDOWS", "WINFRYR", "MACFRYR", "IOS", "ANDROID", "MAC_MACFRYR","WINDOWS_WINFRYR","MTS"]),
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

#Platform matcher -m
opt.add_argument("-m", "--machines", dest="machines", action="store", help="machines: select machines to run automation")

opt.add_argument('-x', '--dry_run', dest="dry_run", action='store_true', help='dryrun automation', default=False)


opt.add_argument("-s", "--schedule", dest="schedule", choices=upper(['CRON', 'INTERVAL']), action="store", help="Trigger: Cron | Interval")

cron_schedule_group = opt.add_argument_group('cronjob')
cron_schedule_group.add_argument("-year", dest="year", type=int, action="store", help="4-digit year")
cron_schedule_group.add_argument("-month", dest="month", type=int, action="store", help="month (1-12)")
cron_schedule_group.add_argument("-day", dest="day", type=int, action="store", help="day of the (1-31)")
cron_schedule_group.add_argument("-week", dest="week", action="store", help="ISO week (1-53)")
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


options = opt.parse_args()
# opt.print_help()


# Parse Product parameter
product = options.product.upper()

oem_client = options.oem_client or 'mozypro'

build = options.build or None

job = options.job or None
if product in ("LINUX", "MAC", "WINDOWS", "WINFRYR", "MACFRYR", "IOS", "ANDROID") and build:
    build = int(build)
if product in ('MAC_MACFRYR', 'WINDOWS_WINFRYR') and build:
    build = build.split('_')
    build = map(lambda x: int(x), build)
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


sendtodb = options.database_enabled

scheduletype = options.schedule or None
year = options.year or 2017
month = options.month or 1
week = options.week or 1
day = options.day or 1
dayofweek = options.dayofweek or 0
hour = options.hour or 0
minute = options.minute or 0
second = options.second or 0

waitweeks = options.waitweeks or 0
waitdays = options.waitdays or 0
waithours = options.waithours or 0
waitminutes = options.waitminutes or 0
waitseconds = options.waitseconds or 0


dry_run = options.dry_run

machines = options.machines
if not machines:
    #Machine is not select
    if product.upper() in ("LINUX", "MAC", "WINDOWS"):
        machines = product.upper()
    if product.upper() in ("WINFRYR", "ANDROID"):
        machines = 'WINDOWS'
    if product.upper() in ("MACFRYR", "IOS"):
        machines = 'MAC'
else:
    machines = machines.upper()


def prepare_testrun(senddb=False):
    start_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    id_timestamp = start_time.replace(":","_").replace("-","_")
    if options.testrun:
        id = "%s_%s" % (options.testrun, id_timestamp)
    else:
        id = "%s_%s_%s_%s" % (options.product, options.oem_client, options.environment, id_timestamp)

    id = id.upper()

    tr = TestRun(id, start_time, qa_env=options.environment,
                 build=options.build, client=options.product, oem=options.oem_client,
                 branch=options.job, runby="clientqaautomation@emc.com")

    if senddb:
        LogHelper.debug("Start to write TestRun to ES")
        tr.save_to_elasticsearch()
        LogHelper.debug("Finish to write TestRun to ES")

    return tr


def parse_feature(features, pattern="*.feature"):
    testfeatures = []
    if FileHelper.file_exist(features) and FileHelper.file_ext(features) == "feature":
        testfeatures.append(features)
    else:
        files = FileHelper.find_file(features, pattern)
        # TODO: refine with FileHelper
        for file in files:
            testfeatures.append("features" + file.split("features")[1])
    return testfeatures

# features = options.features or None
# if features is None:
#     features = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "features", product.lower()))

def run():
    tr = prepare_testrun(sendtodb)

    logger_path = ConfigAdapter.get_log_path()
    logfile = os.path.join(logger_path, tr.id, "tasks_logger.log")
    LogHelper.create_logger(logfile,
                            fmt=PlatformHelper.get_ip_address() + " %(asctime)s %(levelname)s " + product + " | %(message)s |")

    # select workers based on machine parameter

    LogHelper.debug("list all online workers")
    # online_workers = CeleryHelper.get_online_workers()
    # online_workers = CeleryHelper.inspect_active_queues()
    online_workers = CeleryHelper.inspect_active_workers()
    LogHelper.debug(';'.join(online_workers))
    print "online workers \n {0}".format("\n".join(online_workers))
    selected_workers = []
    LogHelper.debug('setup workers')
    worker_setup_queue = 'worker_setup'
    automation_queue = tr.id

    for worker in online_workers:
        CeleryHelper.add_worker(worker_name=worker, queue_name=worker_setup_queue)
        worker_info = CeleryHelper.run_task('worker_setup', worker_name=worker, queue=worker_setup_queue).get()
        result = CeleryHelper.delete_worker(worker_name=worker, queue_name=worker_setup_queue)
        LogHelper.debug('delete worker result %s' % result)
        LogHelper.debug('checking working {0}'.format(worker_info['WORKER_NAME']))
        worker_raw_info = '{os}_{os_version}_{worker_name}_{hostname}_{ip}'.format(os=worker_info.get('OS'),
                                                                                   os_version=worker_info.get('OS_VERSION'),
                                                                                   worker_name=worker_info.get('WORKER_NAME'),
                                                                                   hostname=worker_info.get('HOSTNAME'),
                                                                                   ip=worker_info.get('IP')
                                                                                   )

        LogHelper.debug('worker machine info data is: %s' % worker_raw_info)
        machine_pattern = re.compile(machines, flags=re.IGNORECASE)
        if re.search(machine_pattern, worker_raw_info):
            LogHelper.info("worker: {0} is selected for test agent".format(worker))
            output = CeleryHelper.add_worker(worker, queue_name=automation_queue)
            LogHelper.debug(output)
            selected_workers.append(worker)

    if len(selected_workers) == 0:
        print "ERROR: NO available workers matched!!!!!"
        print "Please recheck machine option argument"
        exit(1)

    LogHelper.debug('select workers: %s' % selected_workers)
    print "selected workers \n {0}".format("\n".join(selected_workers))

    LogHelper.debug("Prepare tasks")
    LogHelper.debug(str(options))
    features = parse_feature(options.features)

    print "start to run automation: %s" % tr.id
    if len(features) < 1:
        print "no feature file"
        LogHelper.error("There is no test feature to be executed.")
        exit(1)
    else:
        task_obj_list = []
        for feature in features:
            feature_name = feature.split('/').pop().replace('.', '_')
            task_id = '{0}_{1}'.format(tr.id, feature_name)
            task = "python bin/runner.py -p {0} -o {1} -f {2} -r {3} --taskid {4}".format(product,
                                                                                                  options.oem_client,
                                                                                                  feature,
                                                                                                  tr.id,
                                                                                                  task_id
                                                                                                  )
            if job:
                task += " -j %s" % job
            if build:
                task += " -b %s" % build
            if options.tags:
                task += " --tags %s" % options.tags
            if options.environment:
                task += " -e %s" % options.environment
            if options.database_enabled:
                task += " -d %s" % options.database_enabled
            if dry_run:
                task += " --dry_run %s" % dry_run

            if scheduletype:
                task += " -s %s" % scheduletype
            if options.year:
                task += " -year %s" % year
            if options.month:
                task += " -month %s" % month
            if options.week:
                task += " -week %s" % week
            if options.day:
                task += " -day %s" % day
            if options.dayofweek:
                task += " -dayofweek %s" % dayofweek
            if options.hour:
                task += " -hour %s" % hour
            if options.minute:
                task += " -minute %s" % minute
            if options.second:
                task += " -second %s" % second

            if options.waitweeks:
                task += " -waitweeks %s" % waitweeks
            if options.waitdays:
                task += " -waitdays %s" % waitdays
            if options.waithours:
                task += " -waithours %s" % waithours
            if options.waitminutes:
                task += " -waitminutes %s" % waitminutes
            if options.waitseconds:
                task += " -waitseconds %s" % waitseconds

            LogHelper.info('run automation task %s' % task)
            p = CeleryHelper.run_task('run_automation', args=[task], queue=automation_queue, task_id=task_id)
            print "start to run task %s " % task
            if sendtodb:
                CeleryHelper.update_task_status(p.id, tr.id, result='PENDING')
            task_obj_list.append(p)

        LogHelper.debug("All tasks are sent to coordinator.")


if __name__ == '__main__':
    run()

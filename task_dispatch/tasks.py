import os
import yaml

from celery.signals import celeryd_after_setup
from celery.exceptions import SoftTimeLimitExceeded


from configuration.config_adapter import ConfigAdapter
from lib.platformhelper import PlatformHelper
from lib.loghelper import LogHelper
from task_dispatch.celeryd import app
from lib.filehelper import FileHelper
from lib.confighelper import ConfigHelper
from lib.cmdhelper import CmdHelper


"""
Celery worker.

-A registered task(s) on worker
-n <worker_name|machine_name>
-Q <message queue>

e.g. celery worker -A task_dispatch.tasks -l info -Ofair -n win7-sinu04
     celery worker -A task_dispatch.tasks -l info -Ofair -n ubuntu-worker01

"""


@app.task(time_limit=30)
def worker_setup(task=None):
    try:
        LogHelper.info("Retrieve task to setup worker.")
        worker_info = ConfigHelper.load(os.path.dirname(__file__), "worker_info.yaml")
        return worker_info
    except SoftTimeLimitExceeded:
        return {}


@app.task(time_limit=3600)
def run_automation(task):
    """
    run automation tasks
    :param task:
    :return:
    """
    try:
        LogHelper.debug("Received task to run automation task {0}".format(task))
        output = CmdHelper.run(task)
        LogHelper.info(output)
        return output

    except SoftTimeLimitExceeded:
        raise SoftTimeLimitExceeded('timeout when execute testcase')


@celeryd_after_setup.connect
def capture_worker_info(sender, instance, **kwargs):
    """
    dump worker infomation whenever worker is connected
    """
    info = PlatformHelper.get_platform_info()
    info['worker_name']='{0}'.format(sender)
    filename = os.path.join(os.path.dirname(__file__), "worker_info.yaml")
    if FileHelper.file_exist(filename):
        LogHelper.info("delete config file %s" % filename)
        FileHelper.delete_file(filename)
    data = dict((k.upper(), v) for k, v in info.items())
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)



def main():
    # ----create log files for runner-----
    logger_path = ConfigAdapter.get_log_path()
    logfile = os.path.join(logger_path, PlatformHelper.get_ip_address(), "worker_logger.log")
    LogHelper.create_logger(logfile,
                            fmt=PlatformHelper.get_ip_address() + " %(asctime)s %(levelname)s " + "worker" + " | %(message)s |")

    LogHelper.info("Worker %s" %(PlatformHelper.get_ip_address()))

main()


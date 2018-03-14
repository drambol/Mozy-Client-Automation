#Script is used to create test run

from time import strftime, gmtime

from lib.testrun import TestRun

from optparse import OptionParser

opt = OptionParser("usage: python bin/setup_testrun.py -f xxx -p xxx -j xxx -b xxx -t xxx")
opt.add_option('-p', "--product",dest="product", help="(required) product: win,mac,linux")
opt.add_option('-j', "--jobname",dest="job", action="store", help="(required) jenkins job name")
opt.add_option('-b', "--build", dest="build", action="store", help="(required) build number to install")
opt.add_option("-e", "--environment",dest="environment", action="store", help="environment: QA12, STD1, STD2, PROD",
               default="QA12")
opt.add_option('-r', '--runtag', dest="runtag", help="testrun tags", default="testrun")


(options, args) = opt.parse_args()

if not options.product:   # if filename is not given
    opt.error('product not given')

if not options.job:  # if filename is not given
    opt.error("branch is not given")


if not options.build:  # if filename is not given
    opt.error("build is not given")

environment = options.environment
if environment not in ("QA12", "STD1", "STD2", "PROD"):
    opt.error("environment must be one of QA12, STD1, STD2, PROD")

#start_time = time.strftime("%Y_%m_%d_%H_%M_%S")
start_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
id = "%s_%s_%s" % (options.product, options.runtag, start_time)
id = id.upper()

tr = TestRun(id, start_time, qa_env=options.environment, build=options.build, client=options.product, branch=options.job, runby="clientqaautomation@emc.com")

tr.save_to_elasticsearch()

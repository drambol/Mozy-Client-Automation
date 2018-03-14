
"""
script to help setup file beat
eventually, we should setup filebeat in runner
"""

import os

from optparse import OptionParser

from lib.filebeathelper import FilebeatHelper
from configuration.global_config_loader import GLOBAL_CONFIG


opt = OptionParser("usage: python bin/setup_fb.py  -p xxx")
opt.add_option('-p', "--product", dest="product", help="(required) product: windows, mac, linux, winfryr, macfryr, iOS, android")

(options, args) = opt.parse_args()


product = None
if not options.product:  # if filename is not given
    opt.error('Product not given')
if options.product.upper() not in ("LINUX", "MAC", "WINDOWS", "WINFRYR", "MACFRYR", "IOS", "ANDROID"):
    opt.error("Product must be one of (linux, mac, window, winfryr, macfryr, ios, android)")
else:
    product = options.product


log_dir = os.path.join(GLOBAL_CONFIG["LogFilePath"][product])
path = os.path.join("%s/*/*.log" % log_dir)
logstash_url = GLOBAL_CONFIG['logstash']['url']
logstash_port = GLOBAL_CONFIG['logstash']['port']
config = {
         "filebeat.prospectors": {
            "input_type": "log",
            "paths": path
        },
        "output.logstash": {
            "hosts": ["%s:%s" %(logstash_url, logstash_port)]
        }
    }
FilebeatHelper.setup_fb(config, product)



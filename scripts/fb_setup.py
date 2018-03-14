#! /usr/sbin/python
import os

from lib.filebeathelper import FilebeatHelper
from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.config_adapter import ConfigAdapter
from configuration.runner_config_loader import RUNNER_CONFIG

logstash_url = GLOBAL_CONFIG.get('LOGSTASH').get('URL') or 'localhost'
port = GLOBAL_CONFIG.get('LOGSTASH').get('PORT') or '5044'

product = RUNNER_CONFIG.get('PRODUCT')
log_path = os.path.join(ConfigAdapter.get_log_path(), '*', '*.log')
config= {}
config['filebeat.prospectors'] = [{'input_type': 'log', 'paths': log_path}]

config['output.logstash'] = {'hosts': ["{logstash_url}:{port}".format(logstash_url=logstash_url,port=port)]}

FilebeatHelper.setup_fb(config, product)

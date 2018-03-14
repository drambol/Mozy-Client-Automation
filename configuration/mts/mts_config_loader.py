import os
from lib import confighelper


MTS_CONFIG = confighelper.ConfigHelper.load(os.path.dirname(__file__), 'mts_config.yaml')
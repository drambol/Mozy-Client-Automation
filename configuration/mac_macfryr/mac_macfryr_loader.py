import os
from lib import confighelper


MAC_MACFRYR_CONFIG = confighelper.ConfigHelper.load(os.path.dirname(__file__), 'mac_macfryr_config.yaml')
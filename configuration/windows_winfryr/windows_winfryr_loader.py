import os
from lib import confighelper


MAC_MACFRYR_CONFIG = confighelper.ConfigHelper.load(os.path.dirname(__file__), 'windows_winfryr_config.yaml')
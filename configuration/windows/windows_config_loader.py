import os
from lib import confighelper


WIN_CONFIG = confighelper.ConfigHelper.load(os.path.dirname(__file__), 'windows_config.yaml')
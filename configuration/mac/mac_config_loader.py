import os
from lib import confighelper


MAC_CONFIG = confighelper.ConfigHelper.load(os.path.dirname(__file__),"mac_config.yaml")


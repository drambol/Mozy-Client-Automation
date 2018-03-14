import os
from lib import confighelper


IOS_CONFIG = confighelper.ConfigHelper.load(os.path.dirname(__file__),"ios_config.yaml")


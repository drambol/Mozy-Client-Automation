import os
from lib import confighelper


LYNX_CONFIG = confighelper.ConfigHelper.load(os.path.dirname(__file__),"lynx_config.yaml")


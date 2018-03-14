import os
from lib import confighelper


ANDROID_CONFIG = confighelper.ConfigHelper.load(os.path.dirname(__file__),"android_config.yaml")


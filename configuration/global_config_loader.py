import os
from lib import confighelper


GLOBAL_CONFIG = confighelper.ConfigHelper.load(os.path.dirname(__file__),"config.yaml")











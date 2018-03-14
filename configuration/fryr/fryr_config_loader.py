import os
from lib import confighelper

FRYR_CONFIG = confighelper.ConfigHelper.load(os.path.dirname(__file__), "winfryr_config.yaml")
MACFRYR_CONFIG = confighelper.ConfigHelper.load(os.path.dirname(__file__), "macfryr_config.yaml")
FRYR_CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "winfryr_config.yaml"))
FRYR_HOST_QA12 = os.path.abspath(os.path.join(os.path.dirname(__file__), "QA12.strings"))
FRYR_HOST_STD1 = os.path.abspath(os.path.join(os.path.dirname(__file__), "STD1.strings"))
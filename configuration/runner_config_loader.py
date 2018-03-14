import os
from lib import confighelper


def runner_config():
    RUNNER_CONFIG = confighelper.ConfigHelper.load(os.path.dirname(__file__), "runner_config.yaml")
    return RUNNER_CONFIG

RUNNER_CONFIG = runner_config()

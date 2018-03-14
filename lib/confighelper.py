#!/usr/bin/env python
#
# Copyright (c) Maginatics, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

import yaml
import os
from lib import singleton


class ConfigHelper(object):
    __metaclass__ = singleton.Singleton

    @staticmethod
    def load(path, name):
        """
        :param path: configuraiton directory
        :param name: yaml file name
        :return: dict
        """
        config = {}
        file = os.path.abspath(os.path.join(path,name))
        if os.path.isfile(file):
            yaml_file = open(file,'r')
            config = yaml.load(yaml_file)
        return config




#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong




import os
import time

from apps.linux.linux_app.command.mozyutil import MozyutilCmd
from lib.singleton import Singleton


class StopCmd(MozyutilCmd):
    __metaclass__ = Singleton
    _command_name = "stop"

    @classmethod
    def stop(cls):
        cls.exe_cmd()

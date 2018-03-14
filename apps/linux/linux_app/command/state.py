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
from configuration.global_config_loader import GLOBAL_CONFIG
from lib.loghelper import LogHelper


class StateCmd(MozyutilCmd):

    _command_name = "state"

    def current_state(self):
        state = ''
        arg = self.generate_str_from_kwargs(engine=None)
        cmd_result = self.exe_cmd(arg)
        result = self.__class__.parse_state_string(cmd_result)
        if result.has_key("State"):
            state = result["State"]
        return state

    def wait_state(self, state, timeout=None, granularity=None):
        """
        :param state:
        :param timeout:
        :param granularity:
        :return:
        """
        result = True

        if timeout is None:
            timeout = GLOBAL_CONFIG["TIMEOUT"]
        if granularity is None:
            granularity = GLOBAL_CONFIG["GRANULARITY"]

        expected_state = []

        if type(state) == str:
            expected_state.append(state)
        else:
            expected_state = state

        current = self.current_state()
        elapsed = 0
        while (current.upper() not in expected_state) and elapsed <= timeout:
            LogHelper.debug("current state is %s" % current)
            time.sleep(granularity)
            elapsed += granularity
            current = self.current_state()
        if current.upper() not in expected_state:
            LogHelper.error("wait %s failed" %expected_state)
            raise Exception("Expected Result %s is not shownup" %expected_state)

        return result

    @classmethod
    def parse_state_string(cls, string):
        result = {}
        lines = string.split(os.linesep)
        for line in lines:
            if line.find(":") >= 0:
                [key,value] = line.split(":")
                result.update({key.lstrip().rstrip(): value.lstrip().rstrip()})
        return result


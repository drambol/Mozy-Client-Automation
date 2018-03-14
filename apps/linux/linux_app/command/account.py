#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

import os
import re

from apps.linux.linux_app.command.mozyutil import MozyutilCmd
from lib.loghelper import LogHelper


class AccountCmd(MozyutilCmd):

    _command_name = "account"

    def get_account(self):
        output = self.exe_cmd()
        return output

    @staticmethod
    def parse_account_to_dict(output):
        dict = {}
        lines = output.split(os.linesep)
        for line in lines:
            match_result = re.match(r"(.*):(.*)", line)
            if match_result is not None:
                key, value = match_result.groups()
                dict.update({key.lstrip().rstrip().upper(): value.lstrip().rstrip()})

        return dict

    def is_activate(self):
        result = False
        if self.get_email() is not None:
            result = True
        return result

    def get_email(self):
        email = None
        account_str = self.get_account()
        account_dict = self.parse_account_to_dict(account_str)
        if account_dict.get("EMAIL"):
            email = account_dict["EMAIL"]
        LogHelper.debug(email)
        return email

    def get_account_details(self):
        """
        :return: (dict) get account details
        """
        account_str = self.get_account()
        acount_dict = self.parse_account_to_dict(account_str)
        return acount_dict



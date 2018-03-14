#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

import re

from apps.mac.mac_cli_client.commands.mac_cmd import MacCmd
from apps.mac.mac_lib.backup_rules import BackupRule


class RuleCmd(MacCmd):

    def __init__(self):
        super(RuleCmd, self).__init__()
        self.command = "rules"

    def list_rules(self):
        result = self.exe_cmd('list')
        rules_list = result.split('\n\n')
        rules_list = filter(lambda x: len(x) > 0, rules_list)

        rules_obj = [BackupRule.create_rule_from_str(rule) for rule in rules_list]

        return rules_obj

    def remove_rule(self, rule):
        if isinstance(rule, BackupRule):
            self.__remove_rule(rule)

    def remove_all_rules(self):
        rules = self.get_rules()
        results = [self.remove_rule(rule) for rule in rules]
        return results

    def __remove_rule(self, rule):

        cmd = 'remove --name={name}'.format(name=re.escape(rule.name))
        if rule.query:
            cmd = '{cmd} --query={query}'.format(cmd=cmd, query=re.escape(rule.query))
        if rule.exclusion == True:
            cmd = '{cmd} --exclusion'.format(cmd=cmd)

        cmd = '{cmd} "{path}"'.format(cmd=cmd, path=rule.path)
        result = self.exe_cmd(cmd)

        return result

    def add_rule(self, rule_obj):
        if isinstance(rule_obj, BackupRule):
            cmd = "add --name={name} {path}".format(name=re.escape(rule_obj.name), path=re.escape(rule_obj.path))
        return self.exe_cmd(cmd)

    def get_rules(self):
        return self.list_rules()



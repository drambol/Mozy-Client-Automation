import os

from behave import *
from configuration.config_adapter import ConfigAdapter
from apps.mac.mac_lib.backup_rules import BackupRule
from apps.mac.mac_cli_client.mac_cli_client import MacCliClient
import sure



@When('I create backup rules')
def step_impl(context):
    root_path = ConfigAdapter.get_testdata_path('MAC')
    raw_path = ''
    rule_name = ''
    for row in context.table:
        rule_name = row.get('name') or 'default_backupset'
        raw_path = row.get('path') or ''
        #TODO: add more fields there

    path = os.path.join(root_path, raw_path)
    backuprule = BackupRule(name=rule_name, path=path)
    MacCliClient.rule_cmd.remove_all_rules()
    MacCliClient.rule_cmd.add_rule(backuprule)


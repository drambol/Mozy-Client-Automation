import os


import sure
from behave import *


from apps.linux.linux_app.linux_gui_client import LinuxGUIClient
from configuration.config_adapter import ConfigAdapter
from lib.loghelper import LogHelper


@When('I add backupdirs with')
def step_impl(context):
    testdata_root = ConfigAdapter.get_testdata_path()
    for row in context.table.rows:
        relative_path = row.get('path') or row.get('paths')
        full_path = os.path.join(testdata_root, relative_path)
        LogHelper.info('add path for %s' % full_path)
        LinuxGUIClient().addbackupdirs_cmd.addbackupdirs(full_path)


@Then('I list backupdirs and verify')
def step_impl(context):
    """
    Useage list backupdirs and check backup dirs from listbackupdirs 
    """
    testdata_root = ConfigAdapter.get_testdata_path()
    for row in context.table.rows:
        relative_path = row.get('path') or row.get('paths')
        full_path = os.path.join(testdata_root, relative_path)
        LogHelper.info('check path for %s' % full_path)
        dirs = LinuxGUIClient().listbackupdir_cmd.listbackupdirs()
        dirs.should.contain(full_path)


@When('I remove backupdirs')
def step_impl(context):
    testdata_root = ConfigAdapter.get_testdata_path()
    for row in context.table.rows:
        relative_path = row.get('path') or row.get('paths')
        full_path = os.path.join(testdata_root, relative_path)
        LogHelper.info('remove path for %s' % full_path)
        LinuxGUIClient.removebackupdirs_cmd.removebackupdirs(full_path)

@When('I clear backupdirs')
def step_impl(context):
    LinuxGUIClient.clearbackupdirs_cmd.clearbackupdirs()
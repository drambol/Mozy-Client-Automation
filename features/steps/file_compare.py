import os

from behave import *
import sure


from lib.filehelper import FileHelper
from configuration.config_adapter import ConfigAdapter
from lib.loghelper import LogHelper
from lib.platformhelper import PlatformHelper


@Then('I expect restore dir "{restore_dir}" is the same with backup dir "{backup_dir}"')
def step_impl(context, restore_dir, backup_dir):
    testdata_root = ConfigAdapter.get_testdata_path()
    output_root = ConfigAdapter.get_output_path()
    restore_file_path = os.path.join(output_root, restore_dir)
    backup_file_path = os.path.join(testdata_root, backup_dir)
    LogHelper.info('restore_file_path is {0}'.format(restore_file_path))
    LogHelper.info('backup_file_path is {0}'.format(backup_file_path))
    if PlatformHelper.is_mac():
        result = FileHelper.is_dir_same(restore_file_path, backup_file_path, exclude_pattern='.DS_Store')
    else:
        result = FileHelper.is_dir_same(restore_file_path, backup_file_path)

    if result:
        for diff in result:
            LogHelper.error("diff files found {path}".format(path=diff))
    try:
        len(result).should.equal(0)
    except AssertionError as e:
        LogHelper.error(e.message)
        raise e




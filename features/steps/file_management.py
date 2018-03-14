import os
import random
from behave import *

from apps.app_lib.datahelper import DataHelper
from configuration.config_adapter import ConfigAdapter
from lib.loghelper import LogHelper
from lib.filehelper import FileHelper

@When('I overwrite testdata with')
def step_impl(context):
    LogHelper.info("start to overwrite files")
    testdata_root = ConfigAdapter.get_testdata_path()

    for row in context.table:
        testdata_dir = os.path.join(testdata_root, row.get('file_folder'))
        testdatas = FileHelper.find_file(testdata_dir, '*')
        max_size = int(row.get('maxsize'))
        min_size = int(row.get('minsize'))
        length = random.randrange(min_size, max_size)

        for testdata in testdatas:
            offset_pattern = row.get('offset_pattern')
            if offset_pattern == 'random':
                size = FileHelper.file_size(testdata)
                offset = random.randrange(1, size)
            elif offset_pattern.isdigit():
                size = FileHelper.file_size(testdata)
                offset = min(int(offset_pattern), size)
            FileHelper.overwrite_file_random(testdata, offset, length)



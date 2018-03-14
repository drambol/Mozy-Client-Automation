import os
import random
from behave import *

from apps.app_lib.datahelper import DataHelper
from configuration.config_adapter import ConfigAdapter
from lib.loghelper import LogHelper
from lib.filehelper import FileHelper

use_step_matcher("parse")


@When('I create {number} test files with')
def step_impl(context, number):
    LogHelper.info("start to create files")
    testdata_config = ConfigAdapter.get_testdata_pros()
    testdata_root = ConfigAdapter.get_testdata_path()
    testdata_dir = testdata_root
    file_size = 0

    for row in context.table:
        if "file_folder" in row.headings:
            testdata_dir = os.path.join(testdata_root, row.get('file_folder'))
        elif "file_dir" in row.headings:
            testdata_dir = os.path.join(testdata_root, row.get('file_dir'))

        for i in range(0, int(number)):
            file_prefix = row.get("file_prefix") or testdata_config.get("FILE_PREFIX") or "td"
            file_txt = row.get("file_ext") or testdata_config.get("FILE_EXT") or "txt"
            name = row.get('file_name') or testdata_config.get("FILE_NAME") or None
            if name:
                file_name = "%s_%s_%s.%s" % (file_prefix, name, i, file_txt)
            else:
                file_name = "%s_%s.%s" % (file_prefix, i, file_txt)
            file_size = row.get("file_size") or testdata_config.get("FILE_SIZE") or 0

            DataHelper.create_testfile(file_name, testdata_dir, int(file_size))

    context.file_size = file_size


@When('I create {number} test files under "{folder}" with')
def step_impl(context, number, folder):
    LogHelper.info("start to create files")
    testdata_config = ConfigAdapter.get_testdata_pros()
    testdata_root = os.path.expanduser("~/{folder}".format(folder=folder))
    testdata_dir = testdata_root

    for row in context.table:
        if "file_folder" in row.headings:
            testdata_dir = os.path.join(testdata_root, row.get('file_folder'))
        elif "file_dir" in row.headings:
            testdata_dir = os.path.join(testdata_root, row.get('file_dir'))

        for i in range(0, int(number)):
            file_prefix = row.get("file_prefix") or testdata_config.get("FILE_PREFIX") or "td"
            file_txt = row.get("file_ext") or testdata_config.get("FILE_EXT") or "txt"
            name = row.get('file_name') or testdata_config.get("FILE_NAME") or None
            if name:
                file_name = "%s_%s_%s.%s" % (file_prefix, name, i, file_txt)
            else:
                file_name = "%s_%s.%s" % (file_prefix, i, file_txt)
            file_size = row.get("file_size") or testdata_config.get("FILE_SIZE") or 0

            DataHelper.create_testfile(file_name, testdata_dir, int(file_size))


@When('I patch test files with')
def step_impl(context):
    testdata_root = ConfigAdapter.get_testdata_path()
    testdata_config = ConfigAdapter.get_testdata_pros()
    for row in context.table.rows:
        if "file_folder" in row.headings:
            testdata_dir = os.path.join(testdata_root, row.get('file_folder') or '')
        elif "file_dir" in row.headings:
            testdata_dir = os.path.join(testdata_root, row.get('file_dir') or '')

        length = row.get('length') or testdata_config.get("FILE_SIZE") or 10
        length = int(length)
        pattern = row.get('content') or 'random'

        testdatas = FileHelper.find_file(testdata_dir, '*')
        for testdata in testdatas:
            LogHelper.info("Patch test files %s %d %s" %(testdata, length, pattern))
            FileHelper.append_file_content(testdata, length, pattern)

@When("I prepare {number} files with")
def step_impl(context, number):
    LogHelper.info("start to judge whether to create files")
    testdata_config = ConfigAdapter.get_testdata_pros()
    testdata_root = ConfigAdapter.get_testdata_path()
    testdata_dir = testdata_root
    file_size = 0
    for row in context.table:
        if "file_folder" in row.headings:
            testdata_dir = os.path.join(testdata_root, row.get('file_folder'))
        elif "file_dir" in row.headings:
            testdata_dir = os.path.join(testdata_root, row.get('file_dir'))

    if not FileHelper.dir_exist(testdata_dir):
        FileHelper.create_directory(testdata_dir)

    if not FileHelper.get_file_count_in_dir(testdata_dir) == int(number):
        FileHelper.delete_file(testdata_dir)
        for row in context.table:
            for i in range(0, int(number)):
                file_prefix = row.get("file_prefix") or testdata_config.get("FILE_PREFIX") or "td"
                file_txt = row.get("file_ext") or testdata_config.get("FILE_EXT") or "txt"
                name = row.get('file_name') or testdata_config.get("FILE_NAME") or None
                if name:
                    file_name = "%s_%s_%s.%s" % (file_prefix, name, i, file_txt)
                else:
                    file_name = "%s_%s.%s" % (file_prefix, i, file_txt)
                file_size = row.get("file_size") or testdata_config.get("FILE_SIZE") or 0

                DataHelper.create_testfile(file_name, testdata_dir, int(file_size))

        context.file_size = file_size

    else:
        for row in context.table:
            length = row.get('length') or testdata_config.get("FILE_SIZE") or 10
            length = int(length)
            size = row.get('file_size') or testdata_config.get("FILE_SIZE")
            pattern = row.get('content') or 'random'

            testdatas = FileHelper.find_file(testdata_dir, '*')
            patch_method = row.get('patch_method')
            if patch_method == "append":
                for testdata in testdatas:
                    LogHelper.info("Patch test files with %s %s %d %s" % (patch_method, testdata, length, pattern))
                    FileHelper.append_file_content(testdata, length, pattern)
            elif patch_method == "truncate":
                for testdata in testdatas:
                    LogHelper.info("Patch test files with %s %s %d %s" % (patch_method, testdata, length, pattern))
                    FileHelper.truncate_file(testdata, length)
            elif patch_method == "insert":
                for testdata in testdatas:
                    LogHelper.info("Patch test files with %s %s %d %s" % (patch_method, testdata, length, pattern))
                    size_offset = random.randrange(1, size)
                    FileHelper.insert_file_content(testdata, size_offset, length, pattern)


@When('I delete test data under "{folder}" with')
def step_impl(context, folder):
    testdata_root = os.path.expanduser("~/{folder}".format(folder=folder))

    for row in context.table.rows:
        if "file_folder" in row.headings or "file_dir" in row.headings:
            testdata_dir = os.path.join(testdata_root, row.get('file_folder') or row.get('file_dir') or '')

            LogHelper.debug("Delete dirs " + testdata_dir)
            FileHelper.delete_directory(testdata_dir)

@when("I clean {location} folder")
def step_impl(context, location):
    if location == 'backup':
        LogHelper.info("start to clean backup folder")
        testdata_root = ConfigAdapter.get_testdata_path()
        testdata_dir = testdata_root
        FileHelper.delete_directory(testdata_dir)
    elif location == 'restore':
        LogHelper.info("start to clean restore folder")
        testdata_root = ConfigAdapter.get_restore_path()
        testdata_dir = testdata_root
        FileHelper.delete_directory(testdata_dir)
    elif location == 'output':
        testdata_root = ConfigAdapter.get_output_path()
        testdata_dir = testdata_root
        LogHelper.info("start to clean output folder: %s"%testdata_dir)
        FileHelper.delete_directory(testdata_dir)


from behave import use_step_matcher
use_step_matcher("re")


@When("I delete test (?P<params>.*) with")
def delete_test_files(context, params):
    testdata_root = ConfigAdapter.get_testdata_path()
    for row in context.table.rows:
        if "file_folder" in row.headings or "file_dir" in row.headings:
            testdata_dir = os.path.join(testdata_root, row.get('file_folder') or row.get('file_dir') or '')

        if params.upper() == "DIRS":
            LogHelper.debug("Delete dirs "+testdata_dir)
            FileHelper.delete_directory(testdata_dir)
            return

        if params.upper() == "FILES":
            pattern = row.get('pattern') or '*'
            file_list = FileHelper.find_file(testdata_dir, pattern)
            for file in file_list:
                LogHelper.debug("delete file %s" % file)
                FileHelper.delete_file(file)
            return


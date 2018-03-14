import re
import os
import time

from behave import *
import sure

from apps.linux.linux_app.linux_gui_client import LinuxGUIClient
from apps.linux.linux_lib.backupset import Backupset
from configuration.config_adapter import ConfigAdapter
from lib.loghelper import LogHelper


@When('I create linux backupset with')
def step_impl(context):
    LinuxGUIClient.backupset_cmd.clear_backup_set()
    root_path = ConfigAdapter.get_testdata_path()
    for row in context.table:
        paths = []
        excludes = []
        filenames = []
        exclude_filenames = []
        filetypes = []
        exclude_filetypes = []


        backupset_name = row.get('name') or 'default_backupset'
        raw_paths = row.get('paths') or ''
        raw_excludes = row.get('excludes') or ''
        exclusionary = row.get('exclusionary') or 'False'

        raw_filenames = row.get('filenames')  # filenames rule
        raw_exclude_filenames = row.get('exclude_filenames')
        raw_filetypes = row.get('filetypes')
        raw_exclude_filetypes = row.get('exclude_filetypes')

        for relative_path in re.split(r",|;|:", raw_paths):
            paths.append(os.path.join(root_path, relative_path.strip().lstrip()))

        if raw_excludes:
            for relative_path in re.split(r",|;|:", raw_excludes):
                excludes.append(os.path.join(root_path, relative_path.strip().lstrip()))

        if raw_filenames:
            for each_filename in re.split(r",|;|:", raw_filenames):
                filenames.append(each_filename)

        if raw_exclude_filenames:
            for each_exclude_filename in re.split(r",|;|:", raw_exclude_filenames):
                exclude_filenames.append(each_exclude_filename)

        if raw_filetypes:
            for each_filetype in re.split(r",|;|:", raw_filetypes):
                filetypes.append(each_filetype)

        if raw_exclude_filetypes:
            for each_exclude_filetype in re.split(r",|;|:", raw_exclude_filetypes):
                exclude_filetypes.append(each_exclude_filetype)

        LogHelper.info("add backupset {name} {paths} {excludes}".format(name=backupset_name, paths=paths,
                                                                        excludes=excludes))

        bs = Backupset(name=backupset_name, paths=paths, excludes=excludes, exclusionary=exclusionary,
                       filenames=filenames, exclude_filenames=exclude_filenames, filetypes=filetypes,
                       exclude_filetypes=exclude_filetypes)

        bs.generate_json_file(filename=backupset_name)


    if LinuxGUIClient.continuous_cmd.get_mode() == LinuxGUIClient.continuous_cmd.ON_DEMAND:
        LogHelper.info("refresh backupset for on-demand mode")
        re_try = 3
        while re_try > 0:
            output = LinuxGUIClient.backupset_cmd.refresh()
            LogHelper.info(output)
            if output.upper().find("SUCCEED") == -1:
                LogHelper.warn("Refresh looks failed")
                LogHelper.debug("re-try refresh after 5 seconds")
                time.sleep(5)
                re_try -= 1
            else:
                LogHelper.info("Refresh success")
                break


@Then('I expect listbackfiles from backupset with')
def step_impl(context):
    for row in context.table.rows:
        expected_value = row.get('summary')
        actual_value = LinuxGUIClient.backupset_cmd.get_listallfiles_summary()
        expected_value.should.be.equal(actual_value)


@Then('I expect listallfiles includes files')
def step_impl(context):
    root_path = ConfigAdapter.get_testdata_path()
    actual_results = LinuxGUIClient.backupset_cmd.list_allfiles()
    LogHelper.info("listallfiles result {result}".format(result=actual_results))
    for row in context.table.rows:
        expected_value = row.get('paths') or row.get('path')
        expected_file = os.path.join(root_path, expected_value)
        LogHelper.info("checking "+expected_file)
        actual_results.should.have(expected_file)


@Then('I expect listallfiles not includes files')
def step_impl(context):
    root_path = ConfigAdapter.get_testdata_path()
    actual_results = LinuxGUIClient.backupset_cmd.list_allfiles()
    LogHelper.info("listallfiles result {result}".format(result=actual_results))
    for row in context.table.rows:
        expected_value = row.get('paths') or row.get('path')
        expected_file = os.path.join(root_path, expected_value)
        LogHelper.info("checking "+expected_file)
        actual_results.shouldnot.have(expected_file)

@Then("I expect dump backupset include")
def step_impl(context):
    root_path = ConfigAdapter.get_testdata_path()
    expected_paths = []
    actual_paths = []

    dumpall_output = LinuxGUIClient.backupset_cmd.dumpall()

    for line in dumpall_output.splitlines():
        if line.lstrip().startswith('+'):
            actual_paths.append(unicode(line))

    for row in context.table.rows:
        path = row.get('paths')
        full_path = path.replace('{root}', root_path)
        expected_paths.append(full_path)
    LogHelper.info("Check paths account...")
    len(actual_paths).should.be(len(expected_paths))

    LogHelper.info("check each item ")
    for path in expected_paths:
        LogHelper.info('Checking path {path}'.format(path=path))
        actual_paths.should.have(path)




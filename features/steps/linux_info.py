import os
import time

import sure
from behave import *

from configuration.config_adapter import ConfigAdapter
from lib.loghelper import LogHelper
from apps.linux.linux_app.linux_gui_client import LinuxGUIClient


@Then("File {file_path} version is not increased")
def step_impl(context, file_path):
    pass


@When("I dump last remote versions for file \"{file_path}\"")
def step_impl(context, file_path):
    testdata_root = ConfigAdapter.get_testdata_path()

    full_file_path = os.path.join(testdata_root, file_path)
    version = LinuxGUIClient.info_cmd.get_last_version(full_file_path)
    LogHelper.info("current version is {version}".format(version=version))
    context.version_before = version


@Then("I expect remote versions for file \"{file_path}\" {is_changed}")
def step_impl(context, file_path, is_changed):
    testdata_root = ConfigAdapter.get_testdata_path()

    full_file_path = os.path.join(testdata_root, file_path)
    current_vesion = LinuxGUIClient.info_cmd.get_last_version(full_file_path)
    LogHelper.info("current version is {version}".format(version=current_vesion))

    if is_changed.upper() == "UNCHANGED":
        current_vesion.should.equal(context.version_before)
    if is_changed.upper() == 'CHANGED':
        #Check whether linux client is running at conntinous mode or manual mode
        current_mode = LinuxGUIClient.continuous_cmd.get_mode()
        if current_mode == LinuxGUIClient.continuous_cmd.ON_DEMAND:
            LogHelper.debug("On demand mode, check version...")
            current_vesion.shouldnot.eql(context.version_before)
        if current_mode == LinuxGUIClient.continuous_cmd.CONTINUOUS:
            LogHelper.debug("On continous mode, wait a new version with 300 second")

            if current_vesion != context.version_before:
                is_version_changed = True
            else:
                is_version_changed = False

            eslapsed_time = 0
            wait_time = 10
            while (not is_version_changed) and eslapsed_time <= 300:
                time.sleep(wait_time)
                eslapsed_time += wait_time
                current_vesion = LinuxGUIClient.info_cmd.get_last_version(full_file_path)
                if current_vesion != context.version_before:
                    is_version_changed = True

                else:
                    LogHelper.info("Current version is %s, it is same as %s"  % (current_vesion, context.version_before) )

            is_version_changed.should.be(True)



@Then("I expected file \"{file_path}\" is deleted from remote")
def step_impl(context, file_path):
    testdata_root = ConfigAdapter.get_testdata_path()
    full_file_path = os.path.join(testdata_root, file_path)
    last_version = LinuxGUIClient.info_cmd.get_last_remote_info(full_file_path, True)
    LogHelper.info("lastest version for %s is %s" % (full_file_path, last_version))
    if last_version is not None:
        last_version.get('DELETE').should.be('Y')
    else:
        last_version.should.be(None)




@Then("I expect file \"{file_path}\" is not backuped")
def step_impl(context, file_path):
    testdata_root = ConfigAdapter.get_testdata_path()
    full_file_path = os.path.join(testdata_root, file_path)
    last_version = LinuxGUIClient.info_cmd.get_last_remote_info(full_file_path, True)
    last_version.should.be(None)

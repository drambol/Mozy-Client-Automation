
import os

from behave import *

from lib.loghelper import LogHelper
from apps.linux.linux_app.linux_gui_client import LinuxGUIClient
from configuration.config_adapter import ConfigAdapter
from lib.filehelper import FileHelper


@When('I download "{raw_path}" to "{raw_output}"')
def step_impl(context, raw_path, raw_output):
    LogHelper.info("start to download %s to %s" %(raw_path, raw_output))
    root_path = ConfigAdapter.get_testdata_path()
    path = os.path.join(root_path, raw_path)
    root_output = ConfigAdapter.get_output_path()
    output = os.path.join(root_output, raw_output)
    LogHelper.info("start to download %s to %s" % (path, output))
    if FileHelper.dir_exist(output):
        FileHelper.delete_directory(output)
    FileHelper.create_directory(output)
    result = LinuxGUIClient.download_cmd.download(path=path, output=output, overwrite=None)
    LogHelper.info(result)


@When('I restore files through mzd to output "{output_dir}"')
def stem_impl(context, output_dir):
    root_path = ConfigAdapter.get_installer_path(product='linux')
    output_path = os.path.join(ConfigAdapter.get_output_path(product='linux'), output_dir)
    for mzd_file in FileHelper.find_file(root_path, "*.mzd"):
        LogHelper.info('restore mzd file %s to %s' %(mzd_file, output_path))
        FileHelper.create_directory(output_path)
        LinuxGUIClient.download_cmd.download(mzd=mzd_file, output=output_path, overwrite=None)


@When('I download files with')
def download_files(context):
    root_path = ConfigAdapter.get_testdata_path()
    output_path = ConfigAdapter.get_output_path(product='linux')

    for row in context.table.rows:
        raw_download_path = row.get('path')
        raw_download_output = row.get('output')
        raw_download_ext = row.get('extensions')
        #add other parameters

        args = {}

        download_path = os.path.join(root_path, raw_download_path)
        args['path'] = download_path

        if raw_download_output:
            download_output = os.path.join(output_path, raw_download_output)
            FileHelper.create_directory(download_output)
            args['output'] = download_output
        if raw_download_ext:
            args['extensions'] = raw_download_ext

	#TODO: add overwrite as condition
	args['overwrite'] = None
        output = LinuxGUIClient.download_cmd.download(**args)
        LogHelper.info(output)

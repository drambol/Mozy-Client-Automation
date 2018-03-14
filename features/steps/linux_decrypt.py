import os
import sure

from behave import *

from apps.linux.linuxclient import LinuxGUIClient
from configuration.config_adapter import ConfigAdapter
from lib.loghelper import LogHelper
from lib.filehelper import FileHelper


@When('I decrypt files "{source}" to "{dest}"')
def decrypt_files(context, source, dest):
    source_root = ConfigAdapter.get_installer_path('LINUX')
    source_full_path = os.path.join(source_root,source)
    LogHelper.info("Decrypt src {source}".format(source=source_full_path))
    dest_root = ConfigAdapter.get_output_path('LINUX')
    dest_full_path = os.path.join(dest_root, dest)
    FileHelper.create_directory(dest_full_path, True)
    output = LinuxGUIClient.decrypt_cmd.decrypt(source_full_path, dest_full_path)
    LogHelper.info("Decrypt output {output}".format(output=output))


@When('I decrypt tarball files to "{dest}"')
def decrypt_tar(context, dest):
    source_root = ConfigAdapter.get_installer_path('LINUX')
    source_full_path = source_root
#    for file in os.listdir(source_root):
#	print(file)
#        if re.match(r'.*\.tar$', file):
#             source_full_path = os.path.join(source_root, file)         
    tars = FileHelper.find_file(source_root, "*.tar")
    LogHelper.info(tars[-1])
    for file in tars:
	LogHelper.info(file)
	source_full_path = os.path.join(source_root, file)


#    source_full_path = os.path.join(source_root,source)
    LogHelper.info("Decrypt src: {source}".format(source=source_full_path))
    dest_root = ConfigAdapter.get_output_path('LINUX')
    dest_full_path = os.path.join(dest_root, dest)
    FileHelper.create_directory(dest_full_path, True)
    output = LinuxGUIClient.decrypt_cmd.decrypt(source_full_path, dest_full_path)
    LogHelper.info("Decrypt output {output}".format(output=output))

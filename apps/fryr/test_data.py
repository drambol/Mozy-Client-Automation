import os, shutil, platform
from lib.loghelper import LogHelper
from lib.filehelper import FileHelper
from configuration.config_adapter import ConfigAdapter

class Test_Data(object):

    @staticmethod
    def clear_restore_folder(folder_name):
        directory = os.path.expanduser('~/Documents/' + folder_name)
        if platform.system() == "Windows":
            directory = "C:/" + folder_name
        for file in FileHelper.find_file(directory, '*'):
            LogHelper.debug('Delete file %s' % file)
            os.remove(file)
        for folder in FileHelper.find_dir(directory, '*'):
            LogHelper.debug('Delete folder %s' % folder)
            try:
                shutil.rmtree(folder)
            except:
                pass

    @staticmethod
    def clear_download_folder():
        directory = ConfigAdapter.get_installer_path('MACFRYR')
        if platform.system() == "Windows":
            directory = "C:/" + ConfigAdapter.get_testdata_path('WINFRYR').split('\\\\')[1]
        for file in FileHelper.find_file(directory, '*'):
            LogHelper.debug('Delete file %s' % file)
            os.remove(file)
        for folder in FileHelper.find_dir(directory, '*'):
            LogHelper.debug('Delete folder %s' % folder)
            try:
                shutil.rmtree(folder)
            except:
                pass

    @staticmethod
    def clear_installer_folder(product_name):
        directory = ConfigAdapter.get_installer_path(product_name)
        for file in FileHelper.find_file(directory, '*'):
            LogHelper.debug('Delete file %s' % file)
            FileHelper.delete_file(file)
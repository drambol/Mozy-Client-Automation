import os, re, time, yaml, subprocess
from lib.platformhelper import PlatformHelper
if PlatformHelper.is_win():
    import win32api
    from pywinauto import application
    from lib.registryhelper import RegistryHelper
from lib.cmdhelper import CmdHelper
from lib.loghelper import LogHelper
from lib.filehelper import FileHelper
from configuration.fryr.fryr_config_loader import FRYR_CONFIG, FRYR_CONFIG_FILE
from configuration.config_adapter import ConfigAdapter
from configuration.runner_config_loader import RUNNER_CONFIG

class WinFryR_Controller(object):

    app = None
    conn_app = None
    restore_manager = None
    test_env = ''
    expected_file_count = 0
    expected_folder_size = 0

    @staticmethod
    def prepare_environment(env):
        FRYR_CONFIG['ENVIRONMENT']['TEST_ENV'] = env
        with open(FRYR_CONFIG_FILE, 'w') as outfile:
            outfile.write(yaml.dump(FRYR_CONFIG, default_flow_style=False))

        hkey1 = 'HKLM\Software\Mozy Restore Manager'
        hkey2 = 'HKCU\Software\Mozy Restore Manager'

        RegistryHelper.write_reg_as_admin(hkey1, 'loglevel', '5', 'REG_DWORD')
        RegistryHelper.write_reg_as_admin(hkey1, 'log.debugmask', 'mordor:Oauth|mordor:http:client', 'REG_SZ')
        RegistryHelper.write_reg_as_admin(hkey1, 'log.tracemask', 'mordor:http:client', 'REG_SZ')
        RegistryHelper.write_reg_as_admin(hkey1, 'ssl.verifyhostname', '0', 'REG_DWORD')
        RegistryHelper.write_reg_as_admin(hkey1, 'ssl.verifypeercertificate', '0', 'REG_DWORD')
        RegistryHelper.write_reg_as_admin(hkey2, 'loglevel', '5', 'REG_DWORD')
        RegistryHelper.write_reg_as_admin(hkey2, 'log.debugmask', 'mordor:Oauth|mordor:http:client', 'REG_SZ')
        RegistryHelper.write_reg_as_admin(hkey2, 'log.tracemask', 'mordor:http:client', 'REG_SZ')
        RegistryHelper.write_reg_as_admin(hkey2, 'ssl.verifyhostname', '0', 'REG_DWORD')
        RegistryHelper.write_reg_as_admin(hkey2, 'ssl.verifypeercertificate', '0', 'REG_DWORD')

        RegistryHelper.write_reg_as_admin(hkey1, 'ahost', FRYR_CONFIG['CREDENTIAL'][env]['AHOST'], 'REG_SZ')
        RegistryHelper.write_reg_as_admin(hkey1, 'bhost', FRYR_CONFIG['CREDENTIAL'][env]['BHOST'], 'REG_SZ')
        RegistryHelper.write_reg_as_admin(hkey1, 'thost', FRYR_CONFIG['CREDENTIAL'][env]['THOST'], 'REG_SZ')
        RegistryHelper.write_reg_as_admin(hkey2, 'ahost', FRYR_CONFIG['CREDENTIAL'][env]['AHOST'], 'REG_SZ')
        RegistryHelper.write_reg_as_admin(hkey2, 'bhost', FRYR_CONFIG['CREDENTIAL'][env]['BHOST'], 'REG_SZ')
        RegistryHelper.write_reg_as_admin(hkey2, 'thost', FRYR_CONFIG['CREDENTIAL'][env]['THOST'], 'REG_SZ')

    @staticmethod
    def clear_restore_folder(folder_name):
        directory = "C:/" + folder_name
        if os.path.exists(directory):
            CmdHelper.runas_admin('RMDIR "' + directory + '" /S /Q')
            time.sleep(3)
        os.makedirs(directory)

    @classmethod
    def launch_restore_manager(self):
        db_file = os.path.expanduser('~/AppData/Local/Mozy Restore Manager/MozyRestoreManager.db')
        LogHelper.info("Deleting db file at " + db_file)
        FileHelper.delete_file(db_file)
        self.app = application.Application()
        self.app.start("C:\Program Files\Mozy\Mozy Restore Manager\MozyRestoreManager.exe")
        time.sleep(2)

    @classmethod
    def login(self, username, password):
        # env = FRYR_CONFIG['ENVIRONMENT']['TEST_ENV']
        self.restore_manager = self.app.Window_(title=u'Mozy Restore Manager', found_index=0)
        self.restore_manager.child_window(class_name="#32770").child_window(class_name="Edit", found_index=0).set_text(username)
        self.restore_manager.child_window(class_name="#32770").child_window(class_name="Edit", found_index=1).set_text(password)
        self.restore_manager.child_window(title="&Next >").Click()
        time.sleep(4)
        # self.restore_manager.print_control_identifiers()

    @classmethod
    def restore_by_mzd(self):
        subprocess.Popen("cmd /c " + self.get_mzd_path())
        time.sleep(15)
        self.conn_app = application.Application().connect(title=u'Mozy Restore Manager', found_index=0)
        self.restore_manager = self.conn_app.Window_(title=u'Mozy Restore Manager', found_index=0)
        try:
            self.restore_manager.child_window(class_name="ListBox").Select(-1)
            self.restore_manager.child_window(title="&Next >").Click()
        except:
            LogHelper.info("Only one restore job found, skip selecting restore job.")
        self.restore_manager.child_window(title="&Select a new location", class_name="Button").CheckByClick()
        self.public_restore_flow()

    @classmethod
    def restore_by_username(self):
        try:
            self.restore_manager.child_window(class_name="ListBox").Select(-1)
            self.restore_manager.child_window(title="&Next >").Click()
        except:
            LogHelper.info("Only one restore job found, skip selecting restore job.")
        try:
            self.app.Window_(title=u'Browse For Folder', found_index=0).child_window(title="Tree View").GetItem([u'Desktop']).Click()
        except:
            LogHelper.info("Browse window not found, clicking 'Browse' button...")
            self.restore_manager.child_window(title="&Select a new location").Click()
            self.public_restore_flow()


    @classmethod
    def archive_restore(self):
        self.restore_manager = self.app.Window_(title=u'Mozy Restore Manager', found_index=0)
        self.restore_manager.child_window(title="Cancel").Click()
        self.restore_manager.MenuSelect("File->Restore From Archive...")
        self.browse_open = self.app.Window_(title=u'Open', found_index=0)
        self.browse_open.child_window(class_name="Edit").set_text(self.get_archive_path())
        win32api.SetCursorPos((0, 0))
        time.sleep(1)
        self.browse_open.Button.Click()
        self.restore_manager = self.app.Window_(title=u'Mozy Restore Manager', found_index=0)
        self.restore_manager.Browse.Click()
        self.public_restore_flow()


    @classmethod
    def decrypt_file(self):
        self.restore_manager = self.app.Window_(title=u'Mozy Restore Manager', found_index=0)
        self.restore_manager.child_window(title="Cancel").Click()
        self.restore_manager.MenuSelect("File->Decrypt Files...")
        self.browse_open = self.app.Window_(title=u'Open', found_index=0)
        self.browse_open.child_window(class_name="Edit").set_text(self.get_encrypted_file())
        win32api.SetCursorPos((0, 0))
        time.sleep(1)
        self.browse_open.Button.Click()
        self.restore_manager = self.app.Window_(title=u'Mozy Restore Manager', found_index=0)
        self.restore_manager.Browse.Click()
        self.public_restore_flow()
        self.enter_personal_key()

    @classmethod
    def decrypt_folder(self, folder_name):
        self.archive_restore()
        self.select_encrypted_folder(folder_name)
        self.restore_manager = self.app.Window_(title=u'Mozy Restore Manager', found_index=0)
        self.restore_manager.Browse.Click()
        self.public_restore_flow(overwrite=True)
        self.enter_personal_key()


    @classmethod
    def public_restore_flow(self, overwrite=False):
        if self.app == None:
            self.app = self.conn_app
        if self.restore_manager == None:
            self.restore_manager = self.app.Window_(title=u'Mozy Restore Manager', found_index=0)
        self.get_file_size()
        win32api.SetCursorPos((0, 0))
        browse_folder = self.app.Window_(title=u'Browse For Folder', found_index=0)
        if PlatformHelper().is_win7():
            browse_folder.child_window(title="Tree View").GetItem([u'Desktop', u'Computer']).Click()
            time.sleep(1)
            browse_folder.child_window(title="Tree View").GetItem([u'Desktop', u'Computer', u'OSDisk (C:)']).Click()
            time.sleep(1)
            browse_folder.child_window(title="Tree View").GetItem([u'Desktop', u'Computer', u'OSDisk (C:)', u'auto_restores']).Click()
            time.sleep(1)
        else:
            browse_folder.child_window(title="Tree View").GetItem([u'Desktop', u'This PC']).Click()
            time.sleep(1)
            browse_folder.child_window(title="Tree View").GetItem([u'Desktop', u'This PC', u'Windows (C:)']).Click()
            time.sleep(1)
            browse_folder.child_window(title="Tree View").GetItem([u'Desktop', u'This PC', u'Windows (C:)', u'auto_restores']).Click()
            time.sleep(1)
        browse_folder.OK.Click()
        if overwrite:
            self.restore_manager.CheckBox.Click()
        self.restore_manager.child_window(title="&Next >").Click()
        self.restore_manager.child_window(title="Finish").Click()

    @classmethod
    def select_encrypted_folder(self, folder_name):
        self.restore_manager = self.app.Window_(title=u'Mozy Restore Manager', found_index=0)
        self.restore_manager.child_window(title="Re&move").Click()
        self.restore_manager.MenuSelect("File->Decrypt Folder Contents...")
        win32api.SetCursorPos((0, 0))
        time.sleep(1)
        browse_folder = self.app.Window_(title=u'Browse For Folder', found_index=0)
        browse_folder.child_window(title="Tree View").GetItem([u'Desktop', u'Computer']).Click()
        time.sleep(1)
        browse_folder.child_window(title="Tree View").GetItem([u'Desktop', u'Computer', u'OSDisk (C:)']).Click()
        time.sleep(1)
        browse_folder.child_window(title="Tree View").GetItem([u'Desktop', u'Computer', u'OSDisk (C:)', u'auto_restores']).Click()
        time.sleep(1)
        browse_folder.child_window(title="Tree View").GetItem([u'Desktop', u'Computer', u'OSDisk (C:)', u'auto_restores', folder_name]).Click()
        time.sleep(1)
        browse_folder.OK.Click()


    @classmethod
    def verify_restore_completed(self, wait_time=60):
        win = self.restore_manager.child_window(title_re="Complete.*")
        for i in range(wait_time):
            try:
                if win.is_visible:
                    LogHelper.info("Restore finished with no error.")
                    return True
            except:
                time.sleep(1)
        LogHelper.info("Restore not finished within given time.")
        return False

    @classmethod
    def check_restore_files(self):
        LogHelper.info("Now checking restore file count and file size.")
        total_size = 0
        file_count = 0
        for dirpath, dirnames, filenames in os.walk(unicode(FRYR_CONFIG['WIN_RESTORE'])):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
                file_count += 1
        LogHelper.info("Expected restore file count: " + str(self.expected_file_count))
        LogHelper.info("Actual restore file count: " + str(file_count))
        LogHelper.info("Expected restore total file size: " + str(self.expected_folder_size))
        LogHelper.info("Actual restore total file size: " + str(total_size))
        assert(self.expected_file_count == file_count)
        # assert(0.99 < self.expected_folder_size / total_size < 1.01)

    @classmethod
    def check_decrypted_files(self):
        time.sleep(2)
        LogHelper.info("Compare files after decryption")
        target1 = self.get_encrypted_file()
        target2 = self.get_decrypted_file()
        assert(self.check_md5(target1, target2) == False)

    @classmethod
    def close_app(self):
        self.restore_manager.child_window(title="Re&move").Click()
        self.restore_manager.Close()
        self.restore_manager = None
        self.app = None

    @classmethod
    def get_file_size(self):
        str = ''
        unit = ''
        num = ''
        for i in range(30):
            if self.restore_manager.Static5.WindowText() == 'Calculating...':
                time.sleep(1)
            else:
                str = self.restore_manager.Static5.WindowText().split(' ')[0]
                unit = self.restore_manager.Static5.WindowText().split(' ')[1]
                num = self.restore_manager.Static4.WindowText()
                break
        if unit == 'MB':
            size = float(str) * 1024 * 1024
        elif unit == 'KB':
            size = float(str) * 1024
        else:
            size = float(str)
        self.expected_folder_size = size
        self.expected_file_count = int(num)

    @staticmethod
    def get_archive_path():
        download_path = ConfigAdapter.get_installer_path().replace("\\\\", "\\")
        for file in os.listdir(download_path):
            if re.match(r'.*\.zip$', file):
                file = os.path.join(download_path, file)
                LogHelper.info("Get archive target path: " + file)
                return file

    @staticmethod
    def get_mzd_path():
        download_path = ConfigAdapter.get_installer_path().replace("\\\\", "\\")
        for file in os.listdir(download_path):
            if re.match(r'restore_.*\.mzd$', file):
                file = os.path.join(download_path, file)
                LogHelper.info("Get mzd target path: " + file)
                return file

    @staticmethod
    def get_encrypted_file():
        download_path = ConfigAdapter.get_testdata_path().replace("\\\\", "\\")
        for file in os.listdir(download_path):
            if os.path.isfile(os.path.join(download_path, file)):
                file = os.path.join(download_path, file)
                LogHelper.info("Get encrypted file path: " + file)
                return file

    @staticmethod
    def get_decrypted_file():
        restore_path = FRYR_CONFIG['WIN_RESTORE']
        for file in os.listdir(restore_path):
            if os.path.isfile(os.path.join(restore_path, file)):
                file = os.path.join(restore_path, file)
                LogHelper.info("Get decrypted file path: " + file)
                return file

    @staticmethod
    def get_encrypted_folder():
        download_path = ConfigAdapter.get_testdata_path().replace("\\\\", "\\")
        for folder in os.listdir(download_path):
            if re.match(r'.*\.zip', folder):
                folder = os.path.join(download_path, folder)
                LogHelper.info("Get encrypted folder path: " + folder)
                return folder


    @classmethod
    def enter_personal_key(self):
        env = RUNNER_CONFIG.get('ENVIRONMENT') or 'QA12'
        personal_key = FRYR_CONFIG['RESTORE'][env]['PERSONAL_KEY']
        time.sleep(1)
        self.restore_manager.Edit.set_text(personal_key)
        time.sleep(1)
        self.restore_manager.child_window(title="&OK", class_name="Button").Click()


    @staticmethod
    def check_md5(target1, target2):
        string1 = FileHelper.md5(target1)
        string2 = FileHelper.md5(target2)
        LogHelper.debug(target1 + " md5: " + string1)
        LogHelper.debug(target2 + " md5: " + string2)
        if string1 == string2:
            return True
        return False
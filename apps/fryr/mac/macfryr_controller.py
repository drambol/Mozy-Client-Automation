import os, time, shutil, re

from lib.filehelper import FileHelper
from lib.cmdhelper import CmdHelper
from lib.loghelper import LogHelper

from apps.mac.mac_lib.mac_ui_util import MacUIUtils
from apps.fryr.mac.base_element import MacFryrElement

from configuration.fryr.fryr_config_loader import FRYR_HOST_QA12, MACFRYR_CONFIG
from configuration.config_adapter import ConfigAdapter
from configuration.mac.mac_config_loader import MAC_CONFIG


class MacFryR_Controller(object):

    expected_file_count = 0
    expected_folder_size = 0

    @staticmethod
    def launch_restore_manager():
        import atomac
        atomac.launchAppByBundleId('com.mozy.restoremanager')
        time.sleep(2)
        app = atomac.getAppRefByBundleId('com.mozy.restoremanager')
        if app:
            app.activate()

    @staticmethod
    def prefix_for_sudo():
        password = MACFRYR_CONFIG.get("LOCAL_ADMIN_PASSWORD")
        prefix = 'echo "{password}" | '.format(password=password)
        return prefix

    @staticmethod
    def prepare_environment(env):
        if env.startswith('QA'):
            FILE = '/Applications/Mozy Restore Manager.app/Contents/Resources/Branding.strings'
            os.remove(FILE)
            shutil.copyfile(FRYR_HOST_QA12, FILE)

        RESTORE_PATH = os.path.expanduser('~/Documents/auto_restore')
        if not os.path.exists(RESTORE_PATH):
            os.mkdir(RESTORE_PATH)

    @staticmethod
    def login(username, password):
        LogHelper.info('Log in Fryr with username: %s password %s' % (username, password))
        MacFryrElement({'AXRole': 'AXTextField', 'AXDescription': 'logInEmail'}).enter_username(username)
        MacFryrElement({'AXRole': 'AXTextField', 'AXDescription': 'loginPassword'}).enter_password(password)
        MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:29'}).click()

    @classmethod
    def run_mzd(self):
        CmdHelper.run('open ' + self.get_mzd_path())
        time.sleep(5)

    @staticmethod
    def public_restore_flow(encrypt_type='default', encrypt_key=None):
        # If multiple restore jobs found, then automation will select the latest job to do the restore.
        # Below try catch is to process the multi-restore job scenarios
        try:
            MacFryrElement({'AXRole': 'AXRow'}, -1, 10).left_click()
            LogHelper.info("Multiple restore jobs found, automation will select the latest job to do the restore.")
            MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:29'}).click()
        except:
            LogHelper.info("Only one restore job found, automation will do restore with the default job.")

        MacFryrElement({'AXRole': 'AXRadioButton', 'AXDescription': 'selectNewLocationRadio'}).click()
        MacFryrElement({'AXValue': 'Documents'}).left_click()
        MacFryrElement({'AXIdentifier': '_NS:64'}).mouse_click({'AXValue': 'auto_restore'})
        MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:97'}).click()
        MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:29'}).click()
        if encrypt_type == 'pkey':
            MacFryrElement({'AXRole': 'AXTextField', 'AXIdentifier': '_NS:502'}).force_send(encrypt_key)
            MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:29'}).click()
        elif encrypt_type == 'ckey' or encrypt_type == 'rkey':
            command = 'cp ' + os.path.dirname(os.path.dirname(__file__)) + '/' + encrypt_key + ' ' + ConfigAdapter.get_installer_path()
            CmdHelper.run(command)
            MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:495'}).click()
            MacFryrElement({'AXIdentifier': '_NS:81'}).click()
            MacFryrElement({'AXTitle': 'Macintosh HD'}).click()
            MacFryrElement({'AXIdentifier': '_NS:64'}).mouse_click({'AXValue': 'fryr_installer'})
            MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:97'}).click()
            MacFryrElement({'AXIdentifier': '_NS:64'}).mouse_click({'AXValue': encrypt_key})
            MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:97'}).click()
            MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:29'}).click()
        MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:29'}).click()
        # pass

    @staticmethod
    def verify_restore_completed(wait_time=60):
        # complete_status = MacFryrElement({'AXRole': 'AXStaticText', 'AXIdentifier': '_NS:87'})
        for i in range(wait_time):
            try:
                if MacFryrElement({'AXRole': 'AXStaticText', 'AXIdentifier': '_NS:87'}).get_text() == 'Complete:':
                    LogHelper.info("Restore finished with no error.")
                    return True
                else:
                    time.sleep(1)
            except:
                time.sleep(1)
        LogHelper.info("Restore not finished within given time.")
        return False

    @staticmethod
    def close_app():
        # Remove the restore job and close restore manager
        MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:175'}).click()
        MacFryrElement({'AXRole': 'AXButton', 'AXRoleDescription': 'close button'}).click()

    @classmethod
    def run_mzd_restore(cls, dest, personal_key=None, index=-1):
        """
        select mzd reuqest to restore files
        :param dest:  restore file destination, dertermine to root config and dest
        :param personal_key: personal key, if not None, input personal key during restore process
        :param index: mzd list
        :return: Boolean. if restore complete, true. otherwise false
        """

        output_path = ConfigAdapter.get_output_path()
        output_path = os.path.join(output_path, dest)
        if FileHelper.dir_exist(output_path):
            FileHelper.delete_directory(output_path)
        FileHelper.create_directory(output_path)
        cmd = MacFryR_Controller.prefix_for_sudo() + 'sudo -S chmod -R 777 "{path}"'.format(path=output_path)
        CmdHelper.run(cmd)

        LogHelper.info('Select %s to generate mzd request' % output_path)

        try:
            LogHelper.info("Multiple restore jobs found, automation will select the latest job to do the restore.")
            MacFryrElement({'AXRole': 'AXRow'}, index, 10).left_click()
            MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:29'}).click()
        except:
            LogHelper.info("Only one restore job found, automation will do restore with the default job.")

        MacFryrElement({'AXRole': 'AXRadioButton', 'AXDescription': 'selectNewLocationRadio'}, wait_time=5).click()
        time.sleep(2)
        root = MacUIUtils.get_root_volume_name()
        pop_menu = MacFryrElement({'AXRole': 'AXPopUpButton'}, 0, 10).element

        app = pop_menu.getApplication()

        MacUIUtils.click_popmenu_item_by_value(pop_menu, root)
        browser_window = MacUIUtils.wait_element(app, AXRole='AXWindow', AXTitle='Open')
        browser_handle = MacUIUtils.wait_element(browser_window, AXRole='AXBrowser')
        MacUIUtils.select_nodes(browser_handle, output_path, node_matcher='AXTextField')
        # MacFryrElement({'AXTitle': 'New Folder'}).click()
        # MacFryrElement({'AXIdentifier': '_NS:43'}, 0, 5).send_keys(dest)
        # MacFryrElement({'AXIdentifier': '_NS:53'}).click()
        btn_open = MacUIUtils.wait_element(browser_window, AXRole='AXButton', AXTitle='Open')
        MacUIUtils.click_button(btn_open)
        MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:29'}).click()

        if personal_key:
            LogHelper.info('input personal key %s' % personal_key)
            el = MacUIUtils.wait_element(app, timeout=120, AXRole='AXTextField', AXDescription='privateKeyField')
            MacUIUtils.input_text(el, personal_key)
            LogHelper.info('click next button')
            btn_next = MacFryrElement({'AXRole': 'AXButton', 'AXTitle': 'Next'})
            btn_next.click()

        MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:29'}).click()
        time.sleep(3)

        from apps.mac.mac_gui_installer.mac_gui_installer import AppUIElement
        try:
            textbox_psd = AppUIElement.from_bundle('com.apple.SecurityAgent',
                                               {'AXRole': 'AXTextField', 'AXSubrole': 'AXSecureTextField'}, 0, 10)
        except ValueError:
            LogHelper.info("Security Agent is not found")
            textbox_psd = None

        if textbox_psd and textbox_psd.element:
            password = MAC_CONFIG.get("LOCAL_ADMIN_PASSWORD")
            textbox_psd.send_keys(password)
            time.sleep(1)
            btn_ok = AppUIElement.from_bundle('com.apple.SecurityAgent', {'AXRole': 'AXButton', 'AXTitle': 'OK'})
            btn_ok.left_click()
            time.sleep(1)

        cls.wait_restore_finished()

    @staticmethod
    def wait_restore_finished(timeout=300, recheck_time=2):
        """
        wait restore to be finished
        :param timeout: wait_time
        :param recheck_time: sleep time
        :return: Boolean
        """

        LogHelper.info('wait restore to be finished')
        result = False
        import atomac
        app = atomac.getAppRefByBundleId('com.mozy.restoremanager')
        sa = None
        try:
            sa = atomac.getAppRefByBundleId('com.apple.SecurityAgent')
        except ValueError:
            LogHelper.info("Security Agent is not found")
            sa = None

        is_restore_complete = MacUIUtils.is_element_exist(app, AXRole='AXStaticText', AXValue='Complete:')
        restore_time = 0
        while (not is_restore_complete) and restore_time <= timeout:
            LogHelper.info("restore is not completed")
            if sa:
                sa_exist = MacUIUtils.is_element_exist(sa, AXRole='AXButton', AXTitle='Cancel')
            else:
                sa_exist = False

            if sa_exist:
                LogHelper.info("Cancel Security Agent")
                MacUIUtils.click_button(sa_exist)
            time.sleep(recheck_time)
            restore_time += recheck_time
            is_restore_complete = MacUIUtils.is_element_exist(app, AXRole='AXStaticText', AXValue='Complete:')
            if is_restore_complete:
                LogHelper.info("Restore completed, retsore take %d" % restore_time)
                result = True

        if restore_time >= timeout:
            LogHelper.error("Restore is not completed in %d second!" % timeout)

        return result

    @classmethod
    def check_restore_files(self):
        LogHelper.info("Now checking restore file count and file size.")
        total_size = 0
        file_count = 0
        for dirpath, dirnames, filenames in os.walk(unicode(MACFRYR_CONFIG['MAC_RESTORE'])):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
                file_count += 1
        LogHelper.info("Expected restore file count: " + str(self.expected_file_count))
        LogHelper.info("Actual restore file count: " + str(file_count))
        LogHelper.info("Expected restore total file size: " + str(self.expected_folder_size))
        LogHelper.info("Actual restore total file size: " + str(total_size))
        assert (self.expected_file_count == file_count)
        # assert(0.99 < self.expected_folder_size / total_size < 1.01)

    @staticmethod
    def get_mzd_path():
        download_path = ConfigAdapter.get_testdata_path()
        for file in os.listdir(download_path):
            if re.match(r'restore_.*\.mzd$', file):
                file = os.path.join(download_path, file)
                LogHelper.info("Get mzd target path: " + file)
                return file

    @classmethod
    def archive_restore(self):
        MacFryrElement({'AXTitle': 'File'}).click()
        MacFryrElement({'AXTitle': 'Restore From Archive...'}).click()
        MacFryrElement({'AXIdentifier': '_NS:81'}).click()
        MacFryrElement({'AXTitle': 'Macintosh HD'}).click()
        MacFryrElement({'AXIdentifier': '_NS:64'}).mouse_click({'AXValue': 'fryr_installer'})
        MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:97'}).click()
        MacFryrElement({'AXIdentifier': '_NS:64'}).mouse_click({'AXValue': self.get_archive_name()})
        MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:97'}).click()
        time.sleep(3)
        self.public_restore_flow()

    @staticmethod
    def get_archive_name():
        download_path = ConfigAdapter.get_installer_path()
        for file in FileHelper.find_file(download_path, '*'):
            file = os.path.basename(file)
            pattern = r'restore_(.+?).zip'
            if re.match(pattern, file):
                return file

    @classmethod
    def decrypt_file(self, key):
        MacFryrElement({'AXTitle': 'File'}).click()
        MacFryrElement({'AXTitle': 'Decrypt Files...'}).click()
        MacFryrElement({'AXIdentifier': '_NS:81'}).click()
        MacFryrElement({'AXTitle': 'Macintosh HD'}).click()
        MacFryrElement({'AXIdentifier': '_NS:64'}).mouse_click({'AXValue': 'fryr_installer'})
        MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:97'}).click()
        time.sleep(3)
        self.public_restore_flow()
        self.enter_personal_key(key)

    @staticmethod
    def enter_personal_key(key):
        MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:74'}).click()
        MacFryrElement({'AXRole': 'AXTextField', 'AXIdentifier': '_NS:69'}).enter_personal_key(key)
        MacFryrElement({'AXRole': 'AXButton', 'AXIdentifier': '_NS:12'}).click()

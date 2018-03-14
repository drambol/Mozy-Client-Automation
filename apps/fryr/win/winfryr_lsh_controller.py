import os, re, time, subprocess
from lib.platformhelper import PlatformHelper
if PlatformHelper.is_win():
    import win32api
    from pywinauto import application, MatchError
from lib.cmdhelper import CmdHelper
from lib.loghelper import LogHelper
from lib.filehelper import FileHelper
from configuration.fryr.fryr_config_loader import FRYR_CONFIG
from configuration.config_adapter import ConfigAdapter

class WinFryR_LSH_Controller(object):

    app = None
    conn_app = None
    restore_manager = None

    @classmethod
    def launch_lsh_restore_manager(self):
        if self.conn_app is None:
            self.app = application.Application()
            self.app.start("C:\Program Files\Mozy\Mozy Restore Manager\MozyLshRestoreManager.exe")
            time.sleep(2)
            self.conn_app = application.Application(backend="uia").connect(title=u'Mozy Restore Manager', found_index=0)
            self.restore_manager = self.conn_app.Window_(title=u'Mozy Restore Manager', found_index=0)

    @classmethod
    def restore_by_mzdx(self, include_all_version=True, wait_for_export_completed=True):
        subprocess.Popen("cmd /c " + self.get_mzdx_path())
        time.sleep(15)
        self.conn_app = application.Application(backend="uia").connect(title=u'Mozy Restore Manager', found_index=0)
        self.restore_manager = self.conn_app.Window_(title=u'Mozy Restore Manager', found_index=0)
        self.restore_manager.Button4.click()
        self.public_lsh_restore_flow(include_all_version=include_all_version, wait_for_export_completed=wait_for_export_completed)

    @classmethod
    def add_queue_job(self):
        subprocess.Popen("cmd /c " + self.get_mzdx_path())
        time.sleep(15)
        self.conn_app = application.Application(backend="uia").connect(title=u'Mozy Restore Manager', found_index=0)
        self.restore_manager = self.conn_app.Window_(title=u'Mozy Restore Manager', found_index=0)
        warning_msg = 'Only one job may be running at a time. This job will be added to the queue.'
        warning_element = self.restore_manager.child_window(title=warning_msg, control_type="Text")
        assert warning_element.is_visible() is True
        LogHelper.info("Verified that the warning message is displayed: " + warning_msg)
        add_to_queue_btn = self.restore_manager.child_window(title="Add to Queue", control_type="Text")
        assert add_to_queue_btn.is_visible() is True
        LogHelper.info("Verified that the 'Add to Queue' button is displayed for user.")
        add_to_queue_btn.click_input()
        job_status = str(self.restore_manager.child_window(title="Queued", control_type="Text").texts()).split("'")[1]
        assert job_status == 'Queued'
        LogHelper.info("Verified that the new added job is in 'Queued' status.")

    @classmethod
    def public_lsh_restore_flow(self, include_all_version=False, wait_for_export_completed=True):
        time.sleep(2)
        browse_app = application.Application().connect(title=u'Browse For Folder', found_index=0)
        browse_folder = browse_app.Window_(title=u'Browse For Folder', found_index=0)
        if PlatformHelper().is_win7():
            browse_folder.child_window(title="Tree View").GetItem([u'Desktop', u'Computer']).Click()
            time.sleep(1)
            browse_folder.child_window(title="Tree View").GetItem([u'Desktop', u'Computer', u'OSDisk (C:)']).Click()
            time.sleep(1)
            browse_folder.child_window(title="Tree View").GetItem(
                [u'Desktop', u'Computer', u'OSDisk (C:)', u'auto_restores']).Click()
            time.sleep(1)
        else:
            browse_folder.child_window(title="Tree View").GetItem([u'Desktop', u'This PC']).Click()
            time.sleep(1)
            browse_folder.child_window(title="Tree View").GetItem([u'Desktop', u'This PC', u'Windows (C:)']).Click()
            time.sleep(1)
            browse_folder.child_window(title="Tree View").GetItem(
                [u'Desktop', u'This PC', u'Windows (C:)', u'auto_restores']).Click()
            time.sleep(1)
        browse_folder.OK.Click()
        if include_all_version:
            self.restore_manager.CheckBox.toggle()
        self.restore_manager.child_window(title="Start", control_type="Button").click()
        if wait_for_export_completed is True:
            self.wait_for_export_completed()

    @classmethod
    def return_to_job_list(self):
        try:
            self.restore_manager.Jobs.click_input()
        except MatchError:
            pass

    @classmethod
    def get_job_status(self, job_name='default'):
        time.sleep(10)  # In case job status is not refreshed
        self.return_to_job_list()
        job_list = self.restore_manager.ListBox0
        if job_name == 'default':
            job_name = str(job_list.child_window(control_type="Text", found_index=0).texts()).split("'")[1]
        for job_name_index in range (0, 5):
            current_job_name = str(job_list.child_window(control_type="Text", found_index=job_name_index).texts()).split("'")[1]
            if current_job_name == job_name:
                job_status_index = job_name_index + 1
                job_name = str(job_list.child_window(control_type="Text", found_index=job_name_index).texts()).split("'")[1]
                job_status = str(job_list.child_window(control_type="Text", found_index=job_status_index).texts()).split("'")[1]
                LogHelper.info("Job name: " + job_name + ", job status: " + job_status)
                return job_status

    @classmethod
    def click_action_panel(self, command, job_name='default'):
        self.return_to_job_list()
        job_list = self.restore_manager.ListBox0
        if job_name == 'default':
            job_name = str(job_list.child_window(control_type="Text", found_index=0).texts()).split("'")[1]
        for job_name_index in range (0, 5):
            current_job_name = str(job_list.child_window(control_type="Text", found_index=job_name_index).texts()).split("'")[1]
            if current_job_name == job_name:
                job_list.child_window(auto_id="m_displayActionPanel", control_type="Button", found_index=job_name_index).click_input()
                try:
                    job_list.child_window(title=command, control_type="Button", found_index=0).click_input()
                except Exception:
                    job_list.child_window(auto_id="m_displayActionPanel", control_type="Button", found_index=job_name_index).click_input()
                    job_list.child_window(title=command, control_type="Button", found_index=0).click_input()
                LogHelper.info("Click '" + command + "' button to export job " + job_name)
                return


    @classmethod
    def export_edrm(self, version="v1.2"):
        export_job_name = self.get_export_job() + "_edrm_" + version
        self.restore_manager.child_window(title="Export EDRM", control_type="Button").click()
        self.restore_manager.child_window(title=version, control_type="MenuItem").click_input()
        save_as_app = application.Application().connect(title=u'Save As', found_index=0)
        save_as_window = save_as_app.Window_(title=u'Save As', found_index=0)
        save_as_window.child_window(class_name="Edit", found_index=0).set_text(export_job_name)
        win32api.SetCursorPos((0, 0))
        save_as_window.child_window(title="&Save", class_name="Button").click()
        msg_app = application.Application().connect(title=u'Mozy Restore Manager', found_index=0)
        msg_window = msg_app.Window_(title=u'Mozy Restore Manager', found_index=0)
        message = str(msg_window.child_window(class_name="Static").texts())
        assert message.find("EDRM XML is exported to") >= 0, "EDRM XML is successfully exported!"
        LogHelper.info("EDRM XML is successfully exported!")
        time.sleep(1)
        msg_app.Dialog.OK.Click()

    @classmethod
    def get_export_job(self):
        export_path = FRYR_CONFIG['WIN_RESTORE']
        for file in os.listdir(export_path):
            if re.match(r'LSH_.*$', file):
                return file

    @classmethod
    def wait_for_export_completed(self, wait_time=60):
        win = self.restore_manager.child_window(title="Completed", control_type="Text")
        for i in range(wait_time):
            try:
                if win.is_visible:
                    LogHelper.info("Export job finished with no error.")
                    return True
            except:
                time.sleep(1)
        LogHelper.info("Export job finished with no error.")
        return False

    @staticmethod
    def get_mzdx_path():
        download_path = ConfigAdapter.get_download_path().replace("\\\\", "\\")
        for file in os.listdir(download_path):
            if re.match(r'export_.*\.mzdx$', file):
                file = os.path.join(download_path, file)
                LogHelper.info("Get mzd target path: " + file)
                return file

    @staticmethod
    def clear_restore_folder(folder_name):
        directory = "C:/" + folder_name
        if os.path.exists(directory):
            CmdHelper.runas_admin('RMDIR "' + directory + '" /S /Q')
            time.sleep(3)
        os.makedirs(directory)

    @classmethod
    def archive_job(self):
        job_list = self.restore_manager.ListBox0
        job_name = str(job_list.child_window(control_type="Text", found_index=0).texts()).split("'")[1]
        LogHelper.info("Ready to archive job: " + job_name)
        job_list.child_window(auto_id="m_displayActionPanel", control_type="Button", found_index=0).click_input()
        job_list.child_window(title="Archive", control_type="Button", found_index=0).click_input()
        time.sleep(2)
        job_element = self.restore_manager.child_window(title=job_name, control_type="Text")
        assert job_element.exists() is True
        assert job_element.is_visible() is False
        LogHelper.info("Job name " + job_name + " no longer exists in active job list.")
        self.restore_manager.child_window(title="Archived Jobs", control_type="Text", found_index=0).click_input()
        assert job_element.is_visible() is True
        LogHelper.info("Job name " + job_name + " exists in archived job list.")

    @staticmethod
    def delete_all_jobs():
        db_directory = os.path.expanduser('~/AppData/Local/Mozy Restore Manager/database')
        FileHelper.remove_tree(db_directory)

    @classmethod
    def close_app(self):
        self.restore_manager.close()
        self.restore_manager = None
        self.app = None

    @classmethod
    def check_message(self, message):
        job_list = self.restore_manager.ListBox0
        message_dialog = job_list.child_window(title=message, control_type="Text")
        assert message_dialog.is_visible() is True

    @classmethod
    def confirm_quit(self, action):
        job_list = self.restore_manager.ListBox0
        confirm_quit_btn = job_list.child_window(title=action, control_type="Text")
        confirm_quit_btn.click_input()
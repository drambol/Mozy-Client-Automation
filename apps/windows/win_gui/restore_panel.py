
from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil

from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_settings_element import WindowsSettingsElement



class RestorePanel(WindowsUIBase):

    elements = []
    elements.append(WindowsSettingsElement('SysTreeView', 'SysTreeView'))
    elements.append(WindowsSettingsElement('DestinationFolderEdit', 'DestinationFolderEdit'))
    elements.append(WindowsSettingsElement('OverwriteExisting', 'OverwriteExisting'))
    elements.append(WindowsSettingsElement('RadioButton11', 'RadioButton11'))
    elements.append(WindowsSettingsElement('RestoreFiles', 'RestoreFiles'))
    elements.append(WindowsSettingsElement('SearchByDate', 'Search by Date'))

    elements.append(WindowsSettingsElement('OKButton', 'OKButton'))

    def __init__(self, oem="mozypro"):
        # super(FileSystemPanel, self).__init__()

        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"


        super(RestorePanel, self).__init__()


    @property
    def settingswindow(self):
        return self._settingswindow

    @property
    def filetreeview(self):
        return self._filetreeview

    @property
    def overwriteradiobutton(self):
        self._overwriteradiobutton

    @property
    def renameradiobutton(self):
        self._renameradiobutton

    @property
    def restorebutton(self):
        self._restorebutton

    def startrestore(self):
        # self.restorebutton.Click()
        # self.settingswindow.RestoreFiles.Click()
        WindowsGUIUtil.click_button(self.RestoreFiles)

    @property
    def destination(self):
        return self._destination

    def select_overwrite(self):
        # self.overwriteradiobutton.CheckByClick()   # Ummm. Doens't work...
        # self.settingswindow.OverwriteExisting.CheckByClick()
        WindowsGUIUtil.click_radio_button(self.OverwriteExisting)

    def select_rename(self):
        # self.renameradiobutton.CheckByClick()   # Ummm. Doens't work...
        # self.settingswindow.RadioButton11.CheckByClick()
        WindowsGUIUtil.click_radio_button(self.RadioButton11)

    def set_destination(self, dest="C:/RESTORE"):
        # self.destination.set_text(dest.replace("/", "\\"))
        WindowsGUIUtil.input_text(self.DestinationFolderEdit, dest.replace("/", "\\"))

    def selectinrestore(self, path = "C:/test_data",dest="C:/RESTORE"):
        """
        Select folder to be backed up
        :param root_path:
        :return:
        """
        # TODO: Now is hardcoded to Local Disk (C:), this may not compatible on other OS.
        import time
        time.sleep(2)
        testfolder = path.split("/")

        # self.settingswindow.RestoreButton.Click()
        # filesystempanel = FileSystemPanel("mozypro")
        file_treeview = self.SysTreeView
        try:
            # file_treeview.GetItem([file_treeview.GetItem([0]).Text()]).Click(double=True)
            items = [file_treeview.GetItem([0]).Text()] + [unicode("Drive(" + testfolder[0].upper() + ")")]# + testfolder[1:]

            # Select files to restore
            file_treeview.GetItem(items).Click(double=True, where='check')

            # Set destination
            self.set_destination(dest)
            time.sleep(1)

            self.select_overwrite()
            time.sleep(1)

            # self.select_rename()

            return True
        except Exception as exc:
            raise self.retry(exc=exc, countdown=60)
            return False

    def select_restore_by_date(self, path = "C:/test_data",dest="C:/RESTORE"):
        import time
        time.sleep(2)
        testfolder = path.split("/")
        file_treeview = self.SysTreeView
        date_setting = self.SearchByDate
        try:
            # file_treeview.GetItem([file_treeview.GetItem([0]).Text()]).Click(double=True)
            WindowsGUIUtil.click_button(date_setting)
            items = [file_treeview.GetItem([0]).Text()] + [
                unicode("Drive(" + testfolder[0].upper() + ")")]  # + testfolder[1:]

            # Select files to restore
            file_treeview.GetItem(items).Click(double=True, where='check')

            # Set destination
            self.set_destination(dest)
            time.sleep(1)

            self.select_overwrite()
            time.sleep(1)

            # self.select_rename()

            return True
        except Exception as exc:
            raise self.retry(exc=exc, countdown=60)
            return False

    def apply(self):
        WindowsGUIUtil.click_button(self.OKButton)


if __name__ == "__main__":
    restorepanel = RestorePanel("mozypro")
    # restorepanel.print_control_identifiers()
    file_treeview = restorepanel.SysTreeView
    # print file_treeview
    root = file_treeview.GetItem([0])
    print root.Text()
    # file_treeview.Click
    result = restorepanel.selectinrestore("c:/test_data/smoke", "c:/output")

    # restorepanel.startrestore()

    # print result
    # if result:
    #     restorepanel.startrestore()
    # else:
    #     print "WARNING: Can't restore files."
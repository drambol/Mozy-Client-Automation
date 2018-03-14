
from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_settings_element import WindowsSettingsElement

from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil


class FileSystemPanel(WindowsUIBase):

    elements = []
    elements.append(WindowsSettingsElement('SysTreeView', 'SysTreeView'))
    elements.append(WindowsSettingsElement('OKButton', 'OKButton'))

    def __init__(self, oem="mozypro"):

        super(FileSystemPanel, self).__init__()


    @property
    def settingswindow(self):
        return self._settingswindow

    @property
    def filetreeview(self):
        return self._filetreeview


    def selectinfilesystem(self, root_path="C:/test_data"):
        """
        Select folder to be backed up
        :param root_path:
        :return:
        """
        WindowsGUIUtil.selectinfilesystem(self.SysTreeView, root_path)
        import time
        time.sleep(2)

    def apply(self):
        WindowsGUIUtil.click_button(self.OKButton)


if __name__ == "__main__":
    # settingswindow = SettingsWindow("mozypro")
    # settingswindow.selectinfilesystem("C:/testdata")
    # exit()
    filesystempanel = FileSystemPanel("MozyEnterprise")
    # file_treeview = filesystempanel.filetreeview
    # print file_treeview
    # root = file_treeview.GetItem([0])
    # print root.Text()

    filesystempanel.selectinfilesystem("C:/test_data")
    filesystempanel.apply()


from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_settings_element import WindowsSettingsElement

from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil



class BackupSetsPanel(WindowsUIBase):

    elements = []
    elements.append(WindowsSettingsElement('SysListView', 'SysListView'))
    elements.append(WindowsSettingsElement('OKButton', 'OKButton'))

    def __init__(self, oem="mozypro"):
        super(BackupSetsPanel, self).__init__()


    def add_backupset(self, name="test"):
        """
        Create a backupset
        :param name:  backupset name
        :return:
        """
        listview = self.SysListView
        # listview.
        WindowsGUIUtil.add_backupset(listview, name)

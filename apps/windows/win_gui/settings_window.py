
from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil

from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_settings_element import WindowsSettingsElement

class SettingsWindow(WindowsUIBase):

    elements = []
    # Tabs
    elements.append(WindowsSettingsElement('Welcome', 'Welcome'))
    elements.append(WindowsSettingsElement('BackupSets', 'BackupSets'))
    elements.append(WindowsSettingsElement('FileSystem', 'FileSystem'))
    elements.append(WindowsSettingsElement('Options', 'Options'))
    elements.append(WindowsSettingsElement('History', 'History'))
    elements.append(WindowsSettingsElement('RestoreButton', 'RestoreButton'))

    # Buttons
    elements.append(WindowsSettingsElement('HelpButton', 'HelpButton'))
    elements.append(WindowsSettingsElement('OKButton', 'OKButton'))
    elements.append(WindowsSettingsElement('CancelButton', 'CancelButton'))


    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"
        # app = Application().start("mozyprostat.exe")


        super(SettingsWindow, self).__init__()


    @property
    def settingswindow(self):
        return self._settingswindow


    @property
    def filesystembutton(self):
        return self._filesystembutton

    def select_panel(self, panelname):
        if panelname.upper() == "Welcome".upper():
            return self.select_welcome_panel()
        elif panelname.upper() == "BackupSets".upper():
            return self.select_backupsets_panel()
        elif panelname.upper() == "FileSystem".upper():
            return self.select_filesystem_panel()
        elif panelname.upper() == "Options".upper():
            return self.select_options_panel()
        elif panelname.upper() == "History".upper():
            return self.select_history_panel()
        elif panelname.upper() == "Restore".upper():
            return self.select_restore_panel()

    def select_welcome_panel(self):
        welcome_tab = self.Welcome
        if WindowsGUIUtil.is_visible(welcome_tab):
            WindowsGUIUtil.click_button(welcome_tab)

    def select_backupsets_panel(self):
        backupset_tab = self.BackupSets
        if WindowsGUIUtil.is_visible(backupset_tab):
            WindowsGUIUtil.click_button(backupset_tab)

    def select_filesystem_panel(self):
        filesystem_tab = self.FileSystem
        if WindowsGUIUtil.is_visible(filesystem_tab):
            WindowsGUIUtil.click_button(filesystem_tab)

    def select_options_panel(self):
        options_tab = self.Options
        if WindowsGUIUtil.is_visible(options_tab):
            WindowsGUIUtil.click_button(options_tab)

    def select_history_panel(self):
        history_tab = self.History
        if WindowsGUIUtil.is_visible(history_tab):
            WindowsGUIUtil.click_button(history_tab)

    def select_restore_panel(self):
        restore_tab = self.RestoreButton
        if WindowsGUIUtil.is_visible(restore_tab):
            WindowsGUIUtil.click_button(restore_tab)

    def apply(self):
        print "Save Config."
        WindowsGUIUtil.click_button(self.OKButton)

    def cancel(self):
        WindowsGUIUtil.click_button(self.CancelButton)

    def applychange(self, save=True):
        if save:
            self.apply()
        else:
            self.cancel()

if __name__ == "__main__":
    settings = SettingsWindow("mozypro")
    print settings.RestoreButton.print_control_identifiers()
    settings.select_panel("Restore")
    # settings.selectinfilesystem("C:/testdata")
    # settings.applychange(save=False)
    # settings.applychange()

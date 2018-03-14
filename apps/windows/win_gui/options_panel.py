
from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_settings_element import WindowsSettingsElement, WindowsProxySettingsElement

from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil

# TODO: Implement later
class OptionsPanel(WindowsUIBase):

    elements = []
    elements.append(WindowsSettingsElement('ListTreeView', 'ListTreeView'))
    elements.append(WindowsSettingsElement('General', 'General'))
    elements.append(WindowsSettingsElement('Scheduling', 'Scheduling'))
    elements.append(WindowsSettingsElement('Performance', 'Performance'))
    elements.append(WindowsSettingsElement('Protect', 'Mozy 2xProtect'))
    elements.append(WindowsSettingsElement('Network', 'Network'))
    elements.append(WindowsSettingsElement('Advanced', 'Advanced'))

    #General Panel Settings
    elements.append(WindowsSettingsElement('BackupStatusIcon', 'Show backup status icon on files'))
    elements.append(WindowsSettingsElement('WarnWhenOverQuote', 'Warn me when I go over my quota'))
    elements.append(WindowsSettingsElement('CheckBox1', 'CheckBox1'))
    elements.append(WindowsSettingsElement('CheckBox2', 'CheckBox2'))
    elements.append(WindowsSettingsElement('DayEdit', 'Edit'))
    elements.append(WindowsSettingsElement('Default', 'Default'))
    elements.append(WindowsSettingsElement('Debug', 'Debug'))
    elements.append(WindowsSettingsElement('Custom', 'Custom'))
    elements.append(WindowsSettingsElement('CustomEdit', 'Edit2'))

    #Scheduling Panel Settings
    elements.append(WindowsSettingsElement('Automatic', '&Automatic (Perform backups when your computer is not in use)'))
    elements.append(WindowsSettingsElement('Scheduled', 'Sc&heduled (Perform backups within 10 minutes of the chosen time)'))
    elements.append(WindowsSettingsElement('AutoRadioButton', 'AutoRadioButton'))
    elements.append(WindowsSettingsElement('AutoRadioButton2', 'AutoRadioButton2'))
    elements.append(WindowsSettingsElement('CPUoverEdit', 'Edit'))
    elements.append(WindowsSettingsElement('IdleTimeEdit', 'Edit2'))
    elements.append(WindowsSettingsElement('BackupTimesEdit', 'Edit3'))
    elements.append(WindowsSettingsElement('ComboBox', 'ComboBox'))
    elements.append(WindowsSettingsElement('DateTime', 'SysDateTimePick32'))
    elements.append(WindowsSettingsElement('BackupEveryDay', 'Edit4'))
    elements.append(WindowsSettingsElement('DayofWeek', 'ComboBox2'))
    elements.append(WindowsSettingsElement('AllowAutoBackup', 'When a scheduled backup is missed, allow an automatic backup.'))
    elements.append(WindowsSettingsElement('CheckAuto', 'CheckBox'))
    elements.append(WindowsSettingsElement('SuspendBackup','&Temporarily suspend automatic and scheduled backups for:'))
    elements.append(WindowsSettingsElement('CheckBox2', 'CheckBox2'))
    elements.append(WindowsSettingsElement('SuspendBackupFor', 'Edit5'))
    elements.append(WindowsSettingsElement('BackupType', 'ComboBox3'))
    elements.append(WindowsSettingsElement('AttemptAutoBackup','Attempt automatic backup even when a &network connection is not detected'))
    elements.append(WindowsSettingsElement('CheckBox3', 'CheckBox3'))
    elements.append(WindowsSettingsElement('StartAutoBackup','Start automatic backups when the computer is running on batter&y power'))
    elements.append(WindowsSettingsElement('CheckBox4', 'CheckBox4'))

    #Performance Panel Settings
    elements.append(WindowsSettingsElement('EnableBandwidthThrottle','Throttlin&g Parameters'))
    elements.append(WindowsSettingsElement('Bandwidth', 'msctls_trackbar3'))
    elements.append(WindowsSettingsElement('AlwaysThrottle', 'Al&ways Throttle'))
    elements.append(WindowsSettingsElement('ThrottleBetween', 'Throttle Between These &Hours:'))
    elements.append(WindowsSettingsElement('AutoRadioButton', 'AutoRadioButton'))
    elements.append(WindowsSettingsElement('AutoRadioButton2', 'AutoRadioButton2'))
    elements.append(WindowsSettingsElement('StartTime', 'SysDateTimePick'))
    elements.append(WindowsSettingsElement('EndTime', 'SysDateTimePick2'))
    elements.append(WindowsSettingsElement('Monday', 'Monday'))
    elements.append(WindowsSettingsElement('Tuesday', 'Tuesday'))
    elements.append(WindowsSettingsElement('Wednesday', 'Wednesday'))
    elements.append(WindowsSettingsElement('Thursday', 'Thursday'))
    elements.append(WindowsSettingsElement('Friday', 'Friday'))
    elements.append(WindowsSettingsElement('Saturday', 'Saturday'))
    elements.append(WindowsSettingsElement('Sunday', 'Sunday'))
    elements.append(WindowsSettingsElement('CheckBox3', 'CheckBox3'))
    elements.append(WindowsSettingsElement('CheckBox4', 'CheckBox4'))
    elements.append(WindowsSettingsElement('CheckBox5', 'CheckBox5'))
    elements.append(WindowsSettingsElement('CheckBox6', 'CheckBox6'))
    elements.append(WindowsSettingsElement('CheckBox7', 'CheckBox7'))
    elements.append(WindowsSettingsElement('CheckBox8', 'CheckBox8'))
    elements.append(WindowsSettingsElement('CheckBox2', 'CheckBox2'))
    elements.append(WindowsSettingsElement('BackupSpeed', 'msctls_trackbar32'))

    #Mozy 2xProtect Panel Settings
    elements.append(WindowsSettingsElement('Enable2Protect','Enable 2xProtect'))
    elements.append(WindowsSettingsElement('CheckBox', 'CheckBox'))
    elements.append(WindowsSettingsElement('Drive', 'ComboBox'))
    elements.append(WindowsSettingsElement('ViewInExplorer','wxWindowClassNR'))
    elements.append(WindowsSettingsElement('MaxFileSize', '&Maximum file size:'))
    elements.append(WindowsSettingsElement('CheckBox2', 'CheckBox2'))
    elements.append(WindowsSettingsElement('MaxFileSizeEdit', 'Edit'))
    elements.append(WindowsSettingsElement('SizeType1', 'ComboBox2'))
    elements.append(WindowsSettingsElement('MaxSizeofFolder', 'M&aximum size of history folder:'))
    elements.append(WindowsSettingsElement('CheckBox3', 'CheckBox3'))
    elements.append(WindowsSettingsElement('MaxSizeofFolderEdit', 'Edit2'))
    elements.append(WindowsSettingsElement('SizeType2', 'ComboBox3'))
    elements.append(WindowsSettingsElement('EmptyHistory', '&Empty History'))

    #Network Panel Settings
    elements.append(WindowsSettingsElement('SetupProxy', 'Setup &Proxy...'))

    #Advanced Panel Settings
    elements.append(WindowsSettingsElement('AutoUpdate', 'Automatically &update the client software without prompting me'))
    elements.append(WindowsSettingsElement('AutoLog', 'Automatically log in to Settings and to my online account'))
    elements.append(WindowsSettingsElement('ShowStatus', 'Show st&atus when a backup completes'))
    elements.append(WindowsSettingsElement('ShowPreconfigured', 'Show all pre-con&figured backup sets'))
    elements.append(WindowsSettingsElement('ShowAdvancesFeatures', 'Show ad&vanced backup set features'))
    elements.append(WindowsSettingsElement('ShowVirtualDrive', 'Show the virtual &drive in This PC'))
    elements.append(WindowsSettingsElement('ShowRestoreOption', 'Show the restore option on the right-click &menu in Windows Explorer'))
    elements.append(WindowsSettingsElement('EnableOpenFiles', 'Enable support for backing up &open files'))
    elements.append(WindowsSettingsElement('EnableEFSFiles', 'Enable support for backing up &EFS encrypted files'))
    elements.append(WindowsSettingsElement('ShowProtectedFiles', 'Allow back up and display of prote&cted operating system files'))
    elements.append(WindowsSettingsElement('ShowMoreDetails', 'Show more details in Status window'))
    elements.append(WindowsSettingsElement('CheckBox', 'CheckBox'))
    elements.append(WindowsSettingsElement('CheckBox2', 'CheckBox2'))
    elements.append(WindowsSettingsElement('CheckBox3', 'CheckBox3'))
    elements.append(WindowsSettingsElement('CheckBox4', 'CheckBox4'))
    elements.append(WindowsSettingsElement('CheckBox5', 'CheckBox5'))
    elements.append(WindowsSettingsElement('CheckBox6', 'CheckBox6'))
    elements.append(WindowsSettingsElement('CheckBox7', 'CheckBox1'))
    elements.append(WindowsSettingsElement('CheckBox8', 'CheckBox8'))
    elements.append(WindowsSettingsElement('CheckBox9', 'CheckBox9'))
    elements.append(WindowsSettingsElement('CheckBox10', 'CheckBox10'))
    elements.append(WindowsSettingsElement('CheckBox11', 'CheckBox11'))



    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"

        super(OptionsPanel, self).__init__()


    def select_general(self):
        WindowsGUIUtil.click_button(self.General)

    def select_scheduling(self):
        WindowsGUIUtil.click_button(self.Scheduling)

    def select_performance(self):
        WindowsGUIUtil.click_button(self.Performance)

    def select_2xprotect(self):
        WindowsGUIUtil.click_button(self.Protect)

    def select_network(self):
        WindowsGUIUtil.click_button(self.Network)

    def select_advanced(self):
        WindowsGUIUtil.click_button(self.Advanced)

    # General Panel Settings
    def show_backup_status_icon(self):
        show_icon = self.BackupStatusIcon
        if not WindowsGUIUtil.is_selected(self.CheckBox1):
            WindowsGUIUtil.click_button(show_icon)

    def warn_when_over_quota(self):
        quota_warn = self.WarnWhenOverQuote
        if not WindowsGUIUtil.is_selected(self.CheckBox2):
            WindowsGUIUtil.click_button(quota_warn)

    def set_warn_days(self, day):
        set_day = self.DayEdit
        WindowsGUIUtil.input_text(set_day,str(day))

    def logging_type_is_default(self):
        WindowsGUIUtil.click_button(self.Default)

    def logging_type_is_debug(self):
        WindowsGUIUtil.click_button(self.Debug)

    def logging_type_is_custom(self, logging_type):
        WindowsGUIUtil.click_button(self.Custom)
        WindowsGUIUtil.input_text(self.CustomEdit,logging_type)

    # Scheduling Panel Settings
    def select_automatic_type(self):
        WindowsGUIUtil.click_button(self.Automatic)

    def select_scheduled_type(self):
        WindowsGUIUtil.click_button(self.Scheduled)

    def set_CPU_over_parameter(self, parameter):
        if WindowsGUIUtil.is_selected(self.AutoRadioButton):
            WindowsGUIUtil.input_text(self.CPUoverEdit, str(parameter))

    def set_idle_time_parameter(self, parameter):
        if WindowsGUIUtil.is_selected(self.AutoRadioButton):
            WindowsGUIUtil.input_text(self.IdleTimeEdit, str(parameter))

    def set_backup_times_parameter(self, parameter):
        if WindowsGUIUtil.is_selected(self.AutoRadioButton):
            WindowsGUIUtil.input_text(self.BackupTimesEdit, str(parameter))

    def select_daily_schedule(self, time, every_day):
        time_list = time.split(":")
        hour = time_list[0]
        minute = time_list[1]
        if WindowsGUIUtil.is_selected(self.AutoRadioButton2):
            WindowsGUIUtil.select_combobox(self.ComboBox, 0)
            WindowsGUIUtil.set_time(self.DateTime, int(hour), int(minute))
            WindowsGUIUtil.input_text(self.BackupEveryDay, str(every_day))

    def select_weekly_schedule(self, time, dayofweek, every_day):
        time_list = time.split(":")
        hour = time_list[0]
        minute = time_list[1]
        if WindowsGUIUtil.is_selected(self.AutoRadioButton2):
            WindowsGUIUtil.select_combobox(self.ComboBox, 1)
            WindowsGUIUtil.set_time(self.DateTime, int(hour), int(minute))
            WindowsGUIUtil.select_combobox(self.DayofWeek, dayofweek-1)
            WindowsGUIUtil.input_text(self.BackupEveryDay, str(every_day))

    def allow_auto_backup(self):
        if not WindowsGUIUtil.is_selected(self.CheckAuto):
            WindowsGUIUtil.click_button(self.AllowAutoBackup)

    def set_suspend_backup(self, number, type):
        if not WindowsGUIUtil.is_selected(self.CheckBox2):
            WindowsGUIUtil.click_button(self.SuspendBackup)
        if WindowsGUIUtil.is_enabled(self.BackupType):
            if type == "hours":
                WindowsGUIUtil.select_combobox(self.BackupType, 0)
            elif type == "days":
                WindowsGUIUtil.select_combobox(self.BackupType, 1)
            elif type == "weeks":
                WindowsGUIUtil.select_combobox(self.BackupType, 2)
        WindowsGUIUtil.input_text(self.SuspendBackupFor, str(number))

    def attempt_automatic_backup(self):
        if not WindowsGUIUtil.is_selected(self.CheckBox3):
            WindowsGUIUtil.click_button(self.AttemptAutoBackup)

    def start_automatic_backup(self):
        if not WindowsGUIUtil.is_selected(self.CheckBox4):
            WindowsGUIUtil.click_button(self.StartAutoBackup)

    #Performance Panel Settings
    def set_bandwidth_throttle(self, bandwidth):
        bandwidth_tab ={
            'no backup': 0,
            '64kbps': 1,
            '128kbps': 2,
            '256kbps': 3,
            '512kbps': 4,
            '768kbps': 5,
            '1mbps': 6,
            '2mbps': 7,
            '3mbps': 8
        }
        bandwidth_throttle = bandwidth_tab[bandwidth]
        WindowsGUIUtil.set_trackbar(self.Bandwidth, bandwidth_throttle)

    def always_throttle(self):
        WindowsGUIUtil.click_button(self.AlwaysThrottle)

    def set_throttle_parameter(self, start_time, end_time):
        if not WindowsGUIUtil.is_selected(self.AutoRadioButton2):
            WindowsGUIUtil.click_button(self.ThrottleBetween)
        time_list1 = start_time.split(":")
        hour1 = time_list1[0]
        minute1 = time_list1[1]
        WindowsGUIUtil.set_time(self.StartTime, int(hour1), int(minute1))
        time_list2 = end_time.split(":")
        hour2 = time_list2[0]
        minute2 = time_list2[1]
        WindowsGUIUtil.set_time(self.EndTime, int(hour2), int(minute2))

    def set_day_of_week(self, day_of_week):
        if day_of_week == "Monday":
            if not WindowsGUIUtil.is_selected(self.CheckBox3):
                WindowsGUIUtil.click_button(self.Monday)
        elif day_of_week == "Tuesday":
            if not WindowsGUIUtil.is_selected(self.CheckBox4):
                WindowsGUIUtil.click_button(self.Tuesday)
        elif day_of_week == "Wednesday":
            if not WindowsGUIUtil.is_selected(self.CheckBox5):
                WindowsGUIUtil.click_button(self.Wednesday)
        elif day_of_week == "Thursday":
            if not WindowsGUIUtil.is_selected(self.CheckBox6):
                WindowsGUIUtil.click_button(self.Thursday)
        elif day_of_week == "Friday":
            if not WindowsGUIUtil.is_selected(self.CheckBox7):
                WindowsGUIUtil.click_button(self.Friday)
        elif day_of_week == "Saturday":
            if not WindowsGUIUtil.is_selected(self.CheckBox8):
                WindowsGUIUtil.click_button(self.Saturday)
        elif day_of_week == "Sunday":
            if not WindowsGUIUtil.is_selected(self.CheckBox2):
                WindowsGUIUtil.click_button(self.Sunday)

    def set_backup_speed(self, speed):
        WindowsGUIUtil.set_trackbar(self.BackupSpeed, speed)

    # Mozy 2xProtect Panel Settings
    def enable_2xprotect(self):
        if not WindowsGUIUtil.is_selected(self.CheckBox):
            WindowsGUIUtil.click_button(self.Enable2Protect)

    def select_destination_drive(self, drive):
        drives = WindowsGUIUtil.get_combobox_text(self.Drive)
        if drive in drives:
            WindowsGUIUtil.select_combobox(self.Drive, drive)
        else:
            print "The drive is not existed."

    def view_in_exploerer(self):
        if WindowsGUIUtil.is_enabled(self.ViewInExplorer):
            WindowsGUIUtil.click_button(self.ViewInExplorer)

    def set_max_file_size(self, size, sizetype):
        if not WindowsGUIUtil.is_selected(self.CheckBox2):
            WindowsGUIUtil.click_button(self.MaxFileSize)
        size = str(size)
        WindowsGUIUtil.input_text(self.MaxFileSizeEdit, size)
        WindowsGUIUtil.select_combobox(self.SizeType1, sizetype)

    def set_max_size_of_history_folder(self, size, sizetype):
        if not WindowsGUIUtil.is_selected(self.CheckBox3):
            WindowsGUIUtil.click_button(self.MaxSizeofFolder)
        size = str(size)
        WindowsGUIUtil.input_text(self.MaxSizeofFolderEdit, size)
        WindowsGUIUtil.select_combobox(self.SizeType2, sizetype)

    def empty_history(self):
        WindowsGUIUtil.click_button(self.EmptyHistory)

    # Network Panel Settings
    def setup_proxy(self):
        WindowsGUIUtil.click_button(self.SetupProxy)

    # Advanced Panel Settings
    def auto_update_with_prompt(self):
        if not WindowsGUIUtil.is_selected(self.CheckBox):
            WindowsGUIUtil.click_button(self.AutoUpdate)

    def auto_log_in_to_settings(self):
        if not WindowsGUIUtil.is_selected(self.CheckBox2):
            WindowsGUIUtil.click_button(self.AutoLog)

    def show_status_after_backup(self):
        if not WindowsGUIUtil.is_selected(self.CheckBox3):
            WindowsGUIUtil.click_button(self.ShowStatus)

    def show_pre_configured_sets(self):
        if not WindowsGUIUtil.is_selected(self.CheckBox4):
            WindowsGUIUtil.click_button(self.ShowPreconfigured)

    def show_advanced_backup_features(self):
        if not WindowsGUIUtil.is_selected(self.CheckBox5):
            WindowsGUIUtil.click_button(self.ShowAdvancesFeatures)

    def show_virtual_drive(self):
        if not WindowsGUIUtil.is_selected(self.CheckBox6):
            WindowsGUIUtil.click_button(self.ShowVirtualDrive)

    def show_restore_option(self):
        if WindowsGUIUtil.is_selected(self.CheckBox6):
            WindowsGUIUtil.click_button(self.ShowVirtualDrive)
            WindowsGUIUtil.click_button(self.ShowVirtualDrive)
            WindowsGUIUtil.click_button(self.ShowRestoreOption)
        else:
            WindowsGUIUtil.click_button(self.ShowVirtualDrive)
            WindowsGUIUtil.click_button(self.ShowRestoreOption)


    def enable_backup_open_files(self):
        if not WindowsGUIUtil.is_selected(self.CheckBox8):
            WindowsGUIUtil.click_button(self.EnableOpenFiles)

    def enable_backup_EFS_files(self):
        if not WindowsGUIUtil.is_selected(self.CheckBox9):
            WindowsGUIUtil.click_button(self.EnableEFSFiles)

    def allow_display_OS_files(self):
        if not WindowsGUIUtil.is_selected(self.CheckBox10):
            WindowsGUIUtil.click_button(self.ShowProtectedFiles)

    def show_more_details(self):
        if not WindowsGUIUtil.is_selected(self.CheckBox11):
            WindowsGUIUtil.click_button(self.ShowMoreDetails)

class ProxySettingsPanel(WindowsUIBase):
    elements = []
    elements.append(WindowsProxySettingsElement('NotUseProxy', 'Do &not use a proxy to connect to servers'))
    elements.append(WindowsProxySettingsElement('UseTheProxy', 'Use &this proxy server:'))
    elements.append(WindowsProxySettingsElement('UseDefaultProxy', 'Use this &computer\'s default proxy server'))
    elements.append(WindowsProxySettingsElement('UseAutoProxy','Automatically &detect proxy settings'))
    elements.append(WindowsProxySettingsElement('UseConfigScript','Use &automatic configuration script:'))
    elements.append(WindowsProxySettingsElement('EditProxy', 'Edit'))
    elements.append(WindowsProxySettingsElement('EditURL', 'Edit2'))
    elements.append(WindowsProxySettingsElement('ImportProxySettings', '&Import Windows Proxy Settings'))
    elements.append(WindowsProxySettingsElement('NoProxyAuth', 'My proxy server does not require authentication'))
    elements.append(WindowsProxySettingsElement('AuthViaDomain', 'My proxy server authenticates my computer via the domain'))
    elements.append(WindowsProxySettingsElement('NeedUseInfo', 'My proxy requires a user name and password:'))
    elements.append(WindowsProxySettingsElement('EditUsername', 'Edit3'))
    elements.append(WindowsProxySettingsElement('EditPassword', 'Edit4'))
    elements.append(WindowsProxySettingsElement('EditDomain', 'Edit5'))
    elements.append(WindowsProxySettingsElement('OKButton', 'OK'))
    elements.append(WindowsProxySettingsElement('CancelButton', 'Cancel'))


    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"

        super(ProxySettingsPanel, self).__init__()


    def not_use_proxy(self):
        WindowsGUIUtil.click_radio_button(self.NotUseProxy)

    def use_proxy(self, proxy):
        WindowsGUIUtil.click_radio_button(self.UseTheProxy)
        WindowsGUIUtil.input_text(self.EditProxy,proxy)

    def use_default_proxy(self):
        WindowsGUIUtil.click_radio_button(self.UseDefaultProxy)

    def use_auto_proxy(self):
        WindowsGUIUtil.click_radio_button(self.UseAutoProxy)

    def use_auto_configuration_script(self, url):
        WindowsGUIUtil.click_radio_button(self.UseConfigScript)
        WindowsGUIUtil.input_text(self.EditURL, url)

    def import_proxy_settings(self):
        WindowsGUIUtil.click_button(self.ImportProxySettings)

    def not_require_authentication(self):
        WindowsGUIUtil.click_radio_button(self.NoProxyAuth)

    def authenticate_via_domain(self):
        WindowsGUIUtil.click_radio_button(self.AuthViaDomain)

    def require_username_and_password(self, username, password, domain=''):
        WindowsGUIUtil.click_radio_button(self.NeedUseInfo)
        WindowsGUIUtil.input_text(self.EditUsername, username)
        WindowsGUIUtil.input_text(self.EditPassword, password)
        WindowsGUIUtil.input_text(self.EditDomain, domain)

    def apply_settings(self):
        WindowsGUIUtil.click_button(self.OKButton)

    def cancel_settings(self):
        WindowsGUIUtil.click_button(self.CancelButton)



if __name__ == "__main__":
    option = OptionsPanel("mozypro")
    option.show_restore_option()

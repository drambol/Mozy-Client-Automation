#!/usr/bin/env python

from lib.singleton import Singleton

from apps.windows.win_gui.status_window import StatusWindow
from apps.windows.win_gui.login_dialog import LoginDialog
from apps.windows.win_gui.settings_window import SettingsWindow
from apps.windows.win_gui.filesystem_panel import FileSystemPanel
from apps.windows.win_gui.restore_panel import RestorePanel
from apps.windows.win_gui.install_window import SetupWindow
from apps.windows.windows_controller import Windows_Controller


"""
Windows client automation uses pywinauto, it is a well structured and easy to use UI automation framework.

Methods available to each different control type are listed at: http://pywinauto.readthedocs.io/en/latest/controls_overview.html

NOTE: There is no extra visible methods for Static and PopupMenu.
"""


class Windows_GUI(object):

    __metaclass__ = Singleton

    def __init__(self, oem="mozypro"):
        self.oem = oem

        self._status_window = StatusWindow(oem)
        self._login_dialog = LoginDialog(oem)
        self._settings_window = SettingsWindow(oem)
        self._filesystem_panel = FileSystemPanel(oem)
        self._restore_panel = RestorePanel(oem)
        self._setup_window = SetupWindow(oem)

    @staticmethod
    def start_app(oem="mozypro"):
        if Windows_Controller(oem).is_client_installed():
            if Windows_Controller(oem).is_client_running():
                return True
            else:
                Windows_Controller(oem).start()
        else:
            return False

    def activate(self):
        return True


    @property
    def status_window(self):
        return self._status_window

    @property
    def login_dialog(self):
        return self._login_dialog

    @property
    def settings_window(self):
        return self._settings_window

    @property
    def filesystem_panel(self):
        return self._filesystem_panel

    @property
    def restore_panel(self):
        return self._restore_panel

    @property
    def setup_window(self):
        return self._setup_window
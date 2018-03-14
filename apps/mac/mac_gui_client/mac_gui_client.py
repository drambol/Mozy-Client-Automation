import time

from lib.platformhelper import PlatformHelper
if PlatformHelper.is_mac():
    import atomac

from apps.mac.mac_gui_client.windows.login_sheet import LoginSheet
from apps.mac.mac_lib.mozy_ui_element import MacMozyUIBase
from apps.mac.mac_gui_client.windows.summary_tab import SummaryTab
from apps.mac.mac_gui_client.windows.restore_auth_window import RestoreAuthWindow
from apps.mac.mac_gui_client.windows.view_restore_window import ViewAndRestoreWindow
from apps.mac.mac_gui_client.windows.restore_dest_window import RestoreDestWindow
from apps.mac.mac_gui_client.windows.files_folders_tab import FilesFoldersTab
from lib.singleton import Singleton
from apps.mac.mac_lib.mac_ui_util import MacUIUtils
from lib.cmdhelper import CmdHelper
from apps.mac.mac_controller.mac_controller import MacController


class MacGUIClient(MacMozyUIBase):

    __metaclass__ = Singleton

    def __init__(self):
        self._summary_tab = SummaryTab()
        self._login_sh = LoginSheet()
        self._restore_auth_window = RestoreAuthWindow()
        self._view_restore_window = ViewAndRestoreWindow()
        self._restore_dest_window = RestoreDestWindow()
        self._files_folder_tab = FilesFoldersTab()

    @property
    def summary_tab(self):
        return self._summary_tab

    @property
    def login_sh(self):
        return self._login_sh

    @property
    def restore_auth_window(self):
        return self._restore_auth_window

    @property
    def view_restore_window(self):
        return self._view_restore_window

    @property
    def restore_dest_window(self):
        return self._restore_dest_window

    @property
    def files_folder_tab(self):
        return self._files_folder_tab

    @staticmethod
    def launch_mozy_application():
        """
        launch app
        :return:
        """
        bundleId = MacController().spbundleid
        WindowName = 'MozyPro'
        try:
            atomac.launchAppByBundleId(bundleId)
        except RuntimeError as e:
            print e.message
        mozy_window = None

        app = atomac.getAppRefByBundleId(bundleId)
        window = MacUIUtils.wait_element(app, AXRole='AXWindow')
        app.activate()
        btn_showall = MacUIUtils.wait_element(window, AXRole='AXButton', AXTitle='Show All')
        MacUIUtils.click_button(btn_showall)
        window = MacUIUtils.wait_element(app, AXRole='AXWindow')

        title = window.AXTitle
        if title == 'MozyPro':  # it is already mozy window
            mozy_window = window
        elif title == "System Preferences":
            btn_mozypro = MacUIUtils.wait_element(app, AXRole='AXButton', AXTitle=WindowName)
            btn_mozypro.Press()
            mozy_window = MacUIUtils.wait_element(app, AXRole='AXWindow', AXTitle=WindowName)
        else:
            raise Exception('Not implemented yet')

        if mozy_window.AXRole:
            MacMozyUIBase.mozy_window = mozy_window
            return mozy_window
        else:
            return False

    @staticmethod
    def start_app():
        #check that where mozy is installed
        if MacController().is_installed():
            current_wait_second = 0
            result = MacGUIClient.launch_mozy_application()
            while (not result) and current_wait_second < 120:
                sleep_time = 5
                time.sleep(sleep_time)
                result = MacGUIClient.launch_mozy_application()
                current_wait_second += sleep_time

            return result
        else:
            # mac client is not installed
            raise Exception('Mac Client is not installed')

    @staticmethod
    def restart_app():
        MacGUIClient.__terminate_mozy_app()
        return MacGUIClient.start_app()

    @staticmethod
    def __terminate_mozy_app():
        cmd = "osascript -e \'quit app \"System Preferences\"\'"
        output = CmdHelper.run(cmd)

        return output

    @staticmethod
    def close_app():
        MacGUIClient.__terminate_mozy_app()


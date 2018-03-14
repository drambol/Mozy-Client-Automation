from apps.mac.mac_controller.mac_controller import MacController
from apps.mac.mac_controller.mac_installer import MacInstaller
from apps.mac.mac_gui_client.mac_gui_client import MacGUIClient
from apps.mac.mac_cli_client.mac_cli_client import MacCliClient


class MacClient(object):

    def __init__(self, oem="mozypro"):
        self._controller = MacController()
        self._installer = MacInstaller()
        #Add oem support
        self._cli = MacGUIClient()
        self._gui = MacCliClient()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, value):
        self.controller = value

    @property
    def installer(self):
        return self._installer

    @installer.setter
    def installer(self, value):
        self.installer = value

    @property
    def cli(self):
        return self._cli

    @cli.setter
    def cli(self, value):
        self.cli = value

    @property
    def gui(self):
        return self._gui

    @cli.setter
    def gui(self, value):
        self.gui = value




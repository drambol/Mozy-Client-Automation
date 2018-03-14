
from lib.singleton import Singleton

from apps.windows.windows_cli import Windows_Cli
from apps.windows.windows_controller import Windows_Controller
from apps.windows.windows_gui import Windows_GUI
from apps.windows.win_lib.windows_installer import Windows_Installer

from apps.baseclient import BaseClient

class Windows_Client(BaseClient):

    __metaclass__ = Singleton


    def __init__(self, oem="mozypro"):
        print "Initialise Windows_Client"
        Windows_Client.oem = oem

        self._controller = Windows_Controller(oem)
        self._cli = Windows_Cli(oem)
        self._installer = Windows_Installer(oem)
        self._gui = Windows_GUI(oem)

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, value):
        self.controller = value

    @property
    def cli(self):
        return self._cli

    @cli.setter
    def cli(self, value):
        self.cli = value

    @property
    def installer(self):
        return self._installer

    @installer.setter
    def installer(self, value):
        self.installer = value

    @property
    def gui(self):
        return self._gui

    @gui.setter
    def gui(self, value):
        self.gui = value

# End of Windows_Client

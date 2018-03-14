from apps.linux.linux_app.controller.lynx_controller import LynxCtrl
from apps.linux.linux_app.controller.lynx_installer import LynxInstaller
from apps.linux.linux_app.linux_gui_client import LinuxGUIClient
from lib.singleton import Singleton


class LinuxClient(object):

    __metaclass__ = Singleton

    def __init__(self, oem="mozypro"):
        self._controller = LynxCtrl()
        self._installer = LynxInstaller()
        #Add oem support
        self._cli = LinuxGUIClient()


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




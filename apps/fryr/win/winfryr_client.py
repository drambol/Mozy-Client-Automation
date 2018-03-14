from apps.fryr.win.winfryr_controller import WinFryR_Controller
from apps.fryr.win.winfryr_installer import WinFryR_Installer


class WinFryR_Client(object):

    def __init__(cls):
        pass

    @property
    def installer(cls):
        return WinFryR_Installer

    @property
    def controller(cls):
        return WinFryR_Controller
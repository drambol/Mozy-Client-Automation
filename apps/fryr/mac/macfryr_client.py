from apps.fryr.mac.macfryr_installer import MacFryR_Installer
from apps.fryr.mac.macfryr_controller import MacFryR_Controller

class MacFryR_Client(object):

    def __init__(cls):
        pass

    @property
    def installer(cls):
        return MacFryR_Installer

    @property
    def controller(cls):
        return MacFryR_Controller
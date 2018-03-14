from apps.android.android_installer import Android_Installer
from apps.android.android_controller import Android_Controller


class Android_Client(object):

    driver = None

    def __init__(cls):
        pass

    @property
    def installer(cls):
        return Android_Installer

    @property
    def controller(cls):
        return Android_Controller

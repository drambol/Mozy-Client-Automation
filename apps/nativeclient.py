
# from lib.singleton import Singleton

from apps.android.android_client import Android_Client
from apps.fryr.mac.macfryr_client import MacFryR_Client
from apps.fryr.win.winfryr_client import WinFryR_Client
from apps.ios.iOS_client import IOSClient
from apps.linux.linuxclient import LinuxClient
from apps.mac.macclient import MacClient
from apps.windows.windows_client import Windows_Client


class NativeClientFactory(object):

    # def __init__(self, product="Windows"):
    #     self.product = product
    #     self.client = None
    #     print "Initialize Native Client"

    @staticmethod
    def get_client(product, oem):
        product = product.lower()
        if product == "windows":
            return Windows_Client(oem)
        elif product == "linux":
            return LinuxClient()
            # print "Linux Client"
        elif product == "mac":
            return MacClient(oem)
        elif product == "winfryr":
            return WinFryR_Client()
        elif product == "macfryr":
            return MacFryR_Client()
        elif product == "ios":
            return IOSClient()
        elif product == "android":
            return Android_Client()
        else:
            raise TypeError('Unknown Product.')


if __name__ == "__main__":
    nativeclient = NativeClientFactory.get_client("Windows", "mozypro")
    print nativeclient.controller.mozyutil
    print nativeclient.controller.mozy_daemon
    print nativeclient.controller.service_name
    print nativeclient.controller.install_path
    print nativeclient.controller.data_dir

    print nativeclient.installer.oem

    print nativeclient.cli.current_state()
    nativeclient._cli.start_backup()
    nativeclient._cli.wait_for_state("BACKINGUP")
    nativeclient._cli.cancel_backup()
    nativeclient._cli.wait_for_state("IDLE")

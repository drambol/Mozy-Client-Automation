
from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_settings_element import WindowsSettingsElement

from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil



class WelcomePanel(WindowsUIBase):

    elements = []
    elements.append(WindowsSettingsElement('OKButton', 'OKButton'))

    def __init__(self, oem="mozypro"):
        super(WelcomePanel, self).__init__()


    def get_client_version(self, name="test"):
        pass

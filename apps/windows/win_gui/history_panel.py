
from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_settings_element import WindowsSettingsElement

from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil


class HistoryPanel(WindowsUIBase):

    elements = []
    elements.append(WindowsSettingsElement('ListTreeView', 'ListTreeView'))

    def __init__(self, oem="mozypro"):

        super(HistoryPanel, self).__init__()
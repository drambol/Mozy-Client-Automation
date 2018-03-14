
from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil

from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_savedconfig_element import WindowsSavedConfigElement


class SavedConfigDialog(WindowsUIBase):

    elements = []
    elements.append(WindowsSavedConfigElement('Button1', 'Button1'))   # OK/Yes
    elements.append(WindowsSavedConfigElement('Button2', 'Button2'))   # No

    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"

        print "Initialize Saved Config Dialog"
        super(SavedConfigDialog, self).__init__()


    @property
    def savedconfigdialog(self):
        return self._savedconfigdialog

    @property
    def yesbutton(self):
        return self._yesbutton

    @property
    def nobutton(self):
        return self._nobutton

    def apply(self):
        # self.yesbutton.Click()
        print "Apply Saved Config."
        WindowsGUIUtil.click_button(self.Button1)

    def cancel(self):
        # self.nobutton.Click()
        WindowsGUIUtil.click_button(self.Button2)
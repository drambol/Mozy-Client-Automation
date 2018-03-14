
from apps.windows.win_lib.windows_gui_util import WindowsGUIUtil

from apps.windows.win_gui.windowsui import WindowsUIBase
from apps.windows.win_gui.windows_wizard_element import WindowsWizardElement


class SummaryDialog(WindowsUIBase):

    elements = []
    elements.append(WindowsWizardElement('NextButton', 'NextButton'))
    elements.append(WindowsWizardElement('BackButton', 'BackButton'))
    elements.append(WindowsWizardElement('CancelButton', 'CancelButton'))

    def __init__(self, oem="mozypro"):
        if oem == "mozypro":
            self.oem = "MozyPro"
        else:
            self.oem = "MozyEnterprise"

        print "Initial Summary Dialog"
        super(SummaryDialog, self).__init__()


    def check_quota(self):
        self.limitstatic.window_text()

    @property
    def summarydialog(self):
        return self._summarydialog

    @property
    def gradientpanel(self):
        return self._gradientpanel

    # @property
    # def limitstatic(self):
    #     return self._limitstatic

    @property
    def nextbutton(self):
        return self.summarydialog.NextButton

    @property
    def backbutton(self):
        return self.summarydialog.BackButton

    @property
    def cancelbutton(self):
        return self.summarydialog.CancelButton

    def apply(self):
        # self.nextbutton.Click()
        print "Apply Summary Dialog"
        next_button = self.NextButton
        if WindowsGUIUtil.is_visible(next_button):
            WindowsGUIUtil.click_button(next_button)

    def backup(self):
        # self.backbutton.Click()
        back_button = self.BackButton
        if WindowsGUIUtil.is_visible(back_button):
            WindowsGUIUtil.click_button(back_button)

    def cancel(self):
        # self.cancelbutton.Click()
        cancel_button = self.CancelButton
        if WindowsGUIUtil.is_visible(cancel_button):
            WindowsGUIUtil.click_button(cancel_button)

if __name__ == "__main__":
    summary = SummaryDialog("mozypro")
    # summary.apply()
    WindowsGUIUtil.click_button(summary.BackButton)
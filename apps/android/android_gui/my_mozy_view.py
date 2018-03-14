from apps.android.appium_driver import Driver
from lib.loghelper import LogHelper

class My_Mozy_View(Driver):

    xpaths = {'my_mozy_textview': "//*[@text='My Mozy']",
              'downloaded_image': "//*[@text='Downloaded']",
              'recent_image': "//*[contains(@text, 'Recent')]",
              'photos_image': "//*[contains(@text, 'Photos')]",
              'documents_image': "//*[contains(@text, 'Documents')]",
              'music_image': "//*[contains(@text, 'Music')]",
              'videos_image': "//*[contains(@text, 'Videos')]",
              'machine_info': "//*[@class='android.widget.ListView']//*[@class='android.widget.TextView']"
              }

    @classmethod
    def navigate_to(self):
        try:
            self.locate_element(self.xpaths['my_mozy_textview'], wait_time=1).click()
        except:
            self.press_menu(82)
            self.locate_element(self.xpaths['my_mozy_textview']).click()

    @classmethod
    def verify_downloaded(self):
        self.navigate_to()
        self.locate_element(self.xpaths['downloaded_image']).click()
        assert self.locate_element(self.xpaths['downloaded_image']).is_displayed()
        machine_list = self.locate_elements(self.xpaths['machine_info'])
        machine_count = len(machine_list)
        LogHelper.info(str(machine_count) + " machine(s) listed in Downloaded tab:")
        for i in range(machine_count):
            LogHelper.info("Machine " + str(i) + ": " + machine_list[i].text)

    @classmethod
    def verify_recent(self):
        self.navigate_to()
        self.locate_element(self.xpaths['recent_image']).click()
        assert self.locate_element(self.xpaths['recent_image']).is_displayed()
        machine_list = self.locate_elements(self.xpaths['machine_info'])
        machine_count = len(machine_list)
        LogHelper.info(str(machine_count) + " machine(s) listed in Recent tab:")
        for i in range(machine_count):
            LogHelper.info("Machine " + str(i) + ": " + machine_list[i].text)

    @classmethod
    def verify_photos(self):
        self.navigate_to()
        self.locate_element(self.xpaths['photos_image']).click()
        assert self.locate_element(self.xpaths['photos_image']).is_displayed()
        machine_list = self.locate_elements(self.xpaths['machine_info'])
        machine_count = len(machine_list)
        LogHelper.info(str(machine_count) + " machine(s) listed in Downloaded tab:")
        for i in range(machine_count):
            LogHelper.info("Machine " + str(i) + ": " + machine_list[i].text)

    @classmethod
    def verify_documents(self):
        self.navigate_to()
        self.locate_element(self.xpaths['documents_image']).click()
        assert self.locate_element(self.xpaths['documents_image']).is_displayed()
        machine_list = self.locate_elements(self.xpaths['machine_info'])
        machine_count = len(machine_list)
        LogHelper.info(str(machine_count) + " machine(s) listed in Documents tab:")
        for i in range(machine_count):
            LogHelper.info("Machine " + str(i) + ": " + machine_list[i].text)

    @classmethod
    def verify_music(self):
        self.navigate_to()
        self.locate_element(self.xpaths['music_image']).click()
        assert self.locate_element(self.xpaths['music_image']).is_displayed()
        machine_list = self.locate_elements(self.xpaths['machine_info'])
        machine_count = len(machine_list)
        LogHelper.info(str(machine_count) + " machine(s) listed in Music tab:")
        for i in range(machine_count):
            LogHelper.info("Machine " + str(i) + ": " + machine_list[i].text)

    @classmethod
    def verify_videos(self):
        self.navigate_to()
        self.locate_element(self.xpaths['videos_image']).click()
        assert self.locate_element(self.xpaths['videos_image']).is_displayed()
        machine_list = self.locate_elements(self.xpaths['machine_info'])
        machine_count = len(machine_list)
        LogHelper.info(str(machine_count) + " machine(s) listed in Videos tab:")
        for i in range(machine_count):
            LogHelper.info("Machine " + str(i) + ": " + machine_list[i].text)
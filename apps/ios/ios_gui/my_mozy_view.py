from apps.ios.appium_driver import Driver
from lib.loghelper import LogHelper

class My_Mozy_View(Driver):

    xpaths = {'my_mozy_textview': "//*[@label='My Mozy']",
              'history_image': "//*[@label='History']",
              'history_info': "//*[@label='You have not viewed any files.']",
              'recent_image': "//*[@label='Recent']",
              'recent_title': "//*[@label='Recent File Updates']",
              'recent_machines': "//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIATableGroup",
              'machine_descriptions': "//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIATableCell",
              'photos_image': "//*[@label='Photos']",
              'documents_image': "//*[@label='Documents']",
              'music_image': "//*[@label='Music']",
              'videos_image': "//*[@label='Videos']",
              'machine_info': "//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIATableCell",
              }

    @classmethod
    def navigate_to(self):
        try:
            self.locate_element(self.xpaths['my_mozy_textview'], wait_time=1).click()
        except:
            pass

    @classmethod
    def verify_history(self):
        self.navigate_to()
        self.locate_element(self.xpaths['history_image']).click()
        assert self.locate_element(self.xpaths['history_image']).is_displayed()
        assert self.locate_element(self.xpaths['history_info']).is_displayed()
        LogHelper.info("History Info: " + self.locate_element(self.xpaths['history_info']).text)
        print("History Info: " + self.locate_element(self.xpaths['history_info']).text)

    @classmethod
    def verify_recent(self):
        self.navigate_to()
        self.locate_element(self.xpaths['recent_image']).click()
        assert self.locate_element(self.xpaths['recent_title']).is_displayed()
        machine_list = self.locate_elements(self.xpaths['recent_machines'])
        machine_count = len(machine_list)
        LogHelper.info(str(machine_count) + " machine(s) listed in Recent tab:")
        for i in range(machine_count):
            num = str(i + 1)
            machine_xpath = self.xpaths['recent_machines'] + "[" + num + "]/UIAStaticText[1]"
            machine_name = self.locate_element(machine_xpath).text
            LogHelper.info("Machine " + num + ": " + machine_name)
            print("Machine " + num + ": " + machine_name)
            description_xpath = self.xpaths['machine_descriptions'] + "[" + num + "]/UIAStaticText[1]"
            machine_description = self.locate_element(description_xpath).text
            LogHelper.info("Last backup: " + machine_description)
            print("Last backup: " + machine_description)

    @classmethod
    def verify_photos(self):
        self.navigate_to()
        self.locate_element(self.xpaths['photos_image']).click()
        assert self.locate_element(self.xpaths['photos_image']).is_displayed()
        machine_list = self.locate_elements(self.xpaths['machine_info'])
        machine_count = len(machine_list)
        LogHelper.info(str(machine_count) + " machine(s) listed in Photos tab:")
        for i in range(machine_count):
            num = str(i + 1)
            machine_xpath = self.xpaths['machine_info'] + "[" + num + "]/UIAStaticText[1]"
            machine_name = self.locate_element(machine_xpath).text
            LogHelper.info("Photo Machine " + num + ": " + machine_name)
            print("Photo Machine " + num + ": " + machine_name)

    @classmethod
    def verify_documents(self):
        self.navigate_to()
        self.locate_element(self.xpaths['documents_image']).click()
        assert self.locate_element(self.xpaths['documents_image']).is_displayed()
        machine_list = self.locate_elements(self.xpaths['machine_info'])
        machine_count = len(machine_list)
        LogHelper.info(str(machine_count) + " machine(s) listed in Documents tab:")
        for i in range(machine_count):
            num = str(i + 1)
            machine_xpath = self.xpaths['machine_info'] + "[" + num + "]/UIAStaticText[1]"
            machine_name = self.locate_element(machine_xpath).text
            LogHelper.info("Document Machine " + num + ": " + machine_name)
            print("Document Machine " + num + ": " + machine_name)

    @classmethod
    def verify_music(self):
        self.navigate_to()
        self.locate_element(self.xpaths['music_image']).click()
        assert self.locate_element(self.xpaths['music_image']).is_displayed()
        machine_list = self.locate_elements(self.xpaths['machine_info'])
        machine_count = len(machine_list)
        LogHelper.info(str(machine_count) + " machine(s) listed in Music tab:")
        for i in range(machine_count):
            num = str(i + 1)
            machine_xpath = self.xpaths['machine_info'] + "[" + num + "]/UIAStaticText[1]"
            machine_name = self.locate_element(machine_xpath).text
            LogHelper.info("Music Machine " + num + ": " + machine_name)
            print("Music Machine " + num + ": " + machine_name)

    @classmethod
    def verify_videos(self):
        self.navigate_to()
        self.locate_element(self.xpaths['videos_image']).click()
        assert self.locate_element(self.xpaths['videos_image']).is_displayed()
        machine_list = self.locate_elements(self.xpaths['machine_info'])
        machine_count = len(machine_list)
        LogHelper.info(str(machine_count) + " machine(s) listed in Videos tab:")
        for i in range(machine_count):
            num = str(i + 1)
            machine_xpath = self.xpaths['machine_info'] + "[" + num + "]/UIAStaticText[1]"
            machine_name = self.locate_element(machine_xpath).text
            LogHelper.info("Videos Machine " + num + ": " + machine_name)
            print("Videos Machine " + num + ": " + machine_name)
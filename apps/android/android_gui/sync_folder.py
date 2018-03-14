from apps.android.appium_driver import Driver
from apps.android.android_gui.all_files import All_Files_View
from lib.loghelper import LogHelper

class Sync_View(Driver):

    xpaths = {'sync_textview': "//*[@text='Sync']",
              'search_sync_textfield': "//*[@text='Search Sync']",
              'search_sync_title': "//*[@text='Search Results in Sync']",
              'sync_files': "//*[@class='android.widget.ListView']/*[@class='android.widget.LinearLayout']",
              'sync_file_name': "//*[@class='android.widget.TextView']",
              'sync_file_description': "//*[@class='android.widget.TextView']/following-sibling::*[1]",
              'search_result_list': "//*[@class='android.widget.ListView']",
              'search_no_result': "//*[contains(@text, 'Mozy Sync')]",
              'search_files': "//*[@class='android.widget.ListView']/*[@class='android.widget.LinearLayout']",
              }

    @classmethod
    def navigate_to(self):
        if self.is_element_exists(self.xpaths['search_sync_title'], wait_time=1):
            return
        try:
            self.locate_elements(self.xpaths['sync_textview'], wait_time=1)[-1].click()
        except:
            All_Files_View.navigate_to()
            self.locate_elements(self.xpaths['sync_textview'])[-1].click()
        assert self.locate_element(self.xpaths['search_sync_textfield']).is_displayed()

    @classmethod
    def verify_sync_files(self):
        folder_list = self.locate_elements(self.xpaths['sync_files'])
        for folder in folder_list:
            sync_file = folder.find_element_by_xpath(self.xpaths['sync_file_name']).text
            try:
                sync_description = folder.find_element_by_xpath(self.xpaths['sync_file_description']).text
            except:
                sync_description = '(Directory)' # sync description will not display when it is a directory
            LogHelper.info('Sync Item: ' + sync_file + ' ' + sync_description)

    @classmethod
    def verify_search_function(self, search_criteria='.pdf'):
        self.locate_element(self.xpaths['search_sync_textfield']).send_keys(search_criteria)
        search_sync_image = "//*[@text='" + search_criteria + "']/following-sibling::*[1]"
        self.locate_element(search_sync_image).click()
        try:
            self.locate_element(self.xpaths['search_result_list']).is_displayed()
            search_file_list = self.locate_elements(self.xpaths['search_files'], wait_time=1)
            file_count = len(search_file_list)
            LogHelper.info('Search result with keyword: ' + search_criteria)
            for i in range(file_count):
                file_name = search_file_list[i].find_element_by_xpath("//*[@class='android.widget.TextView']").text
                file_description = search_file_list[i].find_element_by_xpath("//*[@class='android.widget.TextView']/following-sibling::*[1]").text
                LogHelper.info('    ' + file_name)
                LogHelper.info('        ' + file_description)
        except:
            self.locate_element(self.xpaths['search_no_result']).is_displayed()
            LogHelper.info('No search result found with keyword: ' + search_criteria)
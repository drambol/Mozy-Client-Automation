from apps.ios.appium_driver import Driver
from apps.ios.ios_gui.all_files import All_Files_View
from lib.loghelper import LogHelper

class Sync_View(Driver):

    keyword = ''
    search_index = 0
    xpaths = {'sync_textview': "//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIATableCell[1]/UIAStaticText[1]",
              'search_sync_textfield': "//UIASearchBar",
              'search_sync_title': "//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIASearchBar[1]",
              'sync_files': "//UIATableView[1]/UIATableCell",
              'search_result_tag': "//UIAElement[contains(@label, 'More Info')]",
              'search_no_result': "//*[contains(@text, 'Mozy Sync')]",
              'search_result_list': "//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIATableGroup",
              'search_files': "//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIATableCell",
              }

    @classmethod
    def navigate_to(self):
        try:
            self.locate_element(self.xpaths['sync_textview']).click()
        except:
            All_Files_View.navigate_to()
            self.locate_element(self.xpaths['sync_textview']).click()
        assert self.locate_element(self.xpaths['search_sync_textfield'], 60).is_displayed()

    @classmethod
    def verify_sync_files(self):
        folder_list = self.locate_elements(self.xpaths['sync_files'])
        for index, folder in enumerate(folder_list):
            file_xpath = self.xpaths['sync_files'] + "[" + str(index + 1) + "]/UIAStaticText[1]"
            file_name = self.driver.find_element_by_xpath(file_xpath).text
            try:
                description_xpath = self.xpaths['sync_files'] + "[" + str(index + 1) + "]/UIAStaticText[2]"
                file_description = self.driver.find_element_by_xpath(description_xpath).text
            except:
                file_description = '(Directory)' # sync description will not display when it is a directory
            LogHelper.info('Sync Item: ' + file_name + ' ' + file_description)
            print('Sync Item: ' + file_name + ' ' + file_description)

    @classmethod
    def verify_search_function(self, search_criteria='.pdf'):
        self.search_index = search_criteria
        if self.search_index == 3:
            LogHelper.info('No search result found with keyword: ' + search_criteria)
            raise Exception("No search result found with keyword: " + search_criteria)
            return
        LogHelper.info('===Start search case in Sync folder, keyword=' + search_criteria + '===')
        print('===Start search case in Sync folder, keyword=' + search_criteria + '===')
        self.locate_element(self.xpaths['search_sync_textfield']).send_keys(search_criteria + "\n")
        try:
            self.locate_element(self.xpaths['search_result_tag'], wait_time=90).is_displayed()
            search_file_list = self.locate_elements(self.xpaths['search_result_list'], wait_time=1)
            LogHelper.info('Search result with keyword: ' + search_criteria)
            for index1, node1 in enumerate(search_file_list):
                current_xpath = self.xpaths['search_result_list'] + "[" + str(index1 + 1) + "]/UIAStaticText[1]"
                current_directory = self.driver.find_element_by_xpath(current_xpath).text
                LogHelper.info("Search keyword found in folder: " + current_directory)
                print("Search keyword found in folder: " + current_directory)
                for index2 in range(10):
                    next_sibling_xpath = self.xpaths['search_result_list'] + "[" + str(index1 + 1) + "]/following-sibling::*[" + str(index2 + 1) + "]"
                    try:
                        xpath_tag = self.driver.find_element_by_xpath(next_sibling_xpath).tag_name
                        if xpath_tag == 'UIATableCell':
                            file_xpath = next_sibling_xpath + "/UIAStaticText[1]"
                            file_name = self.driver.find_element_by_xpath(file_xpath).text
                            description_xpath = next_sibling_xpath + "/UIAStaticText[2]"
                            file_description = self.driver.find_element_by_xpath(description_xpath).text
                            LogHelper.info('    ' + file_name)
                            print('    ' + file_name)
                            LogHelper.info('        ' + file_description)
                            print('        ' + file_description)
                        else:
                            break
                    except:
                        LogHelper.info('===End search case in Sync folder===')
                        print('===End search case in Sync folder===')
                        break
        except:
            self.search_index = self.search_index + 1
            self.navigate_to()
            self.verify_search_function(self.keyword)
        pass
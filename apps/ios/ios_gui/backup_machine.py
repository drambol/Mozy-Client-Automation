from apps.ios.appium_driver import Driver
from apps.ios.ios_gui.all_files import All_Files_View
from lib.loghelper import LogHelper

class Machine_View(Driver):

    machine_name = ''
    keyword = ''
    machine_index = 0
    search_index = 0
    xpaths = {'machine_list': "//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIATableCell",
              'folder_list': "//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIATableCell",
              'search_textfield': "//UIASearchBar",
              'search_result_list': "//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIATableGroup",
              'search_no_result': "//*[contains(@text, 'No items found')]",
              'search_files': "//*[@class='android.widget.ListView']/*[@class='android.widget.LinearLayout']",
              }

    @classmethod
    def get_machine_quantity(self):
        All_Files_View.navigate_to()
        machine_list = self.locate_elements(self.xpaths['machine_list'])
        machine_quantity = len(machine_list) - 1
        return machine_quantity

    @classmethod
    def navigate_to(self, index=0):
        self.machine_index = index
        All_Files_View.navigate_to()
        if All_Files_View.machines == []:
            machines = All_Files_View.verify_backups()
        else:
            machines = All_Files_View.machines
        self.machine_name = machines[index].name
        LogHelper.info('View backup machine: ' + self.machine_name)
        print('View backup machine: ' + self.machine_name)
        self.locate_element("//*[@label='" + self.machine_name + "']").click()

    @classmethod
    def verify_ui(self):
        for i in range(3):
            try:
                self.locate_element(self.xpaths['folder_list'], wait_time=60).is_displayed()
                LogHelper.info('Folder list is displayed for ' + self.machine_name)
                return
            except:
                self.navigate_to(self.machine_index)
        LogHelper.error('Folder list is not displayed for ' + self.machine_name)
        raise AssertionError('Folder list is not displayed for ' + self.machine_name)

    @classmethod
    def verify_search_function(self, search_criteria='.pdf'):
        self.keyword = search_criteria
        if self.search_index == 3:
            LogHelper.info('No search result found with keyword: ' + search_criteria)
            raise Exception("No search result found with keyword: " + search_criteria)
            return
        LogHelper.info('===Start search case in ' + self.machine_name + ', keyword=' + search_criteria + '===')
        print('===Start search case in ' + self.machine_name + ', keyword=' + search_criteria + '===')
        self.locate_element(self.xpaths['search_textfield']).send_keys(search_criteria + "\n")
        try:
            self.locate_element(self.xpaths['search_result_list'], wait_time=60).is_displayed()
            search_file_list = self.locate_elements(self.xpaths['search_result_list'], wait_time=1)
            LogHelper.info('Search in ' + self.machine_name + ' with keyword: ' + search_criteria)
            print('Search in ' + self.machine_name + ' with keyword: ' + search_criteria)
            for index1, node1 in enumerate(search_file_list):
                try:
                    current_xpath = self.xpaths['search_result_list'] + "[" + str(index1 + 1) + "]/UIAStaticText[1]"
                    current_directory = self.driver.find_element_by_xpath(current_xpath).text
                    LogHelper.info("Search keyword found in folder: " + current_directory)
                    print("Search keyword found in folder: " + current_directory)
                    for index2 in range(100):
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
                            break
                except:
                    break
                LogHelper.info('===End search case in ' + self.machine_name + '===')
                print('===End search case in ' + self.machine_name + '===')
        except:
            self.search_index = self.search_index + 1
            self.navigate_to(self.machine_index)
            self.verify_search_function(self.keyword)
        pass
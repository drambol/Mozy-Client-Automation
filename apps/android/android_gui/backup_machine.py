from apps.android.appium_driver import Driver
from apps.android.android_gui.all_files import All_Files_View
from lib.loghelper import LogHelper

class Machine_View(Driver):

    machine_name = ''
    xpaths = {'machine_list': "//*[@class='android.widget.ListView']/*[@class='android.widget.RelativeLayout']",
              'folder_list': "//*[@class='android.widget.ListView']",
              'search_textfield': "//*[@class='android.widget.EditText']",
              'search_image': "//*[@class='android.widget.EditText']/following-sibling::*[1]",
              'search_result_list': "//*[@class='android.widget.ListView']",
              'search_no_result': "//*[contains(@text, 'No items found')]",
              'search_files': "//*[@class='android.widget.ListView']/*[@class='android.widget.LinearLayout']",
              }

    @classmethod
    def get_machine_quantity(self):
        machine_list = self.locate_elements(self.xpaths['machine_list'])
        machine_quantity = len(machine_list) - 1
        return machine_quantity

    @classmethod
    def navigate_to(self, index=0):
        All_Files_View.navigate_to()
        machines = All_Files_View.verify_backups()
        self.machine_name = machines[index].name
        LogHelper.info('View backup machine: ' + self.machine_name)
        self.locate_element("//*[@text='" + self.machine_name + "']").click()

    @classmethod
    def verify_ui(self):
        try:
            self.locate_element(self.xpaths['folder_list']).is_displayed()
            LogHelper.info('Folder list is displayed for ' + self.machine_name)
        except:
            LogHelper.error('Folder list is not displayed for ' + self.machine_name)
            raise AssertionError('Folder list is not displayed for ' + self.machine_name)

    @classmethod
    def verify_search_function(self, search_criteria='.pdf'):
        self.locate_element(self.xpaths['search_textfield']).send_keys(search_criteria)
        self.locate_element(self.xpaths['search_image']).click()
        try:
            self.locate_element(self.xpaths['search_result_list'], wait_time=20).is_displayed()
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
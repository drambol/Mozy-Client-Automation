import os, re, subprocess, time, platform
from datetime import datetime
from apps.web_support.base_page import Page
from configuration.fryr.fryr_config_loader import FRYR_CONFIG
from configuration.config_adapter import ConfigAdapter

from lib.loghelper import LogHelper
from lib.kpihelper import KPIHelper

class FreyjaPage(Page):

    def __init__(self):
        pass

    xpaths = {'deviceTab': "//li[@id='backup_tab_button']/a",
              'selectAllCB': "//span[@title='Select all']",
              'restoreName': "//form[@id='restore_form']//input[@id='restore_name']",
              'restoreNextBtn': "//form[@id='restore_form']//div[text()='Next']",
              'mzdRadioBtn': "//form[@id='restore_form']//span[@id='choose_delivery_method_download_manager']",
              'archiveRadioBtn': "//form[@id='restore_form']//span[@id='choose_delivery_method_archive']",
              'arrowLink': "//div[@id='menu-user']/div[@class='arrow']",
              'eventHistoryLink': "//li[@id='panel-action-event-history']",
              'eventItems': "//div[text()='Ready for Download']",
              # 'eventItems': "//div[text()='Downloaded']",
              'downloadArchiveLink': "//div[@class='download_links']/a",
              'downloadFryRLink': "//table[@class='wizard-steps']//a[@id='download_download_manager_link']",
              'skipDownloadLink': "//form[@id='restore_form']//a[contains(text(), 'If Mozy Restore Manager is already installed')]",
              'beginDownloadBtn': "//form[@id='restore_form']//div[text()='Begin Download']",
              'closeBtn': "//div[text()='Close']",
              'downloadBtn': "//div[@id='backup_tab']//span[text()='Download']",
              'noticeDialog': "//span[text()='OK']",
              'actionPanel': "//div[@title='View Actions pane']",
              'downloadNowBtn': "//div[text()='Download Now...']",

              # LSH eDiscovery Page
              'search_input': "//input[@id='search-input']",
              'search_icon': "//div[@class='search-magnify-icon icon-search-filter']",
              'select_all': "//span[@title='Select all']",
              'view_action_pane': "//div[@title='View Actions pane']",
              'export_selected': "//div[text()='Export Selected...']",
              'export_name': "//form[@id='export_form']//input[@id='export_name']",
              'export_next_btn': "//form[@id='export_form']//div[text()='Next']",
              'skip_download_link': "//form[@id='export_form']//a[contains(text(), 'If Mozy Restore Manager is already installed')]",
              'begin_download_btn': "//form[@id='export_form']//div[text()='Begin Download']"
              }

    @classmethod
    def select_restore(self, table):
        self.driver = Page.current_driver()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.locate_element(self.xpaths['deviceTab']).click()
        machine_xpath = "//span[text()='" + table[0].get('restore_machine') + "']"
        self.wait_for_element_list(machine_xpath, 1).click()
        self.dig_to_folder(table[0].get('folder_hierarchy'))
        for row in table:
            xpath = "//tr[contains(@id, '" + row.get('restore_item') + "')]/td[@class='center col col-checkbox']//span"
            self.delayed_click(xpath)
        if platform.system() == "Windows":
            right_click_target = "//tr[contains(@id, '" + table[-1].get('restore_item') + "')]/td[@class='center col col-checkbox']//span"
            self.select_menu(right_click_target, 'Large Download Options...')
        else:
            try:
                self.locate_element('//div[text()="Large Download Options..."]').click()
            except:
                self.locate_element('//div[contains(@class, "panel-toggle") and @title="View Actions pane"]').click()
                self.locate_element('//div[text()="Large Download Options..."]').click()
        # pass

    @classmethod
    def create_mzd(self):
        try:
            self.locate_element(self.xpaths['restoreName']).click()
            time.sleep(1)
            self.locate_element(self.xpaths['restoreName']).send_keys(FRYR_CONFIG['RESTORE']['MZD_TAG'])
            self.locate_element(self.xpaths['restoreNextBtn']).click()
            self.locate_element(self.xpaths['mzdRadioBtn']).click()
            self.locate_element(self.xpaths['restoreNextBtn']).click()

            skip_btn = self.is_element_exist(self.xpaths['skipDownloadLink'], 10)
            if skip_btn:
                skip_btn.click()
            else:
                el = self.is_element_exist(self.xpaths['downloadFryRLink'], 2)
                if el:
                    el.click()

            self.locate_element(self.xpaths['beginDownloadBtn']).click()
            time.sleep(5)
            self.locate_element(self.xpaths['closeBtn']).click()

            return True
        except Exception, e:
            LogHelper.error(repr(e))
            LogHelper.error("Fail to create mzd file.")
            return False

    @classmethod
    def create_archive(self):
        try:
            self.locate_element(self.xpaths['restoreName']).send_keys(FRYR_CONFIG['RESTORE']['MZD_TAG'])
            self.locate_element(self.xpaths['restoreNextBtn']).click()
            self.locate_element(self.xpaths['archiveRadioBtn']).click()
            self.locate_element(self.xpaths['restoreNextBtn']).click()
            self.locate_element(self.xpaths['closeBtn']).click()
            # Here we need to wait some time for Freyja to prepare the archive package.
            time.sleep(60)
            self.locate_element(self.xpaths['arrowLink']).click()
            self.locate_element(self.xpaths['eventHistoryLink']).click()
            self.delayed_click(self.xpaths['eventItems'], sleep_time=3)
            self.locate_element(self.xpaths['downloadArchiveLink']).click()
            # Here we need to wait for download complete
            result = self.wait_for_download_complete()

            return result
        except Exception:
            LogHelper.error("Fail to create archive.")
            return False

    @classmethod
    def direct_download(self, table):
        try:
            self.driver = Page.create_browser()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.locate_element(self.xpaths['deviceTab']).click()
            machine_xpath = "//span[text()='" + table[0].get('restore_machine') + "']"
            self.wait_for_element_list(machine_xpath, 1).click()
            self.dig_to_folder(table[0].get('folder_hierarchy'))
            for row in table:
                xpath = "//tr[contains(@id, '" + row.get('restore_item') + "')]/td[@class='center col col-checkbox']//span"
                self.delayed_click(xpath)
            self.delayed_click(self.xpaths['downloadBtn'])
            self.delayed_click(self.xpaths['noticeDialog'], -1)
            result = self.wait_for_download_complete()

            return result
        except Exception:
            LogHelper.error("Fail to direct download.")
            return False

    @classmethod
    def download_now(self):
        """
        click download now button in Action Panel 
        :return: 
        """
        try:
            download_now_btn_xpath = self.xpaths['downloadNowBtn']
            if self.is_element_exist(download_now_btn_xpath,1) is None:
                #Action Panel is not visible
                Page.delayed_click(self.xpaths['actionPanel'])

            self.delayed_click(download_now_btn_xpath)
            # cls.delayed_click(cls.xpaths['noticeDialog'], -1)
            result = self.wait_for_download_complete()

            return result
        except Exception:
            LogHelper.error("Fail to instant download.")
            return False


    @classmethod
    def close_browser(self):
        time.sleep(3)
        self.driver = None
        Page.driver.quit()
        Page.driver = None

    @staticmethod
    def dig_to_folder(folders):
        time.sleep(3)
        folder_hierarchy = folders.split('/')
        try:
            for folder_name in folder_hierarchy:
                if folder_name == '':
                    folder_name = '/'
                target_folder = "//span[text()='" + folder_name + "']"
                Page.delayed_click(target_folder)
            return True

        except Exception:
            LogHelper.error("Fail to dig folder.")
            return False

    @staticmethod
    def drill_down_folders(folder_list):
        try:
            for folder_name in folder_list:
                target_folder = "//span[text()='" + folder_name + "']"
                LogHelper.info("Try to click '%s'"%target_folder)
                Page.delayed_click(target_folder)
            return True

        except Exception:
            LogHelper.error("Fail to drill down folder.")
            return False

    @classmethod
    def click_machine(self, name):
        xpath_for_machine = "//table[@id='dt-backuplist']//tr[contains(@class,'table-row')]//span[@class='name']"
        try:
            els = self.locate_elements(xpath_for_machine, wait_time=120)

            for el in els:
                LogHelper.info(el.text)
                if el.text.upper().find(name)>=0:
                    el.click()
                    LogHelper.info("Find the correct machine.")
                    return True

        except Exception:
            LogHelper.error("Fail to click machine.")
            return False

    @classmethod
    def get_machine_list(self):
        xpath_for_machine="//table[@id='dt-backuplist']//tr[contains(@class,'table-row')]//span[@class='name']"
        try:
            els = self.locate_element(xpath_for_machine)
            machine_name = []
            for el in els:
               machine_name.append(el.text)
            return machine_name

        except Exception:
            LogHelper.error("Fail to get machine list.")
            return False


    @classmethod
    def check_entity(self, entity_name):
        """
        in Freyja main page, check a dir or files by its name
        :param entity_name:
        :return:
        """
        #check minus
        #right_click_target = "//tr[contains(@id, '\"{entity_name}\"')]/td[@class='center col col-checkbox']//span".format(entity_name=entity_name)
        #right_click_target = "//span[text()='" + entity_name + "']"
        cb_target = '//tr[contains(@id, "{entity_name}")]/td[1]/div/span[contains(@class, "check")]'.format(entity_name=entity_name)
        LogHelper.info(cb_target)
        try:
            self.locate_element(cb_target).click()
            actionPanel = self.locate_element('//div[contains(@class, "panel-toggle") and @title="View Actions pane"]')
            LogHelper.info(str(actionPanel))
            actionPanel.click()
            self.locate_element('//div[text()="Large Download Options..."]').click()
            return True
        except Exception:
            LogHelper.error("Fail to click Large Download Options.")
            return False

    @staticmethod
    def wait_for_download_complete():
        time.sleep(10) # This is to wait the download process to start
        download_path = ConfigAdapter.get_testdata_path().replace("\\\\", "\\")
        temp_file = ''
        for file in os.listdir(download_path):
            if re.match(r'restore_.*\.part$', file):
                temp_file = os.path.join(download_path, file)
        if temp_file == '':
            # KPIHelper.log_error(category="Web", kpiname="Download", result="SUCCESS", message="Download Completed.")
            LogHelper.info('Download Completed!')
            return True
        else:
            time.sleep(5)
            for i in range(100):
                if os.path.isfile(temp_file):
                    time.sleep(4)
                else:
                    # KPIHelper.log_error(category="Web", kpiname="Download", result="SUCCESS", message="Download Completed.")
                    LogHelper.info('Download Completed!')
                    return True

            # KPIHelper.log_error(category="Web", kpiname="Download", result="Fail", message="Timeout.")
            LogHelper.error('ERROR: Download Failed!')

            return False

    @classmethod
    def define_lsh_search(self, search_text):
        self.driver = Page.current_driver()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.locate_element(self.xpaths['search_input']).send_keys(search_text)
        self.locate_element(self.xpaths['search_icon']).click()

    @classmethod
    def create_mzdx(self):
        self.locate_element(self.xpaths['select_all']).click()
        try:
            self.locate_element(self.xpaths['export_selected'], wait_time=5).click()
        except Exception:
            self.locate_element(self.xpaths['view_action_pane']).click()
            self.locate_element(self.xpaths['export_selected']).click()
        export_tag = "Auto_export: " + datetime.now().strftime('%Y%m%d_%H%M%S')
        self.locate_element(self.xpaths['export_name']).send_keys(export_tag)
        self.locate_element(self.xpaths['export_next_btn']).click()
        time.sleep(3)
        self.locate_element(self.xpaths['export_next_btn']).click()
        skip_btn = self.is_element_exist(self.xpaths['skip_download_link'], 6)
        if skip_btn:
            skip_btn.click()
        self.locate_element(self.xpaths['begin_download_btn']).click()
        self.delayed_click(self.xpaths['closeBtn'], sleep_time=5)
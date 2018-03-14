from selenium.webdriver.support import expected_conditions  as EC

from apps.web_support.base_page import Page
from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.runner_config_loader import RUNNER_CONFIG
from selenium.webdriver.support.ui import Select
from lib.loghelper import LogHelper
from lib.kpihelper import KPIHelper

class BusPage(Page):

    bus_driver = None

    xpaths = {
              'loginfield': ".//*[@id='loginfieldsbox']",
              'usernameTxtBox': ".//input[@id='username']",
              'passwordTxtBox': "//input[@id='password']",
              'submitLogin': "//span[@class='login_button']",
              'searchTxtBox': "//input[@id='user_search']",
              'submitSearch': "//input[@id='user_search']/following-sibling::input[@name='commit']",
              'userLink': "//div[@id='user-list-content']//table[@class='table-view']/tbody//a",
              'folderIcon': "//i[@class='icon-folder-open-alt icon-2x']",
              # Section: Search List Partner
              'partnerSearchTxtBox':"//input[@id='pro_partner_search']",
              'partnerSubmitSearch':"//input[@id='pro_partner_search']/following-sibling::input[@name='commit']",
              'partnerLink': "//div[@id='partner-list-content']//table[@class='table-view']/tbody//a",
              # Section: partner detail section
              'act_as_link': "//a[text()='act as']",

              # start using mozy dialog
              'start_using_mozy_btn':"//button[@id='start_using_mozy']",

              # client configuration section
              'client_configuration_link':"//a[text()='Client Configuration']",
              'iframe_tg': "//iframe",
              'config_name_tb':"//input[@id='config_name']",
              'config_license_type_id_select':"//select[@id='config_license_type_id']",
              'config_next_btn':"//input[@value='Next']",

              # tabs when create config
              # Preference Tab
              'Preferences':"//div[contains(@id,'setting-edit_client_config')]/ul/li[1]",
              'user_choose_encryption':"//input[@id='userinfo.allowed_encryption_key_sources.choice']",
              'user_choose_default':"//input[@id='userinfo.allowed_encryption_key_sources.default']",
              'user_choose_random':"//input[@id='userinfo.allowed_encryption_key_sources.random']",
              'user_choose_pkey':"//input[@id='userinfo.allowed_encryption_key_sources.custom']",
              'user_choose_ckey':"//input[@id='userinfo.allowed_encryption_key_sources.adminurl']",

              # Allow export PKey
              'allow_export_pkey': "//input[@id='userinfo.prompt_save_encryption_key_sources.custom']",
              # Allow export Random Key
              'allow_export_randomkey': "//input[@id='userinfo.prompt_save_encryption_key_sources.random']",
              'allow_export_escrow': "//input[@id='userinfo.escrow_encryption_key_sources.random']",
              'allow_export_both': "//input[@id='userinfo.escrow_and_export_encryption_key_sources.random']",
              # Set Ckey URL/Path
              'ckey_url':"//input[@id='userinfo.encryption_key_url']",
              # Select KMIP
              'user_choose_kmip':"//input[@id='userinfo.allowed_encryption_key_sources.kmip']",
              'kmip_address':"//input[@id='userinfo.kmip_kms_address']",
              'kmip_port':"//input[@id='userinfo.kmip_kms_port']",
              'kmip_naeport':"//input[@id='userinfo.kmip_kms_nae_port']",
              'kmip_cert_issuer':"//input[@id='userinfo.kmip_client_cert_issuer']",
              'kmip_group':"//input[@id='userinfo.kmip_group_names']",

              # Enforce encryption
              'enforce_encryption':"//input[@id='options.enforce_encryption_type']",
              'enforce_encryption_cascade':"//input[@id='options.enforce_encryption_type_cascade']",


              # Scheduling Tab
              'scheduling_tab': "//div[contains(@id,'setting-edit_client_config')]/ul/li[2]",
              # Bandwidth Tab
              'bandwidth_throttling_tab': "//div[contains(@id,'setting-edit_client_config')]/ul/li[3]",
              'throttle_cb': 'throttle_checkbox',
              'throttle_amount_tb': 'throttle_kbps',
              # Windows Backup Set Tab
              'windows_backup_sets': "//div[contains(@id,'setting-edit_client_config')]/ul/li[4]",
              'all_settings_check_boxes': "//div[@id='backupsets']/table/tbody/tr[2]/td[2]",
              # Mac Backup Set Tab
              'mac_backup_sets': "//div[contains(@id,'setting-edit_client_config')]/ul/li[5]",

              # User Groups Tab
              'user_groups': "//div[contains(@id,'setting-edit_client_config')]/ul/li[text()='User Groups']",
              'add_user_groups': "//div[@id='config-user-groups']/p[2]/a",
              'choose_user_groups': "//div[@id='config-user-groups']/table/tbody/tr[3]/td/label/input",
              'save_changes_btn': "//input[@value='Save Changes']",

              # eDiscovery
              'eDiscovery_link': "//a[text()='eDiscovery']",
              'define_new_search_btn': "//input[@value='Define New Search']"
              }

    @classmethod
    def openbrowser(self):
        try:
            self.bus_driver = Page.create_browser()
        except Exception:
            LogHelper.error("Can't open browser.")
            return False

    @classmethod
    def visit(self):
        env = RUNNER_CONFIG.get('ENVIRONMENT') or 'QA12'
        bushost = GLOBAL_CONFIG.get('QA_ENVIRONMENT').get(env).get('mozy.bushost') or 'www.mozypro.com'
        if not bushost.startswith('https://'):
            bus_url = "https://{bushost}/login/admin?old_school=1".format(bushost=bushost)
        else:
            bus_url = "{bushost}/login/admin?old_school=1".format(bushost=bushost)

        self.bus_driver = Page.create_browser()
        self.bus_driver.set_page_load_timeout(30)

        result = False

        try:
            self.bus_driver.get(bus_url)

        except Exception:
            LogHelper.error("Can't access BUS.")
            # Page.quit()
            return result
        else:
            # If page is opened successfully
            result = Page.is_element_exist(self.xpaths['loginfield'], wait_time=40)
            return result

    @classmethod
    def login(self, username=None, password=None):
        env = RUNNER_CONFIG.get('ENVIRONMENT') or 'QA12'
        username = username or GLOBAL_CONFIG.get('QA_ENVIRONMENT').get(env).get('bus_admin')
        password = password or GLOBAL_CONFIG.get('QA_ENVIRONMENT').get(env).get('bus_admin_password')

        try:
            Page.locate_element(self.xpaths['usernameTxtBox']).send_keys(username)
            Page.locate_element(self.xpaths['passwordTxtBox']).send_keys(password)
            el=Page.locate_element(self.xpaths['submitLogin'])
            el.click()
            return True
        except Exception:
            LogHelper.error("Can't login BUS.")
            # Page.quit()
            return False

    @classmethod
    def search_user(self, username = None):
        result = False
        try:
            el = Page.locate_element(self.xpaths['searchTxtBox'])
            if el is None:
                LogHelper.error("Fail to locate search user text box.")
            else:
                el.send_keys(username)
                el = Page.locate_element(self.xpaths['submitSearch'])
                if el is None:
                    LogHelper.error("Fail to locate search user button.")
                else:
                    el.click()
                    result = Page.delayed_click(self.xpaths['userLink'], 0, 10)
        except Exception:
            LogHelper.error("Search user failed.")
        finally:
            return result

    @classmethod
    def select_folder(self):
        try:
            Page.wait_for_element_list(self.xpaths['folderIcon']).click()
            return True
        except Exception:
            LogHelper.error("Select folder failed.")
            # Page.quit()
            return False

    @classmethod
    def search_partner(cls, partnername = None,):
        try:
            Page.locate_element(cls.xpaths['partnerSearchTxtBox']).send_keys(partnername)
            Page.locate_element(cls.xpaths['partnerSubmitSearch']).click()
            Page.delayed_click(cls.xpaths['partnerLink'], sleep_time=5)
            return True
        except Exception:
            LogHelper.error("Search partner failed.")
            # Page.quit()
            return False

    @classmethod
    def act_as_partner(cls):
        try:
            Page.delayed_click(cls.xpaths['act_as_link'], sleep_time=2)
            cls.start_use_mozy()
            return True
        except Exception:
            LogHelper.error("Act as partner failed.")
            # Page.quit()
            return False

    @classmethod
    def start_use_mozy(cls):
        try:
            Page.delayed_click(cls.xpaths['start_using_mozy_btn'], sleep_time=2)
            return True
        except Exception:
            LogHelper.error("Click Start Using Mozy Button failed.")
            # Page.quit()
            return False

    @classmethod
    def click_client_configuration(cls):
        try:
            Page.delayed_click(cls.xpaths['client_configuration_link'], sleep_time=2)
            return True
        except Exception:
            LogHelper.error("Click Client Configration link failed.")
            # Page.quit()
            return False

    @classmethod
    def find_or_create_client_configuration(cls,name,type):
        Page.switch_to_iframe(cls.xpaths['iframe_tg'])
        if Page.is_linktext_exist(name):
            Page.find_element_by_linktext(name).click()
        else:
            Page.locate_element(cls.xpaths['config_name_tb']).send_keys(name)
            Page.select_dropbox(cls.xpaths['config_license_type_id_select'], type)
            Page.delayed_click(cls.xpaths['config_next_btn'], sleep_time=2)

    @classmethod
    def uncheck_all_backup_sets(cls,backup_sets_type):
        if backup_sets_type in ("windows_backup_sets", "mac_backup_sets", "linux_backup_sets"):
            print backup_sets_type

            BusPage.switch_to_tab(backup_sets_type)
            # Page.delayed_click((cls.xpaths[backup_sets_type]), sleep_time=2)
            if backup_sets_type == "mac_backup_sets":
                checkbox_xpath = 'macset_active_checkbox'
            elif backup_sets_type == "windows_backup_sets":
                checkbox_xpath = 'set_active_checkbox'
            els = Page.locate_elements("//input[starts-with(@id,'%s')]" % checkbox_xpath)
            for el in els:
                cls.driver.execute_script("arguments[0].scrollIntoView();", el)
                if el.get_attribute("checked"):
                    el.click()
            pass
        else:
            assert "backup sets is not included in windows_backup_sets,mac_backup_sets,linux_backup_sets"

    @classmethod
    def current_tab(cls):
        pass

    @classmethod
    def switch_to_tab(cls, tabname):
        Page.delayed_click((cls.xpaths[tabname]), sleep_time=2)

    @classmethod
    def enforce_encryption(cls):
        Page.check(cls.xpaths["enforce_encryption"])
        Page.check(cls.xpaths["enforce_encryption_cascade"])

    @classmethod
    def choose_encryption(cls, encryption):
        # Select preference tab
        # Page.delayed_click((cls.xpaths["Preferences"]), sleep_time=2)
        cls.switch_to_tab("Preferences")
        cls.select_encryption_type(encryption)

    @classmethod
    def set_kmip(cls):
        kms_server = GLOBAL_CONFIG.get('KMIP').get('SERVERADDRESS')
        kms_port = GLOBAL_CONFIG.get('KMIP').get('SERVERPORT')
        kms_naeport = GLOBAL_CONFIG.get('KMIP').get('NAE-PORT')
        kms_issuer = GLOBAL_CONFIG.get('KMIP').get('ISSUER')
        kms_group = GLOBAL_CONFIG.get('KMIP').get('GROUP')

        Page.delayed_click((cls.xpaths["user_choose_kmip"]), sleep_time=2)

        # Clear existing kmip setting
        Page.clear(cls.xpaths['kmip_address'])
        Page.clear(cls.xpaths['kmip_port'])
        Page.clear(cls.xpaths['kmip_naeport'])
        Page.clear(cls.xpaths['kmip_cert_issuer'])
        Page.clear(cls.xpaths['kmip_group'])

        # Set kmip setting
        Page.locate_element(cls.xpaths['kmip_address']).send_keys(kms_server)
        Page.locate_element(cls.xpaths['kmip_port']).send_keys(kms_port)
        Page.locate_element(cls.xpaths['kmip_naeport']).send_keys(kms_naeport)
        Page.locate_element(cls.xpaths['kmip_cert_issuer']).send_keys(kms_issuer)
        Page.locate_element(cls.xpaths['kmip_group']).send_keys(kms_group)

    @classmethod
    def select_encryption_type(cls, encryption):
        # Allowed encryption types
        Page.check(cls.xpaths["user_choose_encryption"])

        # Choose encryption type
        if encryption.upper() == "KMIP":
            cls.set_kmip()

        elif encryption.upper() == "DEFAULT":
            Page.uncheck(cls.xpaths["user_choose_random"])
            Page.uncheck(cls.xpaths["user_choose_pkey"])
            Page.check(cls.xpaths["user_choose_default"])
            # Page.delayed_click((cls.xpaths["user_choose_default"]), sleep_time=2)
        elif encryption.upper() == "RANDOM":
            Page.uncheck(cls.xpaths["user_choose_default"])
            Page.uncheck(cls.xpaths["user_choose_pkey"])
            Page.check(cls.xpaths["user_choose_random"])
            # Page.delayed_click((cls.xpaths["user_choose_random"]), sleep_time=2)
            Page.delayed_click((cls.xpaths["allow_export_both"]), sleep_time=2)
        elif encryption.upper() == "PKEY":
            Page.uncheck(cls.xpaths["user_choose_default"])
            Page.uncheck(cls.xpaths["user_choose_random"])
            Page.check(cls.xpaths["user_choose_pkey"])
            # Page.delayed_click((cls.xpaths["user_choose_pkey"]), sleep_time=2)
            Page.delayed_click((cls.xpaths["allow_export_pkey"]), sleep_time=2)
        elif encryption.upper() == "CKEY":
            ckey = GLOBAL_CONFIG.get('CKEY')
            Page.delayed_click((cls.xpaths["user_choose_ckey"]), sleep_time=2)
            Page.clear(cls.xpaths['ckey_url'])
            Page.locate_element(cls.xpaths['ckey_url']).send_keys(ckey)
        else:
            assert "ERROR: Please check if you use the correct encryption type in [default, pkey, random, ckey, kmip]."

    @classmethod
    def save_client_configuration(cls):
        Page.delayed_click(cls.xpaths["save_changes_btn"], sleep_time=2)

    @classmethod
    def assign_user_group_to_configuration(cls,group_name):
        # Page.delayed_click(cls.xpaths['user_groups'],0,2)
        cls.switch_to_tab("user_groups")
        Page.delayed_click(cls.xpaths['add_user_groups'], sleep_time=2)
        if Page.locate_element("//div[@id='config-user-groups']//label[text()='%s']/input/ancestor::tr[1]" % group_name).get_attribute('class') == '':
            user_group_checkbox = "//div[@id='config-user-groups']//label[text()='%s']/input" % group_name
            Page.delayed_click(user_group_checkbox, sleep_time=2)

    @classmethod
    def select_folder(cls):
        try:
            el = Page.wait_for_element_list(cls.xpaths['folderIcon'])
            el.click()
            return True
        except Exception:
            LogHelper.error("BUS Select folder failed.")
            # Page.quit()
            return False

    @classmethod
    def go_to_freya(self):
        windows_num_before = len(self.bus_driver.window_handles)
        try:
            self.select_folder()
            # EC.number_of_windows_to_be(windows_num_before+1)
            self.bus_driver.switch_to.window(self.bus_driver.window_handles[-1])
            return True
        except Exception:
            LogHelper.error("Switch to Freyja.")
            # Page.quit()
            return False

    @classmethod
    def go_to_eDiscovery(self):
        Page.locate_element(self.xpaths['eDiscovery_link']).click()
        Page.locate_element(self.xpaths['define_new_search_btn']).click()
        self.bus_driver.switch_to.window(self.bus_driver.window_handles[-1])

    @classmethod
    def visit_cas(self):
        env = RUNNER_CONFIG.get('ENVIRONMENT') or 'QA12'
        if "QA" in env:
            cas_host = GLOBAL_CONFIG.get('QA_ENVIRONMENT').get(env).get('mozy.cashost')
            self.bus_driver = Page.create_browser()
            self.bus_driver.get(cas_host)

if __name__ == '__main__':
    result = BusPage.visit()
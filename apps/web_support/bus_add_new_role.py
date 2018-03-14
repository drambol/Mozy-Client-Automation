from selenium.webdriver.support import expected_conditions  as EC

from apps.web_support.base_page import Page
from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.runner_config_loader import RUNNER_CONFIG
from selenium.webdriver.support.ui import Select
from lib.partnerhelper import PartnerHelper
import ast

class BusAddNewRolePage(Page):

    bus_driver = None

    xpaths = {
                'addNewRoleLnk': "//a[text()='Add New Role']",
                'listRoleLnk': "//a[text()='List Roles']",
                'roleTypeDropBox':"//select[@id='role_subpartner_role']",
                'roleNameTxtBox':"//input[@id='role_name']",
                'roleParent':"//select[@id='role_parent_role_id']",
                'saveChangesBtn':"//input[@value='Save Changes']",

                'all_roleUncheckbox':"//input[starts-with(@id,'capability_') and @type='checkbox' ]",
                'saveChanges4SpecificRole':"//div[starts-with(@id,'roles-show-') and @class='adminbox-content']//input[@name='commit']",

                'Suspend users, user groups, or partners': "102",
                'View user, user group, or partner status':"104",
                'Roles: add/edit/delete':"2",
                'Roles: view/assign':"3",
                'Admins: add/edit/delete':"4",
                'Admins: list/view':"5",
                'Edit Sync':"133",
                'Log in as admin':"6",

              }

    @classmethod
    def __init__(cls,bus_driver):
        cls.bus_driver = bus_driver

    @classmethod
    def create_role(cls,name="default",include_list=[],exclude_list=[],sub_role=True,include_all=False,exclude_all=True):
        el = Page.locate_element(cls.xpaths['addNewRoleLnk'])
        cls.driver.execute_script("arguments[0].scrollIntoView();", el)
        el.click()
        if sub_role:
            Page.select_dropbox(cls.xpaths['roleTypeDropBox'],"Partner admin")
        Page.locate_element(cls.xpaths['roleNameTxtBox']).send_keys(name)
        Page.locate_element(cls.xpaths['saveChangesBtn']).click()

        if include_all:
            els = Page.locate_elements(cls.xpaths['all_roleUncheckbox'])
            for el in els:
                cls.driver.execute_script("arguments[0].scrollIntoView();", el)
                el.click()

        Page.locate_element(cls.xpaths['saveChanges4SpecificRole']).click()

    @classmethod
    def get_role_id(cls,name):
        Page.locate_element(cls.xpaths['listRoleLnk']).click()
        el = Page.locate_element("//a[starts-with(@href,'/roles/show/') and text()='%s']" % name)
        role_link = el.get_attribute("href")
        print("role_link:%s" % role_link)
        last_index = role_link.rfind('/')
        root_role_id = ast.literal_eval(role_link[(last_index-len(role_link)+1):])
        print("root_role_id:%s" % root_role_id)
        return root_role_id

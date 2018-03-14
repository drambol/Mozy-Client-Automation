from selenium.webdriver.support import expected_conditions  as EC

from apps.web_support.base_page import Page
from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.runner_config_loader import RUNNER_CONFIG
from selenium.webdriver.support.ui import Select

class BusAddNewProPlanPage(Page):

    bus_driver = None

    xpaths = {
                'addNewProPlanLnk': "//a[text()='Add New Pro Plan']",
                'planName': "//input[@id='plan_name']",
                'biennial_periods': "//input[@id='period_2']",
                'yearly_periods':"//input[@id='period_Y']",
                'monthly_periods':"//input[@id='period_M']",
                'server_license_price': "//input[@id='price8_license_price']",
                'server_min_licenses': "//input[@id='price8_minimum_licenses']",
                'server_quota_price': "//input[@id='price8_quota_price']",
                'server_min_quota': "//input[@id='price8_minimum_quota']",
                'desktop_license_price': "//input[@id='price7_license_price']",
                'desktop_min_licenses': "//input[@id='price7_minimum_licenses']",
                'desktop_quota_price': "//input[@id='price7_quota_price']",
                'desktop_min_quota': "//input[@id='price7_minimum_quota']",
                'server_tab': "//div[@id='plan-pro_new-tabs']/ul/li[text()='Server']']",
                'desktop_tab': "//div[@id='plan-pro_new-tabs']/ul[1]/li[text()='Desktop']",
                'saveProPlan': "//input[@name='commit']"
              }

    @classmethod
    def __init__(cls,bus_driver):
        cls.bus_driver = bus_driver

    @classmethod
    def create_proplan(cls,name="default",periods="monthly",server_license_price="1",server_min_licenses="1",server_quota_price="1",server_min_quota="1",desktop_license_price="1",desktop_min_licenses="1",desktop_quota_price="1",desktop_min_quota="1"):
        el = Page.locate_element(cls.xpaths['addNewProPlanLnk'])
        cls.driver.execute_script("arguments[0].scrollIntoView();", el)
        el.click()
        Page.locate_element(cls.xpaths['planName']).send_keys(name)

        if periods in ("monthly", "yearly", "biennial"):
            Page.locate_element(cls.xpaths['%s_periods' % (periods)]).click()
        else:
            Page.locate_element("monthly_periods").click()
        Page.locate_element(cls.xpaths['server_license_price']).send_keys(server_license_price)
        Page.locate_element(cls.xpaths['server_min_licenses']).send_keys(server_license_price)
        Page.locate_element(cls.xpaths['server_quota_price']).send_keys(server_license_price)
        Page.locate_element(cls.xpaths['server_min_quota']).send_keys(server_license_price)

        Page.locate_element(cls.xpaths['desktop_tab']).click()
        Page.locate_element(cls.xpaths['desktop_license_price']).send_keys(desktop_license_price)
        Page.locate_element(cls.xpaths['desktop_min_licenses']).send_keys(desktop_min_licenses)
        Page.locate_element(cls.xpaths['desktop_quota_price']).send_keys(desktop_quota_price)
        Page.locate_element(cls.xpaths['desktop_min_quota']).send_keys(desktop_min_quota)

        Page.locate_element(cls.xpaths['saveProPlan']).click()


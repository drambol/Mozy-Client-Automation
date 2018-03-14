from selenium.webdriver.support import expected_conditions  as EC

from apps.web_support.base_page import Page
from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.runner_config_loader import RUNNER_CONFIG
from selenium.webdriver.support.ui import Select

class BusReportBuilderPage(Page):

    bus_driver = None

    xpaths = {
                'reportBuilderLnk': "//a[text()='Report Builder']",
                'reportName': "//input[@id='job_title' and @type='text']",
                'saveReport': "//input[@name='commit']"
              }

    @classmethod
    def __init__(cls,bus_driver):
        cls.bus_driver = bus_driver

    @classmethod
    def create_report(cls,type):
        if type in ('Billing Summary', 'Billing Detail', 'Machine WatchList', 'Machine Status', 'Machine Status', 'Resources Added', 'Machine Over Quota' ):
            Page.delayed_click(cls.xpaths['reportBuilderLnk'])
            Page.delayed_click("//a[text()='%s']" % type)
        else:
            print "type should be one of 'Billing Summary', 'Billing Detail', 'Machine WatchList', 'Machine Status', 'Machine Status', 'Resources Added', 'Machine Over Quota' "

    @classmethod
    def save_report(cls,report_name):
        el = Page.locate_element(cls.xpaths['reportName'])
        el.send_keys(report_name)
        Page.delayed_click(cls.xpaths['saveReport'])


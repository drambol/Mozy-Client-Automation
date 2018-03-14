import subprocess
import time

from apps.web_support.base_page import Page
from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.runner_config_loader import RUNNER_CONFIG


class MachinePage(Page):

    xpaths = {
            'encryptiontype': "//dt[text()='Encryption:']/following-sibling::*[1]"
              }

    def __init__(self):
        pass

    @classmethod
    def visit(self, machineid):
        self.machinepage_driver = Page.current_driver()
        env = RUNNER_CONFIG.get('ENVIRONMENT') or 'QA12'
        bushost = GLOBAL_CONFIG.get('QA_ENVIRONMENT').get(env).get('mozy.bushost') or 'www.mozypro.com'
        if not bushost.startswith('https://'):
            machinepage_url = "https://{bushost}/admin/view_restores/{machineid}".format(bushost=bushost, machineid=machineid)
        else:
            machinepage_url = "{bushost}/admin/view_restores/{machineid}".format(bushost=bushost, machineid=machineid)
        # self.machinepage_driver = Page.create_browser()
        try:
            self.machinepage_driver.get(machinepage_url)
        except:
            self.machinepage_driver = Page.create_browser(force=True)
            self.machinepage_driver.get(machinepage_url)


    @classmethod
    def validate_machine_ecnryption(cls, encryptiontype="default"):
        if encryptiontype.upper() in ("PKEY", "CKEY", "RANDOM"):
            encryptiontype = "CUSTOM"

        encryption_web = Page.locate_element(cls.xpaths['encryptiontype'])

        return (encryption_web.text.upper() == encryptiontype.upper())


if __name__ == '__main__':

    from bus_page import BusPage
    BusPage.visit()
    BusPage.login()
    MachinePage.visit(77154115)
    print MachinePage.validate_machine_ecnryption("kmip")
    print MachinePage.validate_machine_ecnryption("ckey")



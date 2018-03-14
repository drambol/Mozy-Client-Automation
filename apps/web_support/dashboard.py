import subprocess
import time

from apps.web_support.base_page import Page
from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.runner_config_loader import RUNNER_CONFIG


class DashboardPage(Page):


    @classmethod
    def visit(self):
        self.dashboardpage_driver = Page.current_driver()
        env = RUNNER_CONFIG.get('ENVIRONMENT') or 'QA12'
        bushost = GLOBAL_CONFIG.get('QA_ENVIRONMENT').get(env).get('mozy.bushost') or 'www.mozypro.com'
        dashboardpage_url = "{bushost}/dashboard".format(bushost=bushost)
        if not bushost.startswith('https://'):
            dashboardpage_url = "https://{page}".format(page=dashboardpage_url)

        try:
            self.dashboardpage_driver.get(dashboardpage_url)
        except:
            self.dashboardpage_driver = Page.create_browser(force=True)
            self.dashboardpage_driver.get(dashboardpage_url)



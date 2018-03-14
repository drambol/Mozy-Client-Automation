import subprocess
import time

from selenium.webdriver.support.ui import Select
from apps.web_support.base_page import Page
from configuration.windows.windows_config_loader import WIN_CONFIG


class FedidSignInPage(Page):

    xpaths = {'signtothissite': "//input[@id='ctl00_ContentPlaceHolder1_ThisRpRadioButton']",
              'signtoothersite': "//input[@id='ctl00_ContentPlaceHolder1_OtherRpRadioButton']",
              'selectsite': "//select[@id='ctl00_ContentPlaceHolder1_RelyingPartyDropDownList']",
              'continuetosign': "//input[@id='ctl00_ContentPlaceHolder1_SignInButton']",

              'fedidusername': "//input[@id='ctl00_ContentPlaceHolder1_UsernameTextBox']",
              'fedidpwd': "//input[@id='ctl00_ContentPlaceHolder1_PasswordTextBox']",
              'signinbutton': "//input[@id='ctl00_ContentPlaceHolder1_SubmitButton']"
              }

    def __init__(self):
        pass

    @classmethod
    def visit(cls):
        # TODO: Remove hard when config ready
        # https://win-ko2af9k2doa.mtdev.mozypro.local/adfs/ls/?SAMLRequest=7b0HYBxJliUmL23Ke39K9UrX4HShCIBgEyTYkEAQ7MGIzeaS7B1pRyMpqyqBymVWZV1mFkDM7Z28995777333nvvvfe6O51OJ%2fff%2fz9cZmQBbPbOStrJniGAqsgfP358Hz8iHjfZolw9Ol638%2bWr%2fBet86ZNz55%2b9tHv%2f%2bk0m9w%2ff3iwfX%2fv%2fqfb%2b7uTe9sH%2bw92ts%2f3Pp083Ls%2fme4fHHyU%2fmReN0W1%2fOyjvfHOR%2blZ06zzs2XTZsuWPtrZfbC98%2bn27t6bnb1He7v0v%2fHDnf2f%2bih9Sr0Uy6zlN%2bdtu2oe3b17VSy331Z72fnDt3uzKhsv2ll%2bOV5UP7he1dW4rKZZeTebnTd3y%2bbuR%2blJtWxy9LKul4%2bqrCmaR8tskTeP2umj18dfPH9ECD2aSqNH62WzyqfFeZHPPkrfLcpl84iHvflt6ratplX50dFjHlgtr25%2bKWuavMbAPjrCwGhc3z17sf17fbl3%2fOzh77X39Mvj4XHRi5fFNG%2futvW6aR%2fflU6PHtNQZwVANu%2bJwOPj9azIl9P8FdG7Lqb41H14ZAif0dzvMULjabW4%2b4uy3b1ltazyxWpdlndBqMd37Uvu1wDoXYck%2fdHnqaP%2fBw%3d%3d&Signature=PE5xudj2pJEbvkfVY%2bBDCwOVIyLW0USobV%2bgONyZgAbTuJgrZ1ab62bFUksGexqIgP8SnecXjXcgSWCghDuXqdZxdxwmnW1TBnGwNPrEWuPvm0VTCYpsENUT3XxplC45Rrt8SGczowwKTBG1EFF8G9bdfd5cDF5ulNiJzxUDve58UBLzEOFo4NXsvChIcaWUgBZOhf07ietvEBagnZzPNOd2B0i8juxdF%2fXYqlrekIzED4tno0FvHUiMnhYMOsG4NH1K3dKhclordj4Bq787YQzrwZegf3WOllaq%2fPB6%2fapEoakI3b1mk54MMK2EWDrR1i0dJbiV%2bLl1YRX204T7Tg%3d%3d&SigAlg=http%3a%2f%2fwww.w3.org%2f2001%2f04%2fxmldsig-more%23rsa-sha256
        #fedidpage_url = "https://win-ko2af9k2doa.mtdev.mozypro.local/adfs/ls/IdpInitiatedSignOn.aspx"
        fedidpage_url = "https://10.29.103.120/adfs/ls/IdpInitiatedSignOn.aspx"
        cls.driver = Page.create_browser()
        cls.driver.get(fedidpage_url)

    @classmethod
    def select_rely_site(cls, site="Trust.qa12nonoempull"):
        selectothersite = cls.locate_element(cls.xpaths['signtoothersite'])
        selectothersite.click()

        cls.select_dropbox(cls.xpaths['selectsite'], site)

        return True


    @classmethod
    def get_sites_list(cls):
        els = cls.locate_element(cls.xpaths['signtoothersite'])
        site_list = []
        for el in els:
            site_list.append(el.text)
        return site_list


    @classmethod
    def continue_signin(cls):
        Page.delayed_click(cls.xpaths['continuetosign'], 0, 2)

    @classmethod
    def login(cls, username, password):
        Page.locate_element(cls.xpaths['fedidusername']).send_keys(username)
        Page.locate_element(cls.xpaths['fedidpwd']).send_keys(password)
        Page.delayed_click(cls.xpaths['signinbutton'], 0, 3)

    @staticmethod
    def close_browser():
        subprocess.Popen('cmd /c taskkill /F /IM firefox.exe /T')


    @classmethod
    def pass_to_client(cls):
        handles = cls.driver.window_handles
        print handles[0]
        for handle in handles:
            print handle


if __name__ == '__main__':
# # driver = FedidSignInPage.create_browser()
# from selenium import webdriver
# from selenium.webdriver.firefox.remote_connection import FirefoxRemoteConnection
# # driver = webdriver.Firefox
# # webdriver.firefox.webdriver.RemoteWebDriver
# # driver = FirefoxRemoteConnection("http://localhost:7055/hub")
#
# # driver = webdriver.firefox.webdriver.RemoteWebDriver("http://localhost:7055/hub",
# #     desired_capabilities=webdriver.DesiredCapabilities.FIREFOX
# # )
# driver = webdriver.Firefox
# # print driver.command_executor
# # url = driver.command_executor._url  # "http://127.0.0.1:60622/hub"
# # print url
# session_id = driver.session_id
# print session_id
#
# driver = webdriver.Remote(command_executor=url, desired_capabilities={})
# driver.session_id = session_id
#
# print driver
# print driver.title

    FedidSignInPage.visit()
    import time
    time.sleep(8)
    FedidSignInPage.select_rely_site()
    FedidSignInPage.continue_signin()

    FedidSignInPage.login("qa12nonoempush2@mtdev.mozypro.local", "abc!@#123")

    from apps.windows.windows_client import Windows_Client
    windowsclient = Windows_Client("mozypro")
    result = windowsclient.gui.login_dialog.fedid_activate("pkey", "test1234", is_exist="NEW")

    # Allow open Mozy from browser
    # FedidSignInPage.pass_to_client()




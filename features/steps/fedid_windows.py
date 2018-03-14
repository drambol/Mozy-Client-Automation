from behave import *

import time

from apps.windows.windows_client import Windows_Client
from apps.web_support.fedid_win_page import FedidSignInPage

@When('I activate fedid account')
def step_impl(context):
    windowsclient = Windows_Client(context.oem)
    windowsclient.gui.login_dialog.open_fedidpage(context.subdomain)

    FedidSignInPage.visit()
    time.sleep(8)

    FedidSignInPage.select_rely_site()
    FedidSignInPage.continue_signin()

    FedidSignInPage.login(context.fedidusername, context.fedidpwd)


@When('I open fedid {title} window')
def step_impl(context, title):
    windowsclient = Windows_Client(context.oem)
    windowsclient.gui.login_dialog.open_fedidpage(context.subdomain)

    if title == "Sign-In Page":
        FedidSignInPage.visit()
        time.sleep(8)

        FedidSignInPage.select_rely_site()
        FedidSignInPage.continue_signin()

    elif title == "OneLogin":
        print("4. Windows FedId OneLogin")
        pass


@When('Then I activate from fedid SignIn window')
def step_impl(context):
    print(context.fedidusername)
    print(context.fedidpwd)
    FedidSignInPage.login(context.fedidusername, context.fedidpwd)




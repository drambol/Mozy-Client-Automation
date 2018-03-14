
import os

from behave import *

from configuration.runner_config_loader import RUNNER_CONFIG

from apps.windows.windows_client import Windows_Client



@When('I {activate_type} activate windows {client} with')
def step_impl(context, activate_type, client):
    oem_client = RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")
    env = RUNNER_CONFIG.get('ENVIRONMENT', "QA12")
    email = ""
    password = ""
    productkey = ""
    encryption_key = ""
    env = "QA12"
    for row in context.table:
        if oem_client.upper() == row.get('oem').upper() and env.upper() == row.get('env').upper():
            email = row.get('email')
            password = row.get('password')
            productkey = row.get('password')
            encryption_type = row.get('encryption_type')
            encryption_key = row.get('encryption_key')
    # if os.environ['activate'] and os.environ['activate'] == str(True):
    windowsclient = Windows_Client(oem_client)

    if windowsclient.gui.status_window.client_is_activated():
        pass
    else:
        if client.upper() == "GUI":
            # result = windowsclient.gui.status_window.continuesetupbutton.Click()
            # result = windowsclient.gui.login_dialog.activate(email, password)
            if activate_type.upper() == "KEYLESS":
                result = windowsclient.gui.login_dialog.keyless_activate(email, password, encryption_type, encryption_key)
            elif activate_type.upper() == "KEY":
                result = windowsclient.gui.login_dialog.key_activate(productkey, encryption_type, encryption_key)
                pass
            elif activate_type.upper() == "FEDID":
                result = windowsclient.gui.login_dialog.fedid_activate(productkey, encryption_type, encryption_key)
                pass

        else:
            result = windowsclient.cli.activate_keyless(email, password, encryption_type, encryption_key)

    (result is not None).should.be(True)

@When('Windows Client is not activated')
def step_impl(context):
    oem_client = RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")
    windowsclient = Windows_Client(oem_client)
    if windowsclient.gui.status_window.client_is_activated():
        # windowsclient._controller.clear_config()
        pass
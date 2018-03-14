
import os
import time

from behave import *

from configuration.runner_config_loader import RUNNER_CONFIG

from apps.windows.windows_client import Windows_Client
from apps.qa_environment import QA_Environment
from apps.windows.windows_cli import Windows_Cli

@When('I {activate_type} activate windows {client} with')
def step_impl(context, activate_type, client):
    result = None
    oem_client = RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")
    env = RUNNER_CONFIG.get('ENVIRONMENT', "QA12")
    email = ""
    password = ""
    productkey = ""
    encryption_key = ""
    subdomain = ""
    relytrust = ""

    for row in context.table:
        if oem_client.upper() == row.get('oem').upper() and env.upper() == row.get('env').upper():
            email = row.get('email')
            password = row.get('password')
            productkey = row.get('product_key')
            encryption_type = row.get('encryption_type')
            encryption_key = row.get('encryption_key')
            subdomain = row.get('subdomain')
            relytrust = row.get('rely_trust')
    # if os.environ['activate'] and os.environ['activate'] == str(True):
    context.oem = oem_client
    windowsclient = Windows_Client(oem_client)

    if windowsclient.gui.status_window.client_is_activated():
        pass
    else:
        if client.upper() == "GUI":
            # result = windowsclient.gui.status_window.continuesetupbutton.Click()
            # result = windowsclient.gui.login_dialog.activate(email, password)
            if activate_type.upper() == "KEYLESS":
                result = windowsclient.gui.login_dialog.keyless_activate(email, password, encryption_type, encryption_key, is_exist="existing")
            elif activate_type.upper() == "KEYED":
                result = windowsclient.gui.login_dialog.key_activate(productkey, email, password, encryption_type, encryption_key, is_exist="existing")
                pass
            elif activate_type.upper() == "FEDID":
                context.subdomain = subdomain
                # result = windowsclient.gui.login_dialog.open_fedidpage(subdomain)
                context.execute_steps(unicode("I open fedid SignIn window"))
                # result = windowsclient.gui.login_dialog.fedid_activate(subdomain, relytrust, email, password, encryption_type, encryption_key)
                pass

        else:
            result = windowsclient.cli.activate_keyless(email, password, encryption_type, encryption_key)

    (result is not None).should.be(True)

@Then('I do {type} activate with {is_exist} created user using {encryption_type} via {client}')
def step_impl(context, type, is_exist, encryption_type, client):
    result = None

    oem_client = RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")
    env = RUNNER_CONFIG.get('ENVIRONMENT', "QA12")
    email = context.user.username
    password = context.user.password

    productkey = context.user.product_keys

    # TODO: Created from BUS Client Configuration
    encryption_type = encryption_type.lower() or "pkey"
    # encryption_type = context.encryption.type or "pkey"
    # encryption_key = context.encryption.key or "test1234"

    windowsclient = Windows_Client(oem_client)

    if windowsclient.gui.status_window.client_is_activated():
        pass
    else:
        if client.upper() == "GUI":
            if type.upper() == "KEYLESS":
                context.multiencryption = False
                result = windowsclient.gui.login_dialog.keyless_activate(email, password, encryptiontype=encryption_type, key="test1234", is_exist=is_exist, multiencryption=context.multiencryption)
            elif type.upper() == "KEYED":
                result = windowsclient.gui.login_dialog.key_activate(productkey, email, password, encryptiontype=encryption_type, key="test1234", is_exist=is_exist, multiencryption=context.multiencryption)
        else:
            if type.upper() == "KEYLESS":
                result = windowsclient.cli.activate_keyless(email, password, encryption_type=encryption_type, key="test1234")
            # elif type.upper() == "KEYED":
            #     result = windowsclient.cli.activate_keyless(email, password, encryption_type="pkey", key="test1234")

    (result is not None).should.be(True)

@When('Windows Client is not activated')
def step_impl(context):
    from lib.platformhelper import PlatformHelper
    if PlatformHelper.is_win():
        from apps.windows.windows_client import Windows_Client
    winclient = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro"))

    if winclient.gui.status_window.client_is_activated():
        winclient.controller.set_unconfigured_status()
        winclient.controller.reset_reg(RUNNER_CONFIG.get('ENVIRONMENT', "QA12"))
        winclient.controller.restart_services(force=True)
    # context.execute_steps(unicode("When I reset configration by windows Client"))
    # oem_client = RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")
    # windowsclient = Windows_Client(oem_client)
    # if windowsclient.gui.status_window.client_is_activated():
    #     # windowsclient._controller.clear_config()
    #     context.execute_steps(unicode("I reset configration by windows Client"))
    # else:
    #     pass


@When('I activate windows {client} in {activated_type} environment')
def step_impl(context, client, activated_type):
    oem_client = RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")
    env = RUNNER_CONFIG.get('ENVIRONMENT', "QA12")
    windowsenv = QA_Environment(oem_client)
    windowsenv.get_host(env)
    if activated_type == "fedid":
        windowsenv.set_env.set_fedid_env(env)
    elif activated_type == "autoactivate":
        windowsenv.get_autoactivate_env(env)
    elif activated_type == "assistactivate":
        windowsenv.get_assistedactivate_env(env)

@When('I recover {client} setting of {activated_type}')
def step_impl(context, client, activated_type):
    oem_client = RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")
    env = RUNNER_CONFIG.get('ENVIRONMENT', "QA12")
    windowsenv = QA_Environment(oem_client)
    windowsenv.recover_to_qa(activated_type, env)

@When('I {activate_type} activate client with user {username}')
def step_impl(context, activate_type, username):
    oem_client = RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")
    win_cli = Windows_Cli(oem_client)
    if activate_type == "auto":
        now = int(time.time())
        timeArray = time.localtime(now)
        otherStyleTime = time.strftime("%m%d%H%M", timeArray)
        username = username + "+" + otherStyleTime + "@mozy.com"
        win_cli.activate_auto(username)

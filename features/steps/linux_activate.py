import re
import os

from behave import *

from apps.linux.linux_app.linux_gui_client import LinuxGUIClient
from configuration.runner_config_loader import RUNNER_CONFIG
from configuration.linux.lynx_config_loader import LYNX_CONFIG
from lib.userhelper import UserHelper
from lib.loghelper import LogHelper
from lib.filehelper import FileHelper



@When('Linux Client is activated with "{credential}"')
def step_impl(context, credential):
    context.execute_steps(u"""When I wait for sock ready""")
    # logic to parse credential
    cre_with_oc = re.sub(r"{oemclient}", RUNNER_CONFIG.get('OEM_CLIENT'), credential)
    cre_with_oc_env = re.sub(r"{env}", RUNNER_CONFIG.get('ENVIRONMENT'), cre_with_oc)
    expected_credential = LYNX_CONFIG.get('CREDENTIAL').get(cre_with_oc_env)
    username = expected_credential.get('USERNAME')
    LogHelper.debug("username: %s"%username)
    password = expected_credential.get('PASSWORD')
    pk = expected_credential.get('PERSONALKEY') or None
    context.user = UserHelper(username=username)
    to_activate = False
    if not LinuxGUIClient.account_cmd.is_activate():
        to_activate = True
    else:
        current_email = LinuxGUIClient.account_cmd.get_email()
        LogHelper.debug('%s is not the as  %s' % (current_email, username))
        if not current_email.upper() == username.upper():
            to_activate = True

    if to_activate:
        LogHelper.info("change user account")
        LinuxGUIClient.unlink_cmd.unlink()
        context.execute_steps(unicode('When I cleanup local state|metric database'))
        context.execute_steps(unicode('When I restart Linux Client'))
        if pk:
            result = LinuxGUIClient.activate_cmd.activate(email=username, password=password,
                                                customkeytext=pk, force_encryption_change=None)
        else:
            result = LinuxGUIClient.activate_cmd.activate(email=username, password=password, force_encryption_change=None)

        LogHelper.debug(result)


@When('Linux Client is activated with new user')
def step_impl(context):
    context.execute_steps(u"""When I wait for sock ready""")
    LinuxGUIClient.unlink_cmd.unlink()
    username = context.user.username
    password = context.user.password
    LinuxGUIClient.activate_cmd.activate(email=username, password=password)


@When('I active client with "{credential}"')
def step_impl(context, credential):
    """
    Activate with {credential}
    """

    context.execute_steps(u"""When I wait for sock ready""")
    current_credential = LYNX_CONFIG['CREDENTIAL'].get(credential)


    email = current_credential.get('USERNAME')
    password = current_credential.get('PASSWORD')
    customkeytext = current_credential.get('CUSTOMKEYTEXT')
    if customkeytext:
        LinuxGUIClient.activate_cmd.activate(email=email,
                                         password=password,
                                         customkeytext=customkeytext,
                                         force_encryption_change=None)
    else:
        LinuxGUIClient.activate_cmd.activate(email=email, password=password, force_encryption_change=None)


@When('Linux Client is activated with correct credential')
def step_impl(context):
    """
    ensure that Linux Client is activate with {env}_codename pattern
    """
    from configuration.runner_config_loader import RUNNER_CONFIG
    env = RUNNER_CONFIG.get('ENVIRONMENT')
    codename = RUNNER_CONFIG.get('OEM_CLIENT')
    credential_key = "%s_%s" % (env, codename)
    step_str ='When Linux Client is activated with "%s"' % credential_key

    context.execute_steps(unicode(step_str))


@When("I activate Linux Client with credential as below")
def activate_linux_client(context):
    for row in context.table.rows:
        email_raw = row.get('email') or row.get('username')
        password = row.get('password')
        customkeytext = row.get('customkeytext')
        password_file = row.get('password_file')
        #TODO: add other parameters


    regex = re.match(r"{env}_{oemclient}_?.*", email_raw)
    if regex:
        cre_with_oc = re.sub(r"{oemclient}", RUNNER_CONFIG.get('OEM_CLIENT'), email_raw)
        cre_with_oc_env = re.sub(r"{env}", RUNNER_CONFIG.get('ENVIRONMENT'), cre_with_oc)
        expected_credential = LYNX_CONFIG.get('CREDENTIAL').get(cre_with_oc_env)

        email = expected_credential.get('USERNAME')
        password_correct = expected_credential.get('PASSWORD')
    else:
        email = email_raw

    kargs = {
        }

    if email:
        kargs['email'] = email

    if password:
        kargs['password'] = password

    if password_file and password_file.upper() == "VALID":

        password_file_path = os.path.join(LYNX_CONFIG.get('TMP_PATH'), "password.txt")
        FileHelper.delete_file(password_file_path)

        if FileHelper.file_exist(password_file_path):
            FileHelper.delete_file(password_file_path)

        with open(password_file_path, "w") as text_file:
            text_file.write(password_correct)
        kargs['password-file'] = password_file_path

    if password_file and password_file.upper() == "INVALID":

        password_file_path = os.path.join(LYNX_CONFIG.get('TMP_PATH'), "wrong_password.txt")

        if FileHelper.file_exist(password_file_path):
            FileHelper.delete_file(password_file_path)

        with open(password_file_path, "w") as text_file:
            text_file.write("{password}_wrong".format(password=password_correct))

        kargs['password-file'] = password_file_path

    if customkeytext:
        kargs['customkeytext'] = customkeytext

    kargs['force_encryption_change'] = None


    output = LinuxGUIClient.activate_cmd.activate(**kargs)
    LogHelper.info("activate output is %s" % output)






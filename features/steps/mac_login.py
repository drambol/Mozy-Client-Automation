from sure import should
import re
import time
from behave import *
from apps.mac.mac_controller.mac_controller import MacController
from apps.mac.mac_gui_client.mac_gui_client import MacGUIClient
from apps.mac.mac_gui_installer.mac_gui_installer import AppUIElement
from apps.mac.mac_lib.mac_ui_util import MacUIUtils

from configuration.mac.mac_config_loader import MAC_CONFIG
from configuration.runner_config_loader import RUNNER_CONFIG
from lib.userhelper import UserHelper


@When('Mac Client is not activated')
def step_impl(context):
    #MacController().clean_db()
    MacController().clean_all()
    env = RUNNER_CONFIG.get('ENVIRONMENT') or "QA12"
    MacController.setup_qa_env(env)


@When('I launch Mac Client from GUI')
def step_impl(context):
    current_window = MacGUIClient().start_app()
    context.current_window = current_window


@When('I restart Mac Client from GUI')
def step_impl(context):
    current_window = MacGUIClient().restart_app()
    context.current_window = current_window


@Then('I shall see "{type}" with "{property_type}" "{expected_value}"')
def stem_impl(context, type, property_type, expected_value):
    AXRole = MacUIUtils.normalize_role(type)
    AXProperty = MacUIUtils.normalize_property(property_type)
    kwargs = {}
    kwargs['AXRole'] = AXRole
    kwargs[AXProperty] = expected_value

    obj = MacUIUtils.wait_element(context.current_window, kwargs)
    (obj is not None).should.be(True)


@When('I activate with credential "{cre}"')
def step_impl(context, cre):
    cre_with_oc = re.sub(r"{oemclient}", RUNNER_CONFIG.get('OEM_CLIENT'), cre)
    cre_with_oc_env = re.sub(r"{env}", RUNNER_CONFIG.get('ENVIRONMENT'), cre_with_oc)
    expected_credential = MAC_CONFIG.get('CREDENTIAL').get(cre_with_oc_env)
    username = expected_credential.get('USERNAME')
    password = expected_credential.get('PASSWORD')
    pk =expected_credential.get('PERSONALKEY')

    if pk:
        MacGUIClient().login_sh.activate(username, password, keytext=pk)
    else:
        MacGUIClient().login_sh.activate(username, password)


@When('I activate with bifrost created credential')
def step_impl(context):
    username = context.user.username
    password = context.user.password
    MacGUIClient().login_sh.activate(username, password)
    pass


@When("Mac Client is activated with credential '{expected_cre}'")
def step_impl(context, expected_cre):
    MacGUIClient().start_app()
    username = MacGUIClient().summary_tab.get_current_username()
    cre_with_oc = re.sub(r"{oemclient}", RUNNER_CONFIG.get('OEM_CLIENT'), expected_cre)
    cre_with_oc_env = re.sub(r"{env}", RUNNER_CONFIG.get('ENVIRONMENT'), cre_with_oc)
    expected_credential = MAC_CONFIG.get('CREDENTIAL').get(cre_with_oc_env)
    expected_username = expected_credential.get('USERNAME')
    expected_password = expected_credential.get('PASSWORD')
    personal_key = expected_credential.get('PERSONALKEY') or None
    user = UserHelper(username=expected_username, password=expected_password, pk=personal_key)
    context.user = user
    cre_without_env= re.sub(r"{env}_?", '', cre_with_oc)
    if username != expected_username:
        step_str = "When Mac Client is not activated"
        context.execute_steps(unicode(step_str))
        step_str = 'When I launch Mac Client from GUI'
        context.execute_steps(unicode(step_str))
        step_active = 'When I activate with credential "{cre}"'.format(cre=cre_with_oc_env)
        context.execute_steps(unicode(step_active))


@When('I try to activate with credential "{cre}" but enter wrong password')
def step_impl(context, cre):
    cre_with_oc = re.sub(r"{oemclient}", RUNNER_CONFIG.get('OEM_CLIENT'), cre)
    cre_with_oc_env = re.sub(r"{env}", RUNNER_CONFIG.get('ENVIRONMENT'), cre_with_oc)
    expected_credential = MAC_CONFIG.get('CREDENTIAL').get(cre_with_oc_env)
    username = expected_credential.get('USERNAME')
    password = expected_credential.get('PASSWORD') + "suffix"
    context.username = username

    MacGUIClient().login_sh.set_credential_with(username, password)


@Then('I shall see a dialog with message "{text}" is shown')
def step_impl(context, text):
    result = True
    matcher = {'AXRole': 'AXWindow', 'AXSubrole': 'AXDialog'}
    dialog = AppUIElement.from_bundle(MacController().spbundleid, matcher, 0, 30)
    if dialog.element is None:
        result = False
    result.should.equal(True)
    context.dialog = dialog

    matcher = {'AXRole': 'AXStaticText'}
    matcher['AXValue'] = text
    message = dialog.find_child(matcher)
    message.exists().should.equal(True)


@When('I close the dialog')
def step_impl(context):
    dialog = context.dialog
    matcher = {'AXRole': 'AXButton', 'AXTitle': 'OK'}
    button = AppUIElement(dialog.element, matcher)
    button.click()
    time.sleep(1)

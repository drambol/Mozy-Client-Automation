from behave import *
import time
import random
from configuration.runner_config_loader import RUNNER_CONFIG
from apps.windows.windows_client import Windows_Client


@When('Windows {client} is installed')
def step_impl(context, client):
    win_controller = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).controller
    win_controller.is_client_installed()
    isrunning = win_controller.is_client_running()
    isrunning.should.equal(True)

@When('I install Windows Client from {resource}')
def step_impl(context, resource):
    win_installer = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).installer
    if resource == "Jenkins":
        win_installer.download_and_install(RUNNER_CONFIG.get('BUILD', "543"),RUNNER_CONFIG.get('JOB', "kalypso-release"))
    elif resource == "Mozy.com":
        win_installer.download_and_install(RUNNER_CONFIG.get('BUILD', "0"),RUNNER_CONFIG.get('JOB', "product"))

@When('I download Windows Client from {resource} and launch installer')
def step_impl(context, resource):
    win_installer = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).installer
    win_installer.set_UI(True)
    if resource == "Jenkins":
        win_installer.download_and_install(RUNNER_CONFIG.get('BUILD', "543"),RUNNER_CONFIG.get('JOB', "kalypso-release"))
    elif resource == "Mozy.com":
        win_installer.download_and_install(RUNNER_CONFIG.get('BUILD', "0"),RUNNER_CONFIG.get('JOB', "product"))
    time.sleep(5)

@When('I click {buttonname} button')
def step_impl(context, buttonname):
    win_setup = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).gui.setup_window
    if buttonname.upper() == "NEXT":
        win_setup.apply()
    elif buttonname.upper() == "CANCEL":
        win_setup.cancel()
    elif buttonname.upper() == "FINISH":
        win_setup.finish_and_exit()
    elif buttonname.upper() == "INSTALL":
        win_setup.install_start()
    elif buttonname.upper() == "ACCEPT":
        win_setup.accept()

@When('I click {buttonname} button on Cancel Dialog')
def step_impl(context,buttonname):
    time.sleep(2)
    win_cancel = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).gui.setup_window
    if buttonname.upper() == "YES":
        win_cancel.choose_yes_on_cancel()
    elif buttonname.upper() == "NO":
        win_cancel.choose_no_on_cancel()


@when("I click Install button directly")
def step_impl(context):
    win_setup = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).gui.setup_window
    if win_setup.license_agreement_checked():
        win_setup.choose_license_agreement()
    if win_setup.location_change_checked():
        win_setup.choose_location_change()
    win_setup.install_start()


@when("I {operation} View the Agreement")
def step_impl(context, operation):
    selecting = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).gui.setup_window
    if operation.upper() == "DESELECT":
        if selecting.license_agreement_checked():
            selecting.choose_license_agreement()
    else:
        if not selecting.license_agreement_checked():
            selecting.choose_license_agreement()


@when("I {operation} Change Install Location")
def step_impl(context, operation):
    selecting = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).gui.setup_window
    if operation.upper() == "DESELECT":
        if selecting.location_change_checked():
            selecting.choose_location_change()
    else:
        if not selecting.location_change_checked():
            selecting.choose_location_change()


@when("I set a location with {path}")
def step_impl(context, path):
    location = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).gui.setup_window
    location.set_location(path)
    time.sleep(2)


@when("I see an alert information")
def step_impl(context):
    alert_info = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).gui.setup_window
    alert_info.alert_info_popup()


@when("I set an new location with {num} subdirectory")
def step_impl(context,num):
    path = "C:\\"
    count = 0
    while (count < int(num)):
        subpath = random.randrange(1, 100)
        path = path + str(subpath) + "\\"
        count += 1
    location = Windows_Client(RUNNER_CONFIG.get('OEM_CLIENT', "mozypro")).gui.setup_window
    location.set_location(path)
    time.sleep(2)
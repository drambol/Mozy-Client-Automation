from behave import *
import sure
import time


from apps.mac.mac_controller.mac_controller import MacController
from apps.mac.mac_controller.mac_installer import MacInstaller
from apps.mac.mac_gui_installer.mac_gui_installer import MacGUIInstaller
from configuration.runner_config_loader import RUNNER_CONFIG


@When('Mac Client is not installed')
def step_impl(context):
    if MacController().is_installed():
        MacInstaller.uninstall_package()

    result = MacController().is_installed()
    result.should.equal(False)

    if MacController.check_process_by_name('System Preferences'):
        MacController.kill_system_preference()


@When('I launch installer')
def step_impl(context):
    result = MacInstaller.mount_image_and_launch_installer()
    result.should.equal(True)


@Then('I shall see the installer window is launched')
def step_impl(context):
    result = MacGUIInstaller.is_installer_launched()
    result.should.equal(True)


@When('I click the button "{btn_name}" in installer window {number} times')
def step_impl(context, btn_name, number):
    times = int(number)
    while times > 0:
        MacGUIInstaller.click_button(btn_name)
        times -= 1


@When('I proceed to the EULA panel')
def step_impl(context):
    MacGUIInstaller.confirm_installation()
    MacGUIInstaller.click_button("Continue")
    time.sleep(1)
    MacGUIInstaller.click_button("Continue")


@Then('I shall see "{text}" in installer window')
def step_impl(context, text):
    result = MacGUIInstaller.with_message(text)
    result.should.equal(True)


@Then('I shall see the Apple Licence Acceptance page is shown')
def step_impl(context):
    result = MacGUIInstaller.is_license_acceptance_page_shown()
    result.should.equal(True)


@When('I click the button "{btn_name}" in Apple Licence Acceptance page')
def step_impl(context, btn_name):
    MacGUIInstaller.click_button(btn_name)


@Then('I shall see the Apple Licence Acceptance page is collapsed')
def step_impl(context):
    # time.sleep(1)
    result = MacGUIInstaller.is_license_acceptance_page_shown()
    result.should.equal(False)


@Then('I shall see the installer window is closed')
def step_impl(context):
    time.sleep(1)
    result = MacGUIInstaller.is_installer_launched()
    result.should.equal(False)


@When('I install the client silently')
def step_impl(context):
    result = MacInstaller.install_from_volumes()
    result.should.equal(True)

    env = RUNNER_CONFIG.get('ENVIRONMENT')
    MacController.setup_qa_env(env)

    MacInstaller.eject_images('Mozy')


@When('I proceed with the installation')
def step_impl(context):
    MacGUIInstaller.confirm_installation()
    MacGUIInstaller.continue_installation()
    MacGUIInstaller.agree_eula()
    time.sleep(1)
    MacGUIInstaller.click_install()


@Then('I shall see the installation is finished successfully')
def step_impl(context):
    result = MacGUIInstaller.wait_for_finish(120)
    result.should.equal(True)

    MacInstaller.eject_images('Mozy')


@Then('I shall see the installer correctly installed necessary files')
def step_impl(context):
    brand = RUNNER_CONFIG.get('OEM_CLIENT')
    normalize_brand = MacController.normalize_brand_name(brand)

    result = MacInstaller.files_installed(normalize_brand)
    result.should.equal(True)


@Then('I shall see the related processes are started')
def step_impl(context):
    brand = RUNNER_CONFIG.get('OEM_CLIENT')
    normalize_brand = MacController.normalize_brand_name(brand)

    result = MacController.check_process_by_name(normalize_brand + 'Backup')
    result.should.equal(True)

    result = MacController.check_process_by_name(normalize_brand + ' Status')
    result.should.equal(True)


@Then('I shall see the setup assistant is launched')
def step_impl(context):
    result = MacGUIInstaller.is_setup_assistant_launched(120)
    result.should.equal(True)

    env = RUNNER_CONFIG.get('ENVIRONMENT')
    MacController.setup_qa_env(env)
    MacController.kill_system_preference()

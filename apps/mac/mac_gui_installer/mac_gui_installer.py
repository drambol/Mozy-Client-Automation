import time

# from apps.mac.mac_controller.mac_installer import MacInstaller
from apps.mac.mac_controller.mac_controller import MacController
from configuration.runner_config_loader import RUNNER_CONFIG
from configuration.mac.mac_config_loader import MAC_CONFIG

from lib.loghelper import LogHelper
from lib.platformhelper import PlatformHelper

if PlatformHelper.is_mac():
    import atomac


class AppUIElement(object):
    # parent_element = None
    # element = None

    def __init__(self, parent_element, matcher, index=0, wait_time=1):
        self._element = None
        kwargs = {}
        for (attr, value) in matcher.items():
            kwargs[attr] = value

        wait_t = wait_time
        if parent_element:
            while self._element is None and wait_t > 0:
                time.sleep(1)
                if index == 0:
                    self._element = parent_element.findFirstR(**kwargs)
                else:
                    self._element = parent_element.findAllR(**kwargs)[index]
                wait_t -= 1

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, value):
        self._element = value

    @classmethod
    def from_bundle(cls, bundle, matcher, index=0, wait_time=1):
        app = None
        wait_t = 10
        while app is None and wait_t > 0:
            time.sleep(1)
            app = atomac.getAppRefByBundleId(bundle)
            wait_t -= 1

        if app:
            app.activate()
            return cls(app, matcher, index, wait_time)

    @classmethod
    def from_localized_name(cls, name, matcher, index=0, wait_time=1):
        app = None
        wait_t = 10
        while app is None and wait_t > 0:
            time.sleep(1)
            app = atomac.getAppRefByLocalizedName(name)
            wait_t -= 1

        if app:
            app.activate()
            return cls(app, matcher, index, wait_time)

    def exists(self):
        return self.element is not None

    def find_child(self, matcher, index=0, wait_time=1):
        return AppUIElement(self.element, matcher, index, wait_time)

    def get_native_parent(self):
        return self.element.AXParent

    def get_native_ancestor(self, level=1):
        ele = self.element
        while ele and level > 0:
            ele = ele.AXParent
            level -= 1
        return ele

    def click(self):
        self.element.Press()

    def send_keys(self, text):
        keyboard = atomac.AXKeyboard.loadKeyboard()
        upper_symbols_map = {
            '~': '0',
            '!': '1',
            '@': '2',
            '#': '3',
            '$': '4',
            '%': '5',
            '^': '6',
            '*': '7',
            '(': '8',
            ')': '9',
            '_': '-',  # dash
            '+': '=',
            ':': ';',
            '\'': "\"",
            '{': "[",
            '}': "]",
            '<': ",",
            '>': ".",
            '?': "/",
        }
        upper_symbols = keyboard.get('upperSymbols')
        for ch in text:
            if ch in upper_symbols:
                self.element.sendKeyWithModifiers(upper_symbols_map.get(ch), [atomac.AXKeyCodeConstants.SHIFT])
            else:
                self.element.sendKey(ch)

    def left_click(self):
        pos = self.element.AXPosition
        size = self.element.AXSize
        click_pos = ((pos[0] + size[0] / 2), (pos[1] + size[1] / 2))
        self.element.clickMouseButtonLeft(click_pos)

    def right_click(self):
        pos = self.element.AXPosition
        size = self.element.AXSize
        click_pos = ((pos[0] + size[0] / 2), (pos[1] + size[1] / 2))
        self.element.clickMouseButtonRight(click_pos)

    def has_child(self):
        return self.element.AXChildren is not None

    def get_text(self):
        return unicode(self.element.AXValue)

    def get_attributes(self):
        return self.element.getAttributes()

    def get_title(self):
        return unicode(self.element.AXTitle)


class MacGUIInstaller(object):
    # def __init__(self):
    #    pass

    @staticmethod
    def click_button(btn_name):
        matcher = {'AXRole': 'AXButton'}
        matcher['AXTitle'] = btn_name
        btn = AppUIElement.from_bundle('com.apple.installer', matcher)
        btn.click()

    @staticmethod
    def with_message(message):
        win = AppUIElement.from_bundle('com.apple.installer', {'AXRole': 'AXWindow'})
        text_element = AppUIElement(win.element, {'AXRole': 'AXStaticText'}, 7, 2)
        found_text = text_element.get_text()
        # print found_text
        result = True
        if found_text != message:
            result = False

        return result

    @staticmethod
    def is_license_acceptance_page_shown():
        result = False
        matcher = {'AXRole': 'AXButton', 'AXTitle': 'Read License'}
        btn = AppUIElement.from_bundle('com.apple.installer', matcher)
        if btn.element is not None:
            result = True
        return result

    @staticmethod
    def is_installer_launched():
        # print MacController.check_process_by_name("Installer")
        result = False
        if not MacController.check_process_by_name("Installer"):
            return result

        str_oem = RUNNER_CONFIG.get('OEM_CLIENT').lower()
        installer_win = AppUIElement.from_bundle('com.apple.installer', {'AXRole': 'AXWindow'}, 0, 10)

        if installer_win is not None:
            str_title = installer_win.get_title().lower()
            if str_title.find(str_oem) != -1:
                result = True

        return result

    @staticmethod
    def confirm_installation():
        sheet_confirm = AppUIElement.from_bundle('com.apple.installer', {'AXRole': 'AXSheet'})
        # btn_cnt = sheet_confirm.find_child({'AXRole': 'AXButton', 'AXTitle': 'Continue'})
        btn_cnt = AppUIElement(sheet_confirm.element, {'AXRole': 'AXButton', 'AXTitle': 'Continue'})
        btn_cnt.click()

    @staticmethod
    def continue_installation():
        btn_cnt = AppUIElement.from_bundle('com.apple.installer', {'AXRole': 'AXButton', 'AXTitle': 'Continue'})
        btn_cnt.click()
        time.sleep(1)
        btn_cnt.click()
        time.sleep(1)
        btn_cnt.click()

    @staticmethod
    def agree_eula():
        btn_agree = AppUIElement.from_bundle('com.apple.installer', {'AXRole': 'AXButton', 'AXTitle': 'Agree'}, 0, 5)
        btn_agree.click()

    @staticmethod
    def click_install():
        btn_install = AppUIElement.from_bundle('com.apple.installer', {'AXRole': 'AXButton', 'AXTitle': 'Install'})
        btn_install.left_click()

        textbox_psd = AppUIElement.from_bundle('com.apple.SecurityAgent', {'AXRole': 'AXTextField', 'AXSubrole': 'AXSecureTextField'}, 0, 5)
        password = MAC_CONFIG.get("LOCAL_ADMIN_PASSWORD")
        textbox_psd.send_keys(password)
        time.sleep(1)
        btn_install_sw = AppUIElement.from_bundle('com.apple.SecurityAgent', {'AXRole': 'AXButton', 'AXTitle': 'Install Software'})
        btn_install_sw.left_click()

    @staticmethod
    def wait_for_finish(wait_time=60):
        btn_close = AppUIElement.from_bundle('com.apple.installer', {'AXRole': 'AXButton', 'AXTitle': 'Close'}, 0, wait_time)
        if btn_close is None:
            raise StandardError('The installation is not finished in {time} seconds'.format(time=wait_time))

        win = AppUIElement.from_bundle('com.apple.installer', {'AXRole': 'AXWindow'}, 0, 2)
        text_message = AppUIElement(win.element, {'AXRole': 'AXStaticText'}, 10, 2)
        txt_value = text_message.get_text()
        # print txt_value
        if txt_value != 'The installation was completed successfully.':
            raise StandardError('The installation was finished but with some errors')

        LogHelper.info('The installation was completed successfully')
        btn_close.click()
        return True

    @staticmethod
    def is_setup_assistant_launched(wait_time=60):
        result = False
        spbundleid = MacController().spbundleid
        app = None
        wait_t = wait_time
        while app is None and wait_t > 0:
            time.sleep(1)
            app = atomac.getAppRefByBundleId(spbundleid)
            wait_t -= 1

        window = None
        if app is not None:
            window = AppUIElement(app, {'AXRole': 'AXWindow'}, 0, wait_time)

        if window is not None:
            brand = RUNNER_CONFIG.get('OEM_CLIENT')
            window_name = MacController.normalize_brand_name(brand)
            title = window.get_title()
            if title == window_name:
                result = True

        return result


if __name__ == "__main__":
    print "Hello!"
    # MacInstaller.eject_images('Mozy')
    # MacInstaller.mount_image_and_launch_installer()
    # time.sleep(2)
    # MacGUIInstaller.is_installer_launched()
    # MacGUIInstaller.confirm_installation()
    # MacGUIInstaller.continue_installation()
    # MacGUIInstaller.agree_eula()
    # MacGUIInstaller.click_install()
    # MacGUIInstaller.wait_for_finish(120)
    import os
    folder = "Documents"
    path = os.path.expanduser("~/{folder}".format(folder=folder))
    print path

    backup_set_name = "Documents Folder"
    matcher = {'AXRole': 'AXTextField'}
    matcher['AXValue'] = backup_set_name + "*"
    print matcher

    import re
    text = "Sending Files: 1 left (1.08 GB)"
    match = re.findall(r' \((.*) ', text)
    print match[0]
    num = float(match[0])
    print num
    print num.__class__
    file_size = 52428800
    size = file_size / (1024.0 * 1024.0)
    print size
    print "OK!"

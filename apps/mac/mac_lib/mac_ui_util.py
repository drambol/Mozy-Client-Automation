import time
import re

from lib.platformhelper import PlatformHelper
if PlatformHelper.is_mac():
    from atomac._a11y import ErrorCannotComplete, Error
    from atomac import AXKeyboard
    from atomac import AXKeyCodeConstants

from lib.singleton import Singleton
from lib.loghelper import LogHelper
from configuration.mac.mac_config_loader import MAC_CONFIG
from lib.cmdhelper import CmdHelper


class MacUIUtils(object):

    __metaclass__ = Singleton

    @staticmethod
    def wait_element(search_from,  timeout=None, sleep_time=None, method='findFirstR', **matcher):
        """
        :param search_from:
        :param timeout:
        :param sleep_time:
        :param method:
        :param matcher:
        :return:
        """
        if timeout is None:
            timeout = MAC_CONFIG.get('ELEMENT_WAIT_TIME')
        if sleep_time is None:
            sleep_time = MAC_CONFIG.get('ELEMENT_WAIT_GRANULARITY')

        if search_from is None:
            raise Exception("search from is empty")

        current_wait_second = 0
        kwargs = {}
        for (attr, value) in matcher.items():
            if attr.startswith('AX'):
                kwargs[attr] = value

        func = getattr(search_from, method)
        result = func(**kwargs)
        while (not result) and current_wait_second < timeout:
            time.sleep(sleep_time)
            result = func(**kwargs)
            current_wait_second += sleep_time
        try:
            if result:
                return result
        except Exception as e:
            LogHelper.error(e)
            return None

    @staticmethod
    def click_button(btn_handle):
        #LogHelper.info('click button {}'.format(btn_handle.AXTitle))
        try:
            btn_handle.Press()
        except ErrorCannotComplete  as e:
            LogHelper.error(e.message)
        except Error as e:
            LogHelper.error(e.message)

    @staticmethod
    def click_radio_button(radio_button_handle):
        LogHelper.info('click radio button {}'.format(radio_button_handle.AXTitle))
        try:
            radio_button_handle.Press()
        except ErrorCannotComplete as e:
            LogHelper.error(e.message)
        except Error as e:
            LogHelper.error(e.message)

    @staticmethod
    def click_checkbox(checkbox_handle, check=True):
        LogHelper.info('check checkbox')
        current_status = checkbox_handle.AXValue
        if current_status == 1:
            LogHelper.info('checkbox checked')
            if not check:
                checkbox_handle.Press()
        if current_status == 0:
            LogHelper.info('checkbox checked')
            if check:
                checkbox_handle.Press()

    @staticmethod
    def wait_enabled(obj_handle, timeout=60):
        current_status = obj_handle.AXEnabled
        current_wait_second = 0
        while not current_status and current_wait_second < timeout:
            time.sleep(2)
            current_status = obj_handle.AXEnabled
            current_wait_second += 2
        return obj_handle

    @staticmethod
    def make_focus(control):
        result = False
        control_parent = control.AXParent
        for i in  range(0, len(control_parent.AXChildren)):
            if control.AXFocused:
                result = True
                break
            else:
                control_parent.sendKey(AXKeyCodeConstants.TAB)
        return result

    @staticmethod
    def get_element_title(element):
        title = None
        if element.getAttributes().count('AXTitle') != 0:
            title = element.AXTitle

        return title

    @staticmethod
    def empty_text(textbox):
        textbox.sendKey(AXKeyCodeConstants.TAB)
        if not textbox.AXFocused:
            MacUIUtils.make_focus(textbox)
        textbox.sendKey(AXKeyCodeConstants.DELETE)

    @staticmethod
    def input_text(textfield_handle, text):
        if textfield_handle and textfield_handle.getActions().count('Confirm') != 0:
            textfield_handle.Confirm()

        keyboard = AXKeyboard.loadKeyboard()
        upperSymbols_map = {
            ')': '0',
            '!': '1',
            '@': '2',
            '#': '3',
            '$': '4',
            '%': '5',
            '^': '6',
            '*': '7',
            '(': '8',
            ')': '9',
            '_': '-',        # Dash
            '+':  '=',
            ':': ';',
            '\'': "\"",
            '{': "[",
            '}': "]",
            '<': ",",
            '>': ".",
            '?': "/",
        }

        upperSymbols = keyboard.get('upperSymbols')

        for ch in text:
            if (ch in upperSymbols):
                textfield_handle.sendKeyWithModifiers(upperSymbols_map.get(ch), [AXKeyCodeConstants.SHIFT])
            else:
                textfield_handle.sendKey(ch)

    @staticmethod
    def get_popmenu_items(popbutton_handle):
        LogHelper.info('get popmenu item')
        items = []
        popbutton_handle._activate()
        popbutton_handle.Press()
        popbutton_handle._activate()
        menu_handle = popbutton_handle.findFirstR(AXRole='AXMenu')
        menu_items = menu_handle.AXChildren
        for menu_item in menu_items:
                items.append(menu_item.AXTitle)
        return items

    @staticmethod
    def click_popmenu_item_by_index(popbutton_handle, index=0):
        popbutton_handle._activate()
        popbutton_handle.Press()
        popbutton_handle._activate()
        menu_items = popbutton_handle.findAllR(AXRole='AXMenuItem')
        try:
            menu_item = menu_items[index]
            menu_item.activate()
            menu_item.Press()
        except ErrorCannotComplete as e:
            LogHelper.error(e.message)

    @staticmethod
    def click_popmenu_item_by_value(popbutton_handle, value):
        popbutton_handle._activate()
        popbutton_handle.Press()
        popbutton_handle._activate()
        menu_item = popbutton_handle.findFirstR(AXRole='AXMenuItem', AXTitle=value)
        try:
            menu_item.activate()
            menu_item.Press()
        except ErrorCannotComplete as e:
            LogHelper.error(e.message)

    @staticmethod
    def get_table_cells(table_handle):
        result = table_handle
        table = []
        for i in result.AXRows:
            cells = i.findAllR(AXRole='AXTextField')
            row = []
            for cell in cells:
                row.append(cell.AXValue)
            table.append(row)

        return table

    @classmethod
    def normalize_role(cls, text):

        role_text = 'AX' + text.lower().replace('ax', '').title()
        role = ""
        if role_text == 'AXTextfiled':
            role = 'AXTextFiled'

        if role_text == 'AXStatictext':
            role = 'AXStaticText'

        return role

    @classmethod
    def normalize_property(cls, property):
        property = 'AX' + property.lower().replace('ax', '').title()
        return property

    @staticmethod
    def select_nodes(browser_handle, tree, node_matcher='AXStaticText'):
        import re
        nodes = re.split(r'/', tree)
        nodes = filter(lambda x: len(x) > 0, nodes)
        current_level = -1
        for node in nodes:
            current_level += 1
            LogHelper.info("search {node} node!".format(node=node))
            scroll_area_top = MacUIUtils.wait_element(browser_handle, method='findFirstR', AXRole='AXScrollArea')
            scroll_areas = MacUIUtils.wait_element(scroll_area_top, method='findAllR', AXRole='AXScrollArea')
            sc = scroll_areas[current_level]
            entities = MacUIUtils.wait_element(sc, method='findAllR', AXRole=node_matcher)
            result = False
            for entity in entities:
                name = entity.AXValue
                if name == node:
                    LogHelper.info('{name} node found!'.format(name=name))
                    result = True
                    entity.activate()
                    entity.clickMouseButtonLeft(MacUIUtils.__rect_center(entity))
                    time.sleep(1)
                    entity.activate()
                if result:
                    break
            if not result:
                raise Exception("node {node} is not selected".format(node=node))
                return

    @staticmethod
    def __rect_center(entity):
        """
        cal rect center
        :param entity:
        :return: list: pos_x pos_y
        """
        up_x, up_y = entity.AXPosition
        height, width = entity.AXSize
        center_x = up_x + int(height/2)
        center_y = up_y + int(width/2)
        return center_x, center_y

    @staticmethod
    def mouse_click_center(obj_handle):
        center = MacUIUtils.__rect_center(obj_handle)
        obj_handle.clickMouseButtonLeft(center)

    @staticmethod
    def double_click(obj_handle):
        center = MacUIUtils.__rect_center(obj_handle)
        obj_handle.doubleClickMouse(center)

    @staticmethod
    def get_root_volume_name():
        cmd = 'diskutil info / | grep "Volume Name"'
        output = CmdHelper.run(cmd)
        volume_name = ''
        import re
        match = re.findall(r':(.*)', output)
        if match:
            volume_name = match[0].strip().lstrip()

        return volume_name


    @staticmethod
    def get_root_window_from_app(app, **matcher):
        root = app.findFirstR(AXRole='AXWindow', **matcher)
        return  root


    @staticmethod
    def is_element_exist(search_from, method='findFirstR',**matcher ):
        result = None
        func = getattr(search_from, method)
        el = func(**matcher)
        if el:
            result = el

        return result


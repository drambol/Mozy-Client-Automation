import  time

from lib.platformhelper import PlatformHelper

if PlatformHelper.is_mac():
    import atomac

class MacFryrElement(object):

    app = None
    # restore_manager = None
    element = None

    def __init__(self, matcher, index=0, wait_time=1):
        if self.app == None:
            atomac.launchAppByBundleId('com.mozy.restoremanager')
            time.sleep(2)
            self.app = atomac.getAppRefByBundleId('com.mozy.restoremanager')
            self.app.activate()
            self.restore_manager = self.app.findFirstR(AXRole='AXWindow', AXIdentifier='_NS:6')
        kwargs = {}
        for (attr, value) in matcher.items():
            kwargs[attr] = value
        time.sleep(wait_time)
        if index == 0:
            self.element = self.restore_manager.findFirstR(**kwargs)
            if self.element == None:
                self.element = self.app.findFirstR(**kwargs)
        else:
            self.element = self.restore_manager.findAllR(**kwargs)[index]
            if self.element == None:
                self.element = self.app.findAllR(**kwargs)[index]

    def click(self):
        try:
            self.element.Press()
        except:
            pass

    def send_keys(self, text):
        keyboard = atomac.AXKeyboard.loadKeyboard()
        upperSymbols_map = {
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
            '_': '-',  # Dash
            '+': '=',
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
                self.element.sendKeyWithModifiers(upperSymbols_map.get(ch), [atomac.AXKeyCodeConstants.SHIFT])
            else:
                self.element.sendKey(ch)

    def force_send(self, text):
        self.left_click()
        self.send_keys(text)

    def left_click(self):
        position = self.element.AXPosition
        size = self.element.AXSize
        click_position = ((position[0] + size[0]/2), (position[1] + size[1]/2))
        self.element.clickMouseButtonLeft(click_position)

    def enter_username(self, username):
        self.element.sendKey(atomac.AXKeyCodeConstants.TAB)
        self.element.sendKey(atomac.AXKeyCodeConstants.TAB)
        self.send_keys(username)

    def enter_password(self, password):
        self.element.sendKey(atomac.AXKeyCodeConstants.TAB)
        self.send_keys(password)

    def enter_personal_key(self, password):
        self.element.sendKey(atomac.AXKeyCodeConstants.TAB)
        self.send_keys(password)

    def is_visible(self):
        if self.element != None:
            return True
        return False

    def get_text(self):
        return str(self.element._getAttribute('AXValue'))

    def mouse_click(self, kwargs):
        self.element = self.element.findFirstR(**kwargs)
        position = self.element.AXPosition
        size = self.element.AXSize
        click_position = ((position[0] + size[0] / 2), (position[1] + size[1] / 2))
        self.element.clickMouseButtonLeft(click_position)
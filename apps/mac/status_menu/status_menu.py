from apps.mac.mac_gui_installer.mac_gui_installer import AppUIElement


class StatusMenu(object):
    def __init__(self, appname):
        self._menu = AppUIElement.from_localized_name(appname, {'AXRole': 'AXMenuBarItem'})

    @property
    def menu(self):
        return self._menu

    @menu.setter
    def menu(self, value):
        self._menu = value

    def left_click(self):
        self.menu.left_click()

    def right_click(self):
        self.menu.right_click()

    def expand(self):
        if not self.menu.has_child():
            self.left_click()

    def collapse(self):
        if self.menu.has_child():
            self.left_click()

    def find_menu_item_by_index(self, index):
        return self.menu.find_child({'AXRole': 'AXMenuItem'}, index=index)

    def get_menu_text_by_index(self, index):
        return self.menu.find_child({'AXRole': 'AXMenuItem'}, index=index).get_title()

    def get_left_size(self):
        # menu_text = self.get_menu_text_by_index(2)
        menu_name = "Sending Files:"
        menu_text = self.find_menu_item_by_name(menu_name, 0, 30).get_title()
        import re
        matches = re.findall(r' \((.*) ', menu_text)
        print matches[0]
        left_size = float(matches[0]) or 0.0
        return left_size

    def find_menu_item_by_name(self, menuname, index=0, wait_time=1):
        # print menuname
        matcher = {'AXRole': 'AXMenuItem'}
        matcher['AXTitle'] = menuname + '*'
        # ele = self.menu.find_child(matcher=matcher)
        # print ele
        # return ele
        return self.menu.find_child(matcher=matcher, index=index, wait_time=wait_time)

    def click_menu_item(self, menuname):
        self.expand()
        matcher = {'AXRole': 'AXMenuItem'}
        matcher['AXTitle'] = menuname + '*'
        self.menu.find_child(matcher=matcher).left_click()


if __name__ == "__main__":
    brand = "Mozy Enterprise Status"
    menu = StatusMenu(brand)
    menu.expand()
    item = menu.find_menu_item_by_name("Files Pending:")
    title = menu.get_menu_text_by_index(5)
    print title
    text = item.get_title()

    print item

    import re
    match = re.findall(r' \((.*) ', text)
    print match[0]
    size = float(match[0]) or 0.0
    print size
    menu.collapse()

    print "Hello"

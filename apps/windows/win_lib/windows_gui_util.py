
from lib.platformhelper import PlatformHelper
if PlatformHelper.is_win():
    from pywinauto.base_wrapper import ElementNotVisible, ElementNotEnabled
    from pywinauto.findbestmatch import MatchError

from lib.loghelper import LogHelper
from lib.singleton import Singleton


class WindowsGUIUtil(object):

    __metaclass__ = Singleton

    @staticmethod
    def click_button(button):
        result = False
        try:
            button.set_focus()
            button.Click()
        except NotImplementedError as e:
            LogHelper.error(e.message)
        else:
            result = True
        return result

    @staticmethod
    def click_radio_button(radio_button):
        result = False
        try:
            radio_button.set_focus()
            radio_button.CheckByClick()
        except NotImplementedError as e:
            LogHelper.error(e.message)
        else:
            result = True
        return result

    @staticmethod
    def select_combobox(combo_box, index=0):
        result = False
        try:
            combo_box.Select(index)
        except NotImplementedError as e:
            LogHelper.error(e.message)
        else:
            result = True
        return result

    @staticmethod
    def check(item):
        result = False
        try:
            # pywinauto BUG: is_checked() returns False if CHECKED, True if UNCHECKED
            if item.is_checked():
                item.Click(where='check')
        except RuntimeError as e:
            LogHelper.error(e.message)
        else:
            result = True
        return result

    @staticmethod
    def uncheck(item):
        result = False
        try:
            # pywinauto BUG: is_checked() returns False if CHECKED, True if UNCHECKED
            if not item.is_checked():
                item.Click(where='check')
        except RuntimeError as e:
            LogHelper.error(e.message)
        else:
            result = True
        return result

    @staticmethod
    def is_selected(item):
        result = False
        cl = item.get_check_state()
        print cl
        if item.get_check_state() == 1:
            result = True
        return result

    @staticmethod
    def uncheck_checkbox(item):
        if item.get_check_state() == 1:
            item.uncheck()

    @staticmethod
    def choose_checkbox(checkbox, checked=True):
        pass
        # current_status = checkbox.AXValue
        # if current_status == 1:
        #     if not checked:
        #         checkbox.Press()
        # if current_status == 0:
        #     if checked:
        #         checkbox.Press()

    @staticmethod
    def input_text(text_edit, txt):
        result = False
        LogHelper.info(txt)
        try:
            # text_edit.set_focus()
            text_edit.set_text(txt)
        except NotImplementedError as e:
            LogHelper.error(e.message)
        else:
            result = True
        return result

    @staticmethod
    def input_edit_content(edit, content):
        result = False
        LogHelper.info(content)
        try:
            edit.type_keys(content)
        except NotImplementedError as e:
            LogHelper.error(e.message)
        else:
            result = True
        return result

    @staticmethod
    def get_treeview_items(tr, selected="C:"):
        """
        :param tr: treeview
        :param selected: selected drive without label
        :return: drive with label, just like what we see in OS. e.g. "Local Disk (C:)"
        """
        print tr.ItemCount()
        print selected.upper()
        for i in range(tr.ItemCount()-1):

            if selected.upper() in tr.GetItem([0, i]).Text():
                return tr.GetItem([0, i]).Text()

    @staticmethod
    def selectinfilesystem(file_treeview, root_path="C:/test_data"):
        """
        :param file_treeview: systreeview
        :param root_path: folder to check
        :return: Bool
        """
        # # Note: Expand root folder, then all root drives can be access.
        # file_treeview.GetItem([0]).Click(double=True)
        file_treeview.GetItem([0]).Click()

        # TODO: Hard code to only two level folders, refactor later
        driver = root_path.split("/")[0]    #"C:"
        folder = root_path.split("/")[1]    #"test_data"

        # Get drive label
        driverwithlabel = WindowsGUIUtil.get_treeview_items(file_treeview, driver)
        print driverwithlabel

        items = [file_treeview.GetItem([0]).Text(), driverwithlabel, folder]
        print items
        file_treeview.GetItem(items).Click(double=True, where='check')

    @staticmethod
    def listview_count(lv):
        """
        :param tr: listview
        :return: number of list items
        """
        return lv.ItemCount()

    @staticmethod
    def select_listview_item(lv, selected="My Documents", uncheck=False):
        """
        :param tr: listview
        :return: all list items
        """
        count = WindowsGUIUtil.listview_count(lv)
        for i in range(count - 1):
            if selected.upper() in lv.Item(i).Text():
                if uncheck:
                    WindowsGUIUtil.uncheck(lv.Item(i))
                else:
                    WindowsGUIUtil.check(lv.Item(i))
                # lv.Check(i)
                # return lv.Item(i).Text()

    @staticmethod
    def is_visible(element):
        result = False
        try:
            element.is_visible()
            LogHelper.info("Element is visible.")
        except MatchError as e:
            LogHelper.error("ERROR: Can't find the element.")
            LogHelper.error(e.message)
            return result
        except ElementNotVisible as e:
            LogHelper.error("ERROR: The Element is not visible.")
            LogHelper.error(e.message)
            return result
        except RuntimeError as e:
            LogHelper.error("ERROR: Runtime Fatal Error.")
            LogHelper.error(e.message)
            return result
        else:
            print "Element is visible."
            result = True
        return result

    @staticmethod
    def is_enabled(element):
        result = False
        try:
            element.is_enabled()
            LogHelper.info("Element is enabled.")
        except ElementNotEnabled as e:
            LogHelper.error("ERROR: The Element is not enabled.")
            LogHelper.error(e.message)
            return result
        except RuntimeError as e:
            LogHelper.error("ERROR: Runtime Fatal Error.")
            LogHelper.error(e.message)
            return result
        else:
            print "Element is enabled."
            result = True
        return result

    @staticmethod
    def set_time(element, hour, minute):
        time = element.get_time()
        print time
        year = time.wYear
        month = time.wMonth
        dayofweek = time.wDayOfWeek
        day = time.wDay
        second = time.wSecond
        milliseconds = time.wMilliseconds
        element.set_time(year, month, dayofweek, day, hour, minute, second, milliseconds)

    @staticmethod
    def set_trackbar(element, position):
        pos = element.get_position()
        print pos
        element.set_position(position)

    @staticmethod
    def get_combobox_text(element):
        data = element.ItemTexts()
        print data
        return data

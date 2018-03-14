import time

from lib.platformhelper import PlatformHelper
if PlatformHelper.is_mac():
    import atomac

from apps.mac.mac_lib.mac_ui_util import MacUIUtils

class Element(object):
    """
    Mac Element Class
    Mac Element can be any UI control in a UI base
    """
    def __init__(self, name, matcher, element_wait_time=None, bundle='com.apple.systempreferences', parent_matcher=None):
        self._name = name
        self._matcher = matcher
        self.element_wait_time = element_wait_time or 30
        self.root = self.search_from(bundle_id=bundle, parent_matcher=parent_matcher, element_wait_time=self.element_wait_time)

    @property
    def name(self):
        return self._name

    @property
    def matcher(self):
        return self._matcher

    @name.setter
    def name(self, value):
        self._name = value

    @matcher.setter
    def matcher(self, value):
        self._matcher = value

    @staticmethod
    def search_from(bundle_id='com.apple.systempreferences', parent_matcher=None, element_wait_time=60):
        kwargs = {}
        if parent_matcher is None:
            kwargs['AXRole']='AXWindow'
            kwargs['AXTitle']='MozyPro'
        else:
            for (attr, value) in parent_matcher.items():
                if attr.startswith('AX'):
                    kwargs[attr] = value
        root_wait_time = element_wait_time

        def get_root(bundle_id=bundle_id, kwargs=kwargs, wait_time=root_wait_time):
            try:
                atomac.launchAppByBundleId(bundle_id)
                app = atomac.getAppRefByBundleId(bundle_id)
                app.activate()
            except ValueError as e:
                atomac.launchAppByBundleId(bundle_id)
                app = atomac.getAppRefByBundleId(bundle_id)
                app.activate()
            current_wait_second = 0
            parent = app.findFirstR(**kwargs)
            while (parent is None) and current_wait_second < wait_time:
                sleep_time = 5
                time.sleep(sleep_time)
                parent = app.findFirstR(**kwargs)
                current_wait_second += sleep_time
            if parent is None:
                print "error: parent is not find for kwargs %s in %d" % (kwargs, wait_time)
            else:
                parent.activate()
            return parent
        return get_root


class MacMozyUIBase(object):
    """
    MacMozyUIBase
    """

    elements = []

    def __init__(self):
        for element in self.elements:
            element_name = element.name
            matcher = element.matcher
            wait_time = element.element_wait_time or 30
            root = element.root

            def define_property(self, matcher=matcher, wait_time=wait_time):
                search_from = root(wait_time=wait_time)
                current_wait_second = 0
                kwargs = {}
                for (attr, value) in matcher.items():
                    if attr.startswith('AX'):
                        kwargs[attr] = value

                if not search_from:
                    return None

                result = search_from.findFirstR(**kwargs)

                while (not result) and current_wait_second < wait_time:
                    sleep_time = 5
                    time.sleep(sleep_time)
                    result = search_from.findFirstR(**kwargs)
                    current_wait_second += sleep_time

                return result

            setattr(self.__class__, element_name, property(define_property))

    def get_element(self, element_name):
            els = self.__class__.elements
            results = filter(lambda x: x.name == element_name, els)
            return results[0]

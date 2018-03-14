
import time


class WindowsUIBase(object):

    elements = []

    def __init__(self):

        for element in self.elements:
            element_name = element.name
            matcher = element.matcher
            wait_time = element.element_wait_time or 30


            def define_property(self, matcher=matcher, wait_time=wait_time):

                total_wait = 0
                element.wait_window()
                self._window = element.window
                if element.window is None:
                    return None

                result = element.retrieve(element.window, matcher)

                while not result and total_wait < wait_time:
                    time.sleep(1)
                    element.wait_window()
                    result = element.retrieve(element.window, matcher)
                    total_wait += 1

                return result

            setattr(self.__class__, element_name, property(define_property))

    def get_element(self, element_name):
            els = self.__class__.elements
            results = filter(lambda x: x.name == element_name, els)
            return results[0]

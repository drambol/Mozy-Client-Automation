#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


import time

from apps.mac.mac_lib.mozy_ui_element import MacMozyUIBase, Element
from apps.mac.mac_lib.mac_ui_util import MacUIUtils
from apps.mac.mac_controller.mac_controller import MacController
from lib.cmdhelper import CmdHelper


class ViewAndRestoreWindow(MacMozyUIBase):
    """
    description:
    """
    app_bundle = 'com.mozypro.restore'
    parent_match = {'AXRole': 'AXWindow', 'AXIdentifier': "_NS:316"}

    elements =[]
    elements.append(Element("btn_search", {'AXRole': 'AXButton', 'AXDescription': "Search"},
                            bundle=app_bundle, parent_matcher=parent_match))
    elements.append(Element("tf_search", {'AXRole': 'AXTextField', 'AXIdentifier': "_NS:110"},
                            bundle=app_bundle, parent_matcher=parent_match))
    elements.append(Element("ol_restore", {'AXRole': 'AXOutline'},
                            bundle=app_bundle, parent_matcher=parent_match))
    elements.append(Element("btn_restore", {'AXRole': 'AXButton'},
                            bundle=app_bundle, parent_matcher=parent_match))
    elements.append(Element('browser_restore', {'AXRole': 'AXBrowser', 'AXIdentifier': "_NS:93"},
                            bundle=app_bundle, parent_matcher=parent_match))
    elements.append(Element('btn_browse', {'AXRole': 'AXButton', 'AXTitle': "Browse*"},
                            element_wait_time=120, bundle=app_bundle, parent_matcher=parent_match))

    elements.append(Element('btn_close', {'AXRole': 'AXButton', 'AXRoleDescription': "close*"},
                            bundle=app_bundle, parent_matcher=parent_match))
    elements.append(Element('pm_backupdate', {'AXRole': 'AXPopUpButton'},
                            bundle=app_bundle, parent_matcher=parent_match))
    elements.append(Element('menu_backupdate', {'AXRole': 'AXMenu'},
                            bundle=app_bundle, parent_matcher=parent_match))
    elements.append(Element('pi_restore', {'AXRole': 'AXProgressIndicator'},
                            bundle=app_bundle, parent_matcher=parent_match)) # restore indicator

    def __init__(self):
        super(ViewAndRestoreWindow, self).__init__()

    def click_browse_button(self):
        MacUIUtils.click_button(self.btn_browse)

    #

    def restore_last_backup(self):
        MacUIUtils.click_popmenu_item_by_index(self.pm_backupdate, index=2)
        self.restore_root()
        self.close()

    def restore_root(self):
        root_handle = MacUIUtils.wait_element(self.browser_restore, AXRole='AXStaticText')
        node_name = root_handle.AXValue
        self.restore_entity(node_name)

    def wait_restore_finished(self, timeout=100):
        restore_finish = False

        wait_time = 0
        sleep_time = 3

        while self.pi_restore and wait_time < timeout:
            time.sleep(sleep_time)
            wait_time += sleep_time
            # self.__kill_security_agent()

        if self.pi_restore is None:
            restore_finish = True
        return restore_finish

    def restore_entity(self, entity_name):
        MacUIUtils.select_nodes(self.browser_restore, entity_name)
        self.btn_restore.Press()

        self.wait_restore_finished()

    def close(self):
        MacUIUtils.click_button(self.btn_close)

    @staticmethod
    def __kill_security_agent():
        is_sa_exist = False
        find_cmd = 'lsappinfo find name=SecurityAgent'
        output = CmdHelper.run(find_cmd).replace('\n','')
        wait_time = 0
        while (not output) and wait_time<60:
            time.sleep(5)
            wait_time += 5
            output = CmdHelper.run(find_cmd)
        if wait_time>=60:
            print 'timeout'
        if output:
            cmd = MacController.prefix_for_sudo() + 'sudo -S killall -9 "SecurityAgent"'
            CmdHelper.run(cmd)

    def get_outline_rows(self):
        rows = self.ol_restore.findAll(AXRole='AXRow')
        return rows

    def click_restore_button(self):
        MacUIUtils.click_button(self.btn_restore)

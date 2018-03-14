import time
from behave import *

from apps.mac.mac_gui_client.mac_gui_client import MacGUIClient


@When('I visit "{tab_name}" tab')
def stem_impl(context, tab_name):
    if tab_name.lower() == 'files & folders':
        MacGUIClient().files_folder_tab.visit()

    if tab_name.lower() == 'summary':
        MacGUIClient().summary_tab.visit()

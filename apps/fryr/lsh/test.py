from apps.fryr.test_data import Test_Data
from apps.web_support.bus_page import BusPage
from apps.web_support.freyja_page import FreyjaPage
from apps.fryr.win.winfryr_controller import WinFryR_Controller
from apps.fryr.win.winfryr_lsh_controller import WinFryR_LSH_Controller
import os, re, win32api

# BusPage.visit()
# BusPage.login()
# BusPage.search_partner("LSH Integration MozyEnt Noedit")
# BusPage.act_as_partner()
# BusPage.go_to_eDiscovery()
# Test_Data.clear_download_folder()
# FreyjaPage.define_lsh_search("version")
# FreyjaPage.create_mzdx()
# FreyjaPage.close_browser()
#
WinFryR_LSH_Controller.clear_restore_folder('auto_restores')
WinFryR_LSH_Controller.restore_by_mzdx()
WinFryR_LSH_Controller.export_edrm(version="v1.2")
WinFryR_LSH_Controller.export_edrm(version="v2.0")

WinFryR_LSH_Controller.delete_all_jobs()
WinFryR_LSH_Controller.launch_lsh_restore_manager()
WinFryR_LSH_Controller.archive_job()



print 'Done'

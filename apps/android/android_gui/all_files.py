from apps.android.appium_driver import Driver
from apps.android.android_gui.my_mozy_view import My_Mozy_View
from lib.loghelper import LogHelper

class All_Files_View(Driver):

    xpaths = {'all_files_textview': "//*[@text='All Files']",
              'sync_layout': "//*[@class='android.widget.ListView']//*[@text='Sync']",
              'backups_layout': "//*[@class='android.widget.ListView']//*[@text='Backups']",
              'backup_machines': "//*[@class='android.widget.ListView']//*[@class='android.widget.LinearLayout']",
              'machine_name': "//*[@class='android.widget.TextView']",
              'machine_description': "//*[@class='android.widget.TextView']/following-sibling::*[1]",
              }

    @classmethod
    def navigate_to(self):
        try:
            self.locate_element(self.xpaths['all_files_textview'], wait_time=1).click()
        except:
            My_Mozy_View.navigate_to()
            self.locate_element(self.xpaths['all_files_textview']).click()

    @classmethod
    def verify_sync(self):
        assert self.locate_elements(self.xpaths['sync_layout'], wait_time=1)[0].is_displayed()
        assert self.locate_elements(self.xpaths['sync_layout'], wait_time=1)[1].is_displayed()

    @classmethod
    def verify_backups(self):
        assert self.locate_element(self.xpaths['backups_layout'], wait_time=1).is_displayed()
        backup_machines = self.locate_elements(self.xpaths['backup_machines'])
        machine_quantity = len (backup_machines) / 2
        machines = []
        for i in range(machine_quantity):
            index = i * 2
            assert backup_machines[index].is_displayed()
            machine_name = backup_machines[index].find_element_by_xpath(self.xpaths['machine_name']).text
            if machine_name <> 'Sync':
                machine_desc = backup_machines[index].find_element_by_xpath(self.xpaths['machine_description']).text
                machines.append(Machine(machine_name, machine_desc))

        for i in range(len(machines)):
            LogHelper.info('Machine: ' + machines[i].name + ' ' + machines[i].description)

        return machines


class Machine(object):

    def __init__(self, name='', description=''):
        self.name = name
        self.description = description


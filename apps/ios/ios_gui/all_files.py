from apps.ios.appium_driver import Driver
from lib.loghelper import LogHelper

class All_Files_View(Driver):

    machines = []
    xpaths = {'all_files_textview': "//*[@label='All Files']",
              'sync_layout': "//UIAStaticText[@label='Sync']",
              'backups_layout': "//UIAStaticText[@label='Backups']",
              'backup_machines': "//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIATableCell",
              }

    @classmethod
    def navigate_to(self):
        try:
            self.locate_element(self.xpaths['all_files_textview']).click()
        except:
            pass

    @classmethod
    def verify_sync(self):
        self.navigate_to()
        assert self.locate_elements(self.xpaths['sync_layout'], wait_time=30)[0].is_displayed()
        assert self.locate_elements(self.xpaths['sync_layout'])[1].is_displayed()
        LogHelper.info('Sync folder is displayed for the Mozy account.')
        print('Sync folder is displayed for the Mozy account.')

    @classmethod
    def verify_backups(self):
        assert self.locate_element(self.xpaths['backups_layout']).is_displayed()
        backup_machines = self.locate_elements(self.xpaths['backup_machines'])
        machine_quantity = len (backup_machines)
        self.machines = []
        for i in range(machine_quantity):
            index = str(i + 1)
            assert backup_machines[i].is_displayed()
            machine_xpath = self.xpaths['backup_machines'] + '[' + index + ']/UIAStaticText[1]'
            machine_name = self.driver.find_element_by_xpath(machine_xpath).text
            if machine_name != 'Sync':
                description_xpath = self.xpaths['backup_machines'] + '[' + index + ']/UIAStaticText[2]'
                machine_desc = self.driver.find_element_by_xpath(description_xpath).text
                self.machines.append(Machine(machine_name, machine_desc))

        for i in range(len(self.machines)):
            LogHelper.info('Machine: ' + self.machines[i].name + ' ' + self.machines[i].description)
            print('Machine: ' + self.machines[i].name + ' ' + self.machines[i].description)

        return self.machines


class Machine(object):

    def __init__(self, name='', description=''):
        self.name = name
        self.description = description


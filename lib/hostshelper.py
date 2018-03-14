import os
import re
import shutil
from configuration.windows.windows_config_loader import WIN_CONFIG


class HostsHelper(object):

    def __init__(self, oem, file_path):   #file_path = 'r'C:\WINDOWS\system32\drivers\etc'
        self.oem = oem
        self.src = file_path + '\hosts'   #r'C:\WINDOWS\system32\drivers\etc\hosts'
        self.temp = file_path + '\Temp_Host\hosts'
        self.mid = file_path + '\Temp_Host'


    def add_hosts_to_file(self, env):  #add hosts to hosts-file
        host_path = self.src
        input = open(host_path, 'r')
        input.close()
        output = open(host_path, 'a')
        if env.upper() in WIN_CONFIG["QA_ENVIRONMENT"].keys():
            subkeys = WIN_CONFIG["QA_ENVIRONMENT"][env.upper()]["fedid"].keys()
        else:
            raise KeyError("unsupport environment")
        for subkey in subkeys:
            subs = 'host'
            res = re.match(subs,subkey)
            if res is not None:
                host_hash = WIN_CONFIG["QA_ENVIRONMENT"][env.upper()]["fedid"][subkey]
                print host_hash
                for key, value in host_hash.items():
                    output.write(key+" ")
                    output.write(value)
                    output.write('\n')
            # else:
            #     host_reg = WIN_CONFIG["QA_ENVIRONMENT"][env.upper()]["fedid"][subkey]
            #     self.set_keyed_reg(subkey, host_reg)
        # print host_reg

    def duplicate_hostfile(self):
        src = self.src
        des = self.temp
        file_path = self.mid
        if os.path.isdir(file_path):
            print src
            print des
            shutil.copy(src,des)
        else:
            os.mkdir(file_path)
            shutil.copy(src, des)

    def remove_hostfile(self):
        if os.path.exists(self.src) and os.path.exists(self.temp):
            os.remove(self.src)
            return True
        else:
            print "hosts file does not exist"
            return False

    def recover_hostfile(self):
        src = self.temp
        des = self.src
        folder = self.mid
        shutil.copy(src, des)
        os.remove(src)
        shutil.rmtree(folder)


if __name__ == '__main__':
    # HostsHelper("mozypro",r'C:\WINDOWS\system32\drivers\etc').duplicate_hostfile()
    HostsHelper("mozypro",r'C:\WINDOWS\system32\drivers\etc').add_hosts_to_file("qa12")
    # HostsHelper().remove_hostfile()
    # HostsHelper().recover_hostfile()


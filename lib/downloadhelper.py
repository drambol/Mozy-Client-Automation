import urllib2
import os
from lib import filehelper

class Download_Helper(object):

    def __init__(self, url):
        self.url = url


    def get_download_url(self, pattern):
        url = "%s/downloads/%s" % (self.url, pattern)
        return url


    def download_package(self, url, dest):
        """
        :param download_url:
        :param dest:
        :return: local destination of download package
        """
        package = url.split('/')[-1]
        filehelper.FileHelper().create_directory(dest)
        dest_full_path = os.path.join(dest,package)
        req = urllib2.Request(url)

        if filehelper.FileHelper().file_exist(dest_full_path):
            filehelper.FileHelper().delete_file(dest_full_path)

        with open(dest_full_path, 'wb') as output:
            output.write(urllib2.urlopen(req).read())

        return dest_full_path

if __name__ == '__main__':
    dest = 'C:\\file'
    ad= Download_Helper().create(dest)
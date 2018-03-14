import os
from lib.filehelper import FileHelper


class DataHelper(object):

    @staticmethod
    def create_testfile(filename, dir, size, pattern="random", **kwargs):
        # filename = DataProperty(filename, dir, size, pattern,  **kwargs

        FileHelper.create_file(os.path.join(dir, filename), True, size, pattern)

    def set_property(self, property):
        pass


if __name__ == "__main__":
    DataHelper().create_testfile("abc", "/tmp", 100000)









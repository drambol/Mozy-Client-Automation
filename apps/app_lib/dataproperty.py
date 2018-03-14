import os


class DataProperty(object):

    def __init__(self, filename, dir, size, pattern="random", **kwargs):
        self.filename = filename
        self.dir = dir
        self.full_path = os.path.join(dir, filename)
        self.pattern = pattern

        for (key ,value) in kwargs.items():
            self.__parse_key(key,value)

    def __parse_key(self, key,value):

        valid_keys = ("owner", "group", "permission", "symlink_dest")
        if key in valid_keys:
            setattr(self, key, value)


if __name__ == "__main__":
    test = DataProperty("asd", "/tmp",  1000, owner="christine", aaa="asdf")
    # print test










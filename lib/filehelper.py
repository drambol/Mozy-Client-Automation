#!/usr/bin/env python
#
# Copyright (c) Maginatics, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


import filecmp
import hashlib
import os
import random
import shutil
import string
import fnmatch
import stat
import re

from lib.singleton import Singleton
from lib.platformhelper import PlatformHelper
from lib.cmdhelper import CmdHelper


class FileHelper(object, filecmp.dircmp):
    """
    class that hold method to handle file system
    like create files
    """
    __metaclass__ = Singleton

    @staticmethod
    def file_exist(path):
        """
        method to test if file existed?
        """
        return os.path.isfile(path)

    @staticmethod
    def dir_exist(dir):
        """
        method to test if a director existed
        :param dir: dir
        :return: True or False
        """

        return os.path.isdir(dir)

    @staticmethod
    def file_ext(filename):
        """
        get file extension from path
        :param filename: filename
        :return: file extention without .  e.g. jpg,
        """
        return os.path.splitext(filename)[1][1:]

    @staticmethod
    def create_file(path, overwrite=True, size=1024, content="random"):
        """
          method to create test files
        """
        basedir = os.path.dirname(path)
        FileHelper.create_directory(basedir)
        if PlatformHelper.is_Linux(): # or PlatformHelper.is_mac():
            cmd = 'sudo chmod -R 777 {path}'.format(path=basedir)
            CmdHelper.run(cmd)

        if content == "random":
            FileHelper._create_file_random(path, overwrite, size, 1024)
        else:
            FileHelper._create_file_pattern(path, overwrite, size, content)

    @staticmethod
    def _create_file_random(path, overwrite, size, chunksize=1024):
        chars_written = 0

        if not overwrite and FileHelper.file_exist(path):
            os.remove(path)

        if not FileHelper.file_exist(path) or True == overwrite:
            newfile = open(path, "w+")

        # check to see that we have an existent, regular file
        try:

            # now put in the pattern enough to times to fill it up. pad with filler characters
            full_patterns_needed = size / chunksize
            filler_chars_needed = size % chunksize

            for i in range(0, full_patterns_needed):
                newfile.write(FileHelper._create_random_string(chunksize))

            for i in range(0, filler_chars_needed):
                newfile.write(FileHelper._create_random_string(1))

        except Exception as e:
            print e.message

        finally:
            newfile.close()

        return chars_written

    @staticmethod
    def create_directory(path, recursive=True):
        """
        :param path: directory path
        :return: path
        """
        path = os.path.abspath(path)
        sub_path = os.path.dirname(path)
        if not os.path.exists(sub_path) and recursive:
            FileHelper.create_directory(sub_path)
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except OSError:
                if PlatformHelper.is_Linux(): # or PlatformHelper.is_mac():
                    cmd = 'sudo mkdir -p {path}'.format(path=path)
                    CmdHelper.run(cmd)
        return path



    @staticmethod
    def delete_file(path):
        """
        :param path: delete file path
        :return:
        """

        if FileHelper.file_exist(path):
            os.remove(path)

    @staticmethod
    def delete_directory(dir):
        """
        delete directory and files

        """

        # if directory has file
        FileHelper.remove_tree(dir, True)

    @staticmethod
    def remove_tree(dir, topdown=True):
        for root, dirs, files in os.walk(dir, topdown=False):
            for name in files:
                filename = os.path.join(root, name)
                os.chmod(filename, stat.S_IWUSR)
                os.remove(filename)
            for name in dirs:
                try:
                    os.removedirs(os.path.join(root, name))
                except OSError as e:
                    if PlatformHelper.is_Linux(): # or PlatformHelper.is_mac():
                        CmdHelper.run('sudo rm -rf {path}'.format(path=os.path.join(root, name)))


    @staticmethod
    def _create_file_pattern(path, overwrite, size, pattern):

        if not overwrite and FileHelper.file_exist(path):
            os.remove(path)

        try:
            newfile = None
            if not FileHelper.file_exist(path) or True == overwrite:
                newfile = open(path, "w+")
                times_to_repeat_pattern = size / len(pattern)
                filler_bytes_needed = size % len(pattern)

            # write the pattern enough times
            for i in range(0, times_to_repeat_pattern):
                newfile.write(pattern)

            # write enough filler to get to the needed size
            for i in range(0, filler_bytes_needed):
                newfile.write(".")
        except Exception as e:
            print e.message

    @staticmethod
    def overwrite_file_content(path, starting_offset, length, pattern, filler_str="."):
        """
        :param path: file path
        :param starting_offset: offset
        :param length:  length to overwrite
        :param pattern: character pattern that to overwrite
        :param filler: . filter content if length/len(pattern) is not equal to integer
        :return:  chars that have written
        """

        chars_written = 0

        if FileHelper.file_exist(path):

            file = open(path, "r+")
            actual_offset = min(starting_offset, FileHelper.file_size(path))

            file.seek(actual_offset)

            full_patterns_needed = length / len(pattern)
            filler_chars_needed = length % len(pattern)

            for __ in range(full_patterns_needed):
                file.write(pattern)
                chars_written += len(pattern)

            for __ in range(filler_chars_needed):
                file.write(filler_str)
                chars_written += len(filler_str)

            file.close()

        return chars_written

    @staticmethod
    def overwrite_file_random(path, starting_offset, length):
        """
        usage: overwrite file content with random string
        :param path: file path
        :param starting_offset: offset
        :param length:  length to overwrite
        :return:  chars that have written
        """

        if FileHelper.file_exist(path):
            file = open(path, "r+")
            actual_offset = min(starting_offset, FileHelper.file_size(path))

            file.seek(actual_offset)

            random_str = FileHelper._create_random_string(length)
            file.write(random_str)
            file.close()

        return len(random_str)

    @staticmethod
    def insert_file_content(path, starting_offset, length, pattern="random"):

        if not FileHelper.file_exist(path):
            raise Exception("%s not existed")
            return

        file_size = FileHelper.get_file_size(path)

        if starting_offset > file_size:
            starting_offset = file_size

        tmpfile = FileHelper.get_dir(path) + os.sep + os.path.basename(path) + ".tmp"

        with open(path, "r+") as f1, open(tmpfile, "w+") as f2:
            before_postion = f1.read(starting_offset)
            f1.seek(starting_offset)
            after_position = f1.read()
            if pattern == "random":
                insert_content = FileHelper._create_random_string(length)
            else:
                insert_content = FileHelper._create_string_with_pattern(length, pattern)

            f2.write(before_postion)
            f2.write(insert_content)
            f2.write(after_position)

        FileHelper.move(tmpfile, path)

    @staticmethod
    def append_file_content(path, length, pattern="random"):
        """
        :param path: file path
        :param length:  length of character to append
        :param pattern: c
        :return:
        """
        file_size = FileHelper.get_file_size(path)
        FileHelper.insert_file_content(path, file_size, length, pattern)

    @staticmethod
    def truncate_file(path, size):
        if FileHelper.file_exist(path):
            file_size = FileHelper.get_file_size(path)
            if size > file_size:
                size = file_size
            tmpfile = FileHelper.get_dir(path) + os.sep + os.path.basename(path) + ".tmp"
            with open(path, "rw+") as f,  open(tmpfile,"w+") as f2:
                f2.write(f.read(size))
            FileHelper.move(tmpfile, path)
        else:
            raise Exception("%s is not existed" % path)

    @staticmethod
    def get_dir(path):
        return os.path.dirname(path)

    @staticmethod
    def file_size(path):
        """
        :param self:
        :param path: file path
        :return: size of a file. unit: B
        """
        try:
            size = -1
            f = open(path, "r")
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.close()
        except Exception, e:
            print e

        return size

    @staticmethod
    def _create_random_string(size):
        """
        create random string
        """
        seq = string.ascii_letters + string.digits
        keylist = [random.choice(seq) for _ in range(0, size)]
        return "".join(keylist)

    @staticmethod
    def _create_string_with_pattern(size, pattern, filter_str="."):
        """
        create string with pattern
        """
        output = ""
        repeat_number = size / len(pattern)
        filter_str_number = size % len(pattern)

        for __ in range(0, repeat_number):
            output += pattern

        for __ in range(0, filter_str_number):
            output += filter_str

        return output

    @staticmethod
    def md5(file):
        hash_md5 = hashlib.md5()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @staticmethod
    def sha256(file):
        sha256 = hashlib.sha256()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    @staticmethod
    def get_file_size(file):
        size = os.path.getsize(file)
        return size

    @staticmethod
    def is_file_same(file1, file2, method="sha256"):
        result = False
        file1_size = FileHelper.get_file_size(file1)
        file2_size = FileHelper.get_file_size(file2)

        if file1_size != file2_size:
            return result

        check_method = getattr(FileHelper, method)
        file1_check = check_method(file1)
        file2_check = check_method(file2)

        if file1_check == file2_check:
            result = True
        return result

    @staticmethod
    def copy_file(source, dst):
        shutil.copyfile(source, dst)

    @staticmethod
    def get_file_stat(file):
        """
        :param file:
        :return:  stat object
        """
        if not FileHelper.file_exist(file):
            raise Exception("%s is not existed" % file)
            return
        return os.stat(file)

    @staticmethod
    def move(source_file, target):
        """
        :param source_file: source file or directory
        :param target: target file
        :param overwrite: whether overwrite is target existed
        :return:
        """
        shutil.move(source_file, target)

    @staticmethod
    def rename(path, new_name):
        new_path = os.path.join(FileHelper.get_dir(path), new_name)
        FileHelper.move(path, new_path)

    @staticmethod
    def find_file(path, pattern):
        configfiles = []
        configfiles = [os.path.join(dirpath, f)
                       for dirpath, dirnames, files in os.walk(path)
                       for f in fnmatch.filter(files, pattern)]
        return configfiles


    @staticmethod
    def find_files(path, find_pattern, excluded_pattern=None, flag=''):
        include_files = FileHelper.find_file(path, find_pattern)
        if excluded_pattern:
            file_list = []
            for include_file in include_files:
                filename = os.path.basename(include_file)
                match = re.compile(excluded_pattern)
                if not re.match(match, filename):
                    file_list.append(include_file)
            return file_list
        else:
            return include_files


    @staticmethod
    def find_dir(path, pattern):
        configdirs = [os.path.join(dirpath, f)
                       for dirpath, dirnames, files in os.walk(path)
                       for f in fnmatch.filter(dirnames, pattern)]

        return configdirs

    @staticmethod
    def find_dirs(path, find_pattern, excluded_pattern=None, flag=''):
        include_dirs = FileHelper.find_dir(path, find_pattern)

        if excluded_pattern:
            dir_list = []
            for include_dir in include_dirs:
                filename = include_dir.split(os.sep)[-1]  # get dir
                match = re.compile(excluded_pattern)
                if not re.match(match, filename):
                    dir_list.append(include_dir)

            return dir_list
        else:
            return include_dirs

    @staticmethod
    def is_dir_same(dir1, dir2, method='shadow', exclude_pattern= None):
        """
        :param dir1:
        :param dir2:
        :param method:compare method: it could be shadow || sha256 || md5
        :param exclude_pattern: files that do not want to excluded, like .DS_Store in mac system
        :return: list with diff files
        """

        result = []

        # compare files that only exsited in dir2 but not existed in dir1
        dir2_file_list = FileHelper.find_files(dir2, '*', exclude_pattern)
        for dir2_file in dir2_file_list:
            dir1_files = FileHelper.find_file(dir1, os.path.basename(dir2_file))
            if not dir1_files:
                result.append(dir2_file)

        # walk files in dir 1. if existed in dir2, compare file
        # if not existed in dir2, add to result
        if exclude_pattern:
            exclude = re.compile(exclude_pattern)
        else:
            exclude = None

        for root, dirs, files in os.walk(dir1):
            left_files = [os.path.join(root, x) for x in files]

            for left_file in left_files:

                if exclude and re.findall(exclude, left_file):
                    continue
                right_files = FileHelper.find_file(dir2, os.path.basename(left_file))
                right_file = None
                if right_files:
                    right_file = right_files[0]
                else:
                    result.append(left_file)
                    continue
                if method.lower() == 'shadow':
                    if not filecmp.cmp(left_file, right_file):
                        result.append(left_file)
                else:
                    FileHelper.is_file_same(left_file, right_file, method)

        return result

    @staticmethod
    def get_file_count_in_dir(dir):
        count = 0
        for n in os.walk(dir):
            count += 1
        return count

        #####end of class


if __name__ =='__main__':
    print FileHelper.find_file("/linux/backup/lin-484","lin_1.txt" )
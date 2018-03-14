import unittest
import os

from lib.filehelper import FileHelper

class TestFileHelper(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.testdatadir = os.path.abspath('{}{}'.format(os.path.dirname(__file__), "/../../testdata"))
        cls.fh = FileHelper()
        cls.fh.create_directory(cls.testdatadir)

    def testCreateDir(self):
        testdir = "%s/subdir1/subdir2" %TestFileHelper.testdatadir
        FileHelper.create_directory(testdir)
        self.assertTrue(testdir)

    def test_create_file(self):
        """
        test: create test file
        """
        testfile = "%s%s%s" %(TestFileHelper.testdatadir, os.path.sep,  "testfilename")
        size = 2000
        FileHelper.create_file(testfile, size=size )
        result = FileHelper.file_exist(testfile)
        self.assertTrue(result)
        stat = FileHelper.get_file_stat(testfile)
        self.assertEqual(stat.st_size,size)

    def test_overwrite_file_content(self):
        testfile = "%s%s%s" % (TestFileHelper.testdatadir, os.path.sep, "testfilename")
        size = 2000
        FileHelper.create_file(testfile, overwrite=True, size=size, content="aaa")
        sha1 = FileHelper.sha256(testfile)
        FileHelper.overwrite_file_content(testfile,10,100,"@@@")
        sha2 = FileHelper.sha256(testfile)
        self.assertNotEqual(sha1, sha2)

    def test_insert_file_content(self):
        testfile = "%s%s%s" % (TestFileHelper.testdatadir, os.path.sep, "test_insert.dat")
        size = 2000
        size_insert = 50
        FileHelper.create_file(testfile, overwrite=True, size=size, content="aaa")
        FileHelper.insert_file_content(testfile, size/2, size_insert)
        new_size = FileHelper.get_file_size(testfile)
        self.assertEqual(new_size, size+size_insert)

    def test_append_file_content(self):
        testfile = "%s%s%s" % (TestFileHelper.testdatadir, os.path.sep, "test_append.dat")
        size = 2000
        size_append = 50
        FileHelper.create_file(testfile, overwrite=True, size=size, content="aaa")
        FileHelper.append_file_content(testfile, size_append)
        new_size = FileHelper.get_file_size(testfile)
        self.assertEqual(new_size, size + size_append)

    def test_truncate_file(self):
        testfile = "%s%s%s" % (TestFileHelper.testdatadir, os.path.sep, "test_truncate.dat")
        size = 2000
        size_truncate = 50
        FileHelper.create_file(testfile, overwrite=True, size=size, content="aaa")
        FileHelper.truncate_file(testfile, size_truncate)
        new_size = FileHelper.get_file_size(testfile)
        self.assertEqual(new_size, size_truncate)

    def test_overwrite_file_content(self):
        testfile = "%s%s%s" % (TestFileHelper.testdatadir, os.path.sep, "test_overwrite.dat")
        size = 2000
        size_overwrite = 50
        FileHelper.create_file(testfile, overwrite=True, size=size, content="aaa")
        sha1 = FileHelper.sha256(testfile)
        FileHelper.overwrite_file_content(testfile, size/2, size_overwrite, "%%%%")
        sha2 = FileHelper.sha256(testfile)
        new_size = FileHelper.get_file_size(testfile)
        self.assertEqual(new_size, size)
        self.assertNotEqual(sha1, sha2)


    @classmethod
    def tearDownClass(cls):
        FileHelper.delete_directory(TestFileHelper.testdatadir)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestFileHelper("testOverwriteFile"))
    runner = unittest.TextTestRunner()
    runner.run(suite)




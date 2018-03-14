
import sqlite3
from lib.filehelper import FileHelper
from lib.loghelper import LogHelper

class SqliteHelper(object):

    def __init__(self, database=None):
        try:
            self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()
        except sqlite3.Error, e:
            print "ERROR: Could not connect to server: %s" % e


    def query(self, statement):
        if self.connection:
            self.cursor.execute(statement)

    def execute(self, statement):
        if self.connection:
            self.connection.execute(statement)
            self.connection.commit()

    def find(self, statement):
        """
        Find the first line matches the criteria.
        :param statement:
        :return:
        """
        self.query(statement)
        return self.cursor.fetchone()


    def retrieve(self, statement, size=None):
        """
        Find all lines match the criteria, or limited lines according to size.
        :param statement:
        :param size: How many lines to find
        :return:
        """
        self.query(statement)
        if size == None:
            rows = self.cursor.fetchall()
        else:
            rows = self.cursor.fetchmany(size)

        # for row in rows:
        #     print row

        return rows


    def close(self):
        if self.connection:
            self.connection.close()

    @staticmethod
    def find_machine_id(manifest):
        state = 'select * from user where key = "_containerId"'
        db = SqliteHelper(manifest)
        result = db.find(state)
        return result[1]

    @staticmethod
    def search_history_result(path):
        data_path = path + "state.dat"
        print data_path
        if FileHelper.file_exist(data_path):
            db = SqliteHelper(data_path)
            statement = "select result from history where start_date in (select max(start_date) from history)"
            # print statement
            result = db.find(statement)
            print type(result)
            print result
            return result
        else:
            LogHelper.error("ERROR:Could not find result to search. Terminating")
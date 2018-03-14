#!/usr/bin/env python
#
# Copyright (c) Maginatics, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from pymongo import MongoClient


class MongoHelper(object):

    def __init__(self, host="127.0.0.1", port=27017, database=None):
        try:

            self.connection = MongoClient(host, port)
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to server: %s" % e

        self.db = getattr(self.connection, database)

    # @property
    # def db(self):
    #     return self.db

    # @db.setter
    # def db(self, db_name):
    #     self.db = getattr(self.connection, db_name)
    #     return self.db



    def is_collection_existed(self, cltname):
        """
        description: test if a collection existed
        :param name: clt_name
        :return: True || False
        """
        result = False
        clt_names = self.db.collection_names()
        if cltname in clt_names:
            result = True
        return result


    def create_collection(self, name):
        """
        :param name: collection_name
        :return:
        """

        if not self.is_collection_existed(name):
            self.db.create_collection(name)

    def drop_collection(self, name):
        if self.is_collection_existed(name):
            self.db.drop_collection(name)

    def insert_document(self, collection, document):
        return self.__get_clt(collection).insert_one(document)

    def insert_many(self, collection, documents):
        return self.__get_clt(collection).insert_many(documents)

    def delete_document(self, collection, document):
        result = self.__get_clt(collection).delete_one(document)
        return result.deleted_count


    """
    Get Collection
    """
    def __get_clt(self,collection):
        return getattr(self.db, collection)



    def create_documents(self,documents):
        pass

    def query_document(self,documents):
        pass

    def __del__(self):
        if self.connection is not None:
                self.connection.close()


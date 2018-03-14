#!/usr/bin/env python
#
# Copyright (c) Maginatics, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from time import strftime,gmtime
import json


from lib.mongohelper import MongoHelper
from lib.loghelper import LogHelper
from lib.elasticsearchhelper import ElasticsearchHelper
from configuration.global_config_loader import GLOBAL_CONFIG


class TestRun(object):
    def __init__(self, id=None, start_time=None, end_time=None,
                 qa_env=None, build=None, client=None, oem=None,
                 branch=None, runby=None):
        self._id = id
        self._name = id
        self._start_time = start_time or strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
        self._end_time = end_time or None
        self._env = qa_env or ""
        self._build = build or ""
        self._client = client or ""
        self._oem = oem or ""
        self._branch = branch or ""
        self._run_by = runby or ""

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        self._end_time = value

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, value):
        self._env = value.upper()

    @property
    def build(self):
        return self._build

    @build.setter
    def build(self, value):
        self._build = value.upper()

    @property
    def client(self):
        return self._client.upper()

    @client.setter
    def client(self, value):
        self._client = value.upper()

    @property
    def oem(self):
        return self._oem.upper()

    @oem.setter
    def oem(self, value):
        self._oem = value.upper()

    @property
    def branch(self):
        return self._branch

    @branch.setter
    def branch(self, value):
        self._branch = value.upper()

    @property
    def run_by(self):
        return self._run_by

    @run_by.setter
    def run_by(self, value):
        self._run_by = value.upper()

    def write_to_db(self):
        db_config = GLOBAL_CONFIG['mongo_db']
        client = MongoHelper(db_config.get('url'), db_config.get('port'), db_config.get('db_name'))

        if not client.is_collection_existed(db_config.get('testrun_collection')):
            client.create_collection("testrun_collection")
        result = client.insert_document(db_config.get('testrun_collection'), self.__create_bd_document())

        return result

    def __create_bd_document(self):
        document = {
            '_id': self.id,
            'run_by': self.run_by,
            'qa_environment': self.env,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'build': self.build,
            'client': self.client,
            'oem': self.oem,
            'branch': self.branch
        }
        return document

    def to_json(self):
        tr = {
           # '_id': self.id,
            'run_by': self.run_by,
            'qa_environment': self.env,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'build': self.build,
            'client': self.client,
            'oem': self.oem,
            'branch': self.branch
        }

        return json.dumps(tr)


    def save_to_elasticsearch(self, sendes=True):
        if sendes:
            url = GLOBAL_CONFIG['ELASTICSEARCH'].get('URL') or "http://localhost"
            port = GLOBAL_CONFIG['ELASTICSEARCH'].get('PORT') or "8080"
            es = ElasticsearchHelper(url, port)
            result = es.index(index="testrun", doc_type="testrun", body=self.__create_es_body(), _id=self.id)
            if result:
                message = result.get('result')
                print message
                # if message.strip().lstrip() not in ("created", 'updated'):
                #     LogHelper.error("create testresult message is %s" %message)
                # else:
                #     LogHelper.warn("create test result is %s" %message)
                return result
            else:
                LogHelper.error("Fail to send TestRun info to ES.")
                return
        else:
            print "Don't send testrun to ES."
            return

    def __create_es_body(self):
        # body = {
        #     "doc": {
        #         # '_id': self.id,
        #         'run_by': self.run_by,
        #         'qa_environment': self.env,
        #         'start_time': self.start_time,
        #         'end_time': self.end_time,
        #         'build': self.build,
        #         'client': self.client,
        #         'branch': self.branch
        #     }
        # }

        body = {
                'name': self.name,
                'run_by': self.run_by,
                'qa_environment': self.env,
                'start_time': self.start_time,
                'end_time': self.end_time,
                'build': self.build,
                'client': self.client,
                'oem': self.oem,
                'branch': self.branch

        }

        return body

    #
    # def write_to_logstash(self):
    #     host = "10.5.96.211" #TODO: add to config
    #     port = 5043
    #
    #     try:
    #         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #
    #     except socket.error, msg:
    #         sys.stderr.write("[ERROR] %s\n" % msg[1])
    #         sys.exit(1)
    #
    #
    #     try:
    #         sock.connect((host, port))
    #     except socket.error, msg:
    #         sys.stderr.write("[ERROR] %s\n" % msg[1])
    #         sys.exit(2)f
    #
    #     #msg = self.to_json()
    #     msg = {'@message': 'python test message', '@tags': ['python', 'test']}
    #
    #     print sock.send(json.dumps(msg))
    #
    #     sock.close()
    #     sys.exit(0)







from time import strftime, gmtime

from lib.platformhelper import PlatformHelper
from lib.loghelper import LogHelper
from configuration.global_config_loader import GLOBAL_CONFIG

#from lib.mongohelper import MongoHelper
from lib.elasticsearchhelper import ElasticsearchHelper



class TestCase(object):
    valid_test_result = ("PASS", "FAIL")

    def __init__(self,
                 testrun=None, start_time=None, duration=None,
                 tags=None, feature=None, summary=None,
                 ip=None, hostname=None, logfile=None, product=None, _id=None, build=None, error=None, end_time=None, thost=None):
        self.testrun = testrun
        self.start_time = start_time or strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
        self.duration = duration or 0
        self.tags = tags or []
        self.summary = summary
        self.feature = feature
        self.logfile = logfile
        self.machine_ip = ip or PlatformHelper.get_ip_address()
        self.machine_hostname = hostname or PlatformHelper.get_hostname()
        self.product = product
        self.test_result = "unknown"
        self.id = _id
        self.name = self.id
        self.build = build or "-999"
        self.error = error
        self.thost = thost
        self.end_time = end_time


    def write_to_db(self):
        db_config = GLOBAL_CONFIG['MONGO_DB']
        client = MongoHelper(db_config.get('url'), db_config.get('port'), db_config.get('db_name'))

        if not client.is_collection_existed(db_config.get('testcase_collection')):
            client.create_collection("testcase_collection")
        result = client.insert_document(db_config.get('testcase_collection'), self.__create_bd_document())

        return result

    def write_to_elasticsearch(self, sendes=True):
        if sendes:
            url = GLOBAL_CONFIG['ELASTICSEARCH'].get('URL') or "http://localhost"
            port = GLOBAL_CONFIG['ELASTICSEARCH'].get('PORT') or "8080"
            es = ElasticsearchHelper(url, port)

            #LogHelper.debug("Start to Write testresult to ES")
            result = es.index(index='testcase', doc_type='testcase', body=self.__create_es_body(), _id=self.id)
            if result:
                message = result.get('result')
                print message
                # if message.strip().lstrip() not in ("created", 'updated'):
                #     LogHelper.error("create testresult message is %s" %message)
                # else:
                #     LogHelper.warn("create test result is %s" %message)
                return result
            else:
                LogHelper.error("Fail to send TestCase info to ES.")
                return
        else:
            print "Don't send testcase to ES."
            return

    def __create_es_body(self):
        body = {
                'id': self.id,
                'testrun': self.testrun,
                'duration': self.duration,
                'start_time': self.start_time,
                'end_time': self.end_time,
                'tags': self.tags,
                'summary': self.summary,
                'feature': self.feature,
                'log': self.logfile,
                'machine': {
                    "ip": self.machine_ip,
                    "hostname": self.machine_hostname
                },
                'product': self.product,
                'test_result': self.test_result,
                'name': self.name,
                'build': self.build,
                'thost': self.thost,
                'error': self.error
            }

        return body

    def __create_bd_document(self):
        document = {
            'testrun': self.testrun,
            'duration': self.duration,
            'start_time': self.start_time,
            'tags': self.tags,
            'summary': self.summary,
            'feature': self.feature,
            'log': self.logfile,
            'machine': {
                "ip": self.machine_ip,
                "hostname": self.machine_hostname
            },
            'product': self.product,
            'test_result': self.test_result,
            'id': self.id
        }
        return document


if __name__ == "__main__":
    tc = TestCase(testrun="TESTCASE_DEMO")
    import datetime
    tc.start_time = datetime.datetime.strptime("30Sep2017 14:34:18", '%d%b%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')
    # tc.end_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    result = tc.write_to_elasticsearch()
    #
    # result

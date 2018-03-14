import datetime
from time import strftime, gmtime

from lib.platformhelper import PlatformHelper
from lib.loghelper import LogHelper
from lib.clienterrorhelper import ClientErrorHelper
from configuration.global_config_loader import GLOBAL_CONFIG

from lib.elasticsearchhelper import ElasticsearchHelper



class KPI(object):
    def __init__(self, _id=None, testcase=None, category=None, name=None, apimethod=None, result=None, start_time=None,
                 end_time=None, apicode=None, exterrorcode=None, message=None, throughput=None, duration=None,
                 thost=None, ip=None, hostname=None, env=None, client=None):
        self.testcase = testcase or "Unknown"
        self.env = env or "PROD"
        self.client = client
        self.category = category
        self.name = name
        self.apimethod = apimethod
        self.apicode = apicode
        self.exterrorcode= exterrorcode
        self.result = result
        self.message = message

        self.start_time = start_time or strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
        self.end_time = end_time or strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())

        self.machine_hostname = hostname or PlatformHelper.get_hostname()
        self.machine_ip = ip or PlatformHelper.get_ip_address()

        self.throughput = throughput
        self.duration = duration
        self.thost = thost
        self.id = _id


    def write_to_elasticsearch(self, sendes=True):
        if sendes:
            url = GLOBAL_CONFIG['ELASTICSEARCH'].get('URL') or "http://localhost"
            port = GLOBAL_CONFIG['ELASTICSEARCH'].get('PORT') or "8080"
            es = ElasticsearchHelper(url, port)
            #LogHelper.debug("Start to Write testresult to ES")
            result = es.index(index='kpi', doc_type='kpi', body=self.__create_es_body(), _id=self.id)
            if result:
                message = result.get('result')
                print message
                # if message.strip().lstrip() not in ("created", 'updated'):
                #     LogHelper.error("create testresult message is %s" %message)
                # else:
                #     LogHelper.warn("create test result is %s" %message)
                return result
            else:
                LogHelper.error("Fail to send KPI info to ES.")
                return

        else:
            print "Don't Send KPI to ES..."
            return self.read()

    def read(self):
        self.__create_es_body()

    def __create_es_body(self):
        body = {
            'id': self.id,
            'testcase': self.testcase,
            'env': self.env,  # PROD, PANTHEON, STAGING, QA12
            'client': self.client,
            'category': self.category,  # service, client
            'name': self.name, # API name, client behavior.  /namedObject/<id>,   activate, backup, restore
            'apimethod': self.apimethod,  # HEAD/GET/PUT/UPDATE/DELETE
            'apicode': self.apicode,
            'exterrorcode': self.exterrorcode,
            'result': self.result,  # API response code, client result
            'start_time': self.start_time,
            'end_time': self.end_time,
            "ip": self.machine_ip,
            "hostname": self.machine_hostname,
            'message': self.message,
            'throughput': self.throughput,
            'thost': self.thost,
            'duration': self.duration
        }
        print body

        return body

    def set_name(self, kpiname):
        if kpiname.upper() in ("START", "BACKUP"):
            self.name = "BACKUP"

    def set_apicode(self, apikpi):
        if len(apikpi[0].split()) > 1:
            self.end_time = datetime.datetime.strptime(apikpi[0], '%d%b%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')
            self.duration = (
            datetime.datetime.strptime(self.end_time, "%Y-%m-%dT%H:%M:%SZ") - datetime.datetime.strptime(
                self.start_time, "%Y-%m-%dT%H:%M:%SZ")).total_seconds()
        else:
            self.end_time = apikpi[0]
            self.duration = (
            datetime.datetime.strptime(self.end_time, "%Y-%m-%dT%H:%M:%S.%f") - datetime.datetime.strptime(
                self.start_time, "%Y-%m-%dT%H:%M:%S.%f")).total_seconds()

        self.apicode = apikpi[3]
        self.result = apikpi[4]

    def set_backupstatus(self, statuskpi):
        if len(statuskpi[0].split()) > 1:
            self.end_time = datetime.datetime.strptime(statuskpi[0], '%d%b%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            self.end_time = statuskpi[0]

        if ClientErrorHelper.get_error(statuskpi[4]):
            self.result = "Fail"
            self.message = ClientErrorHelper.get_error(statuskpi[4])

    def set_restorestatus(self, statuskpi):
        if len(statuskpi[0].split()) > 1:
            self.end_time = datetime.datetime.strptime(statuskpi[0], '%d%b%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            self.end_time = statuskpi[0]

        if ClientErrorHelper.get_error(statuskpi[3]):
            self.result = "Fail"
            self.message = ClientErrorHelper.get_error(statuskpi[3])



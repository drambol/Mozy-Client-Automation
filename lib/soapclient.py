import suds
from requests import Session
from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import
from suds_requests import RequestsTransport
from suds.sudsobject import asdict

from datetime import datetime
import traceback

from lib.loghelper import LogHelper
from lib.kpi import KPI


class SoapClient(object):

    def __init__(self, wsdl_host, wsdl_api, ssl=False, cert=None, **params):
        imp = Import('http://schemas.xmlsoap.org/soap/encoding/')
        doctor = ImportDoctor(imp)
        session = Session()
        session.verify = cert or ssl
        self._wsdl_api = wsdl_api
        wsdl = "%s%s" % (wsdl_host, wsdl_api)
        self._client = Client(
            wsdl, doctor=doctor, transport=RequestsTransport(session))
        self._params = params

    @property
    def client(self):
        return self._client

    @property
    def wsdl_api(self):
        return self._wsdl_api

    @property
    def params(self):
        return self._params

    def recursive_dict(self, response):
        out = {}
        for k, v in asdict(response).iteritems():
            if hasattr(v, '__keylist__'):
                out[k] = self.recursive_dict(v)
            elif isinstance(v, list):
                out[k] = []
                for item in v:
                    if hasattr(item, '__keylist__'):
                        out[k].append(self.recursive_dict(item))
                    else:
                        out[k].append(item)
            elif isinstance(v, suds.sax.text.Text):
                out[k] = str(v)
            else:
                out[k] = v
        return out

    def call(self, method, request_body):
        try:
            LogHelper.info("SOAP Request: %s %s\nBody: %s" % (
                method, self.wsdl_api, str(request_body)))
            kpi = KPI(
                testcase=self.params['testcase'],
                category=self.params['category'] or 'Service',
                apimethod=method,
                start_time=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                name=self.wsdl_api)
            response = self.client.service.__getattr__(method)(**request_body)
            kpi.result = 'SUCCESS'
            kpi.apicode = '200'
        except Exception, e:
            kpi.result = "FAIL"
            kpi.message = str(e)
            LogHelper.error("SOAP Response: %s %s - Fail\nBody: %s" % (
                method, self.wsdl_api, e))
            raise Exception(traceback.format_exc())
        finally:
            try:
                kpi.end_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                kpi.write_to_elasticsearch()
            except Exception, e:
                LogHelper.error("Write KPI: %s %s - Fail\nReason: %s" % (
                    method, self.wsdl_api, e))

        if type(response) == list:
            parsed_response = []
            for item in response:
                try:
                    parsed_response.append(self.recursive_dict(item))
                except TypeError:
                    parsed_response.append(item)
        else:
            try:
                parsed_response = self.recursive_dict(response)
            except TypeError:
                parsed_response = response

        LogHelper.info("SOAP Response: %s %s - Success\nBody: %s" % (
            method, self.wsdl_api, parsed_response))

        return parsed_response

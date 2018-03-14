from soapclient import SoapClient


class OdinHelper(object):

    def __init__(self, wsdl_host, wsdl_api, **params):
        params['category'] = 'odin'
        if wsdl_host.startswith('https') and 'api.mozypro.com' in wsdl_host:
            self._soap_client = SoapClient(
                wsdl_host, wsdl_api, True, None, **params)
        else:
            self._soap_client = SoapClient(
                wsdl_host, wsdl_api, False, None, **params)

    @property
    def soap_client(self):
        return self._soap_client

    def create(self, request_body):
        response = self.soap_client.call('Create', request_body)
        return response

    def get(self, request_body):
        response = self.soap_client.call('Get', request_body)
        return response

    def update(self, request_body):
        response = self.soap_client.call('Update', request_body)
        return response

    def delete(self, request_body):
        response = self.soap_client.call('Delete', request_body)
        return response

    def deliver(self, request_body):
        response = self.soap_client.call('Deliver', request_body)
        return response

    def release(self, request_body):
        response = self.soap_client.call('Release', request_body)
        return response

    def transfer(self, request_body):
        response = self.soap_client.call('Transfer', request_body)
        return response

    def provision(self, request_body):
        response = self.soap_client.call('Provision', request_body)
        return response

    def getLicenses(self, request_body):
        response = self.soap_client.call('GetLicenses', request_body)
        return response

    def getResources(self, request_body):
        response = self.soap_client.call('GetResources', request_body)
        return response

    def updateLicenses(self, request_body):
        response = self.soap_client.call('UpdateLicenses', request_body)
        return response

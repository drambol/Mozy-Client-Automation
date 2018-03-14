import requests
import json
from singleton import Singleton

# from configuration.global_config_loader import GLOBAL_CONFIG

class RestfulHelper(object):
    """
        class that hold method to handle file system
        like create files
        """
    __metaclass__ = Singleton

    @staticmethod
    def send_get(url,request_header):
        response = requests.get(url,headers = request_header)
        return response

    @staticmethod
    def send_post(url,request_header,request_body):
        response = requests.post(url,data=json.dumps(request_body),headers = request_header)
        return response

    @staticmethod
    def send_delete(url,request_header):
        response = requests.delete(url,headers = request_header)
        return response

    @staticmethod
    def send_put(url,request_header,request_body):
        response = requests.put(url,data=json.dumps(request_body),headers = request_header)
        return response


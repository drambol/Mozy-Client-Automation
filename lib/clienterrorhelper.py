
from lib import singleton
from error_codes import Error_Codes

class ClientErrorHelper(object):

    __metaclass__ = singleton.Singleton

    @staticmethod
    def keys():
        return Error_Codes.ERROR_CODE.keys()

    @staticmethod
    def has_key(key):
        # Error_Codes.ERROR_CODE.has_key("0xfffffff7")
        return Error_Codes.ERROR_CODE.has_key(key)

    @staticmethod
    def get_error(key):
        if key == "0x00000000":
            return None
        elif ClientErrorHelper.has_key(key):
            return Error_Codes.ERROR_CODE.get(key)

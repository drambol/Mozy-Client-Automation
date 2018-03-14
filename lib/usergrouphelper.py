import types
import inspect
import json


class UserGroupHelper(object):

    @classmethod
    def __init__(self, billing_address =None, billing_city = None, billing_state =None, billing_country =None,billing_zip =None,external_id=None,language =None,name = None,password=None,status = None,username=None,user_group_id =None,email_verified_at=None,type = None,install_region=None,sync=None):
        self.billing_address = ('%s' % (billing_address))
        self.billing_city = ('%s' % (billing_city))
        self.billing_state = ('%s' % (billing_state))
        self.billing_country = ('%s' % (billing_country))
        self.billing_zip = ('%s' % (billing_zip))
        self.external_id = ('%s' % (external_id))
        self.language = ('%s' % (language))
        self.name = ('%s' % (name))
        self.password = ('%s' % (password))
        self.status = ('%s' % (status))
        self.username = ('%s' % (username))
        self.user_group_id = user_group_id
        self.email_verified_at = ('%s' % (email_verified_at))
        self.type = ('%s' % (type))
        self.sync = sync
        self.install_region = ('%s' % (install_region))
        self.id = None
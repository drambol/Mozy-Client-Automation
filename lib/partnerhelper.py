import types
import inspect
import json

from bifrosthelper import AuthExchange
from bifrosthelper import BifrostHelper

AUTH_EXCHANGE_URL = "/auth/exchange"
HTTP_PROTOCOL = "http://"
BIFROST_HOST = "bifrost01.qa12h.mozyops.com"  # GLOBAL_CONFIG['QA_ENVIRONMENT']['QA8']['bifrost.host']
API_KEY = 'RekgE8bUB6APRrQrAKxEcbyZJebsFq0HagMNW320bDsYe8QLgOegJbfOnSDy8dVJ'
CONTENT_TYPE = "application/json"
ACCEPT = "application/vnd.mozy.bifrost+json;v=1"
DELL_MOZYPRO_ROOT_ROLE_ID=15195
DELL_MOZYPRO_ROOT_PARTNER_ID=416944

class PartnerHelper(object):

    @classmethod
    def __init__(self, name = "",root_role_id=None,admin = None, parent_partner_id =None,pro_plan_id = None, billing_address =None, billing_city = None, billing_state =None, billing_country =None,billing_zip =None,company_type =None,external_id=None,subdomain =None,phone = None,add_ons=None,sync = None,sync_default_quota=None,account_type =None,security_requirement=None,install_region = None):
        self.billing_address = billing_address
        self.billing_city = billing_city
        self.billing_state = billing_state
        self.billing_country = billing_country
        self.billing_zip = billing_zip
        self.company_type = company_type
        self.external_id = external_id
        self.name = name
        self.pro_plan_id = pro_plan_id
        self.root_role_id = root_role_id
        self.subdomain = subdomain
        self.phone = phone
        self.add_ons = add_ons
        self.sync = sync
        self.sync_default_quota = sync_default_quota
        self.account_type = account_type
        self.parent_partner_id = parent_partner_id
        self.admin = admin
        self.security_requirement = security_requirement
        self.install_region = install_region
        self.id = None
        self.api_key = None

    @classmethod
    def set_username(self,username):
        if username != None:
            self.username = str(username)
        else:
            self.username = username

    @classmethod
    def set_api_key(self,api_key):
        if api_key != None:
            self.api_key = str(api_key)
        else:
            self.api_key = api_key


# authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL,BIFROST_HOST,AUTH_EXCHANGE_URL)), API_KEY)
# # authexchange = AuthExchange('http://bifrost01.qa8.mozyops.com/auth/exchange', API_KEY)
# token = (authexchange.get_auth_exchange())
# partner_body = {'admin': {'username': 'test_bifrost_helper_mozypro_clientqaautomation@bifrost.com','full_name': 'test bifrost helper partner'}, 'name': 'Provision Storage Bifrost Partner',"root_role_id" : 6648,"parent_partner_id" : 273490,}
# # partner_body = {'admin': {'username': 'test_bifrost_helper_mozypro_clientqaautomation@bifrost.com','full_name': 'test bifrost helper partner'}, 'name': 'Provision Storage Bifrost Partner',"root_role_id" : 6648,"parent_partner_id" : 273490,}
# #fedid_role
# bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL,BIFROST_HOST)), token)
# bifrosthelper.post_accounts_partners(partner_body)

if __name__ == '__main__':
    # admin = {}
    # admin['fullname'] = row['admin fullname'] or "test ELK"
    # admin['username'] = row['admin username'] or 'clientautomationforbifrost@test.com'
    admin = {"full_name": "test", "username": "test.test.round9@test.com"}
    partner = PartnerHelper(name = "test ELK partner",admin=admin)

    partner.root_role_id = DELL_MOZYPRO_ROOT_ROLE_ID
    partner.parent_partner_id = DELL_MOZYPRO_ROOT_PARTNER_ID
    authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, BIFROST_HOST, AUTH_EXCHANGE_URL)), API_KEY)
    token = (authexchange.get_auth_exchange())
    bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, BIFROST_HOST)), token)
    new_partner_response = bifrosthelper.post_accounts_partners({"name": partner.name, "admin": partner.admin, "root_role_id": partner.root_role_id, "parent_partner_id":partner.parent_partner_id })
    print(new_partner_response.status_code)
    if new_partner_response.status_code == 201:
        # partner.id = new_partner_response['items'][0]['data']['id']
        content = new_partner_response.text
        print(content)
        json_content = json.loads(content)
        print(json_content['items'][0]['data']['id'])

        # print(new_partner_response.json())
        # content = new_partner_response.text
        # print(types(new_partner_response.text))
        # response_hash = json.dumps(new_partner_response.json())
        # print(types(response_hash))
        # print(types(response_hash['items']))
        # partner.id = new_partner_response['items'][0]['data']['id']
        print(partner.id)

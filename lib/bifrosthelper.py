#!/usr/bin/env python
#
# Copyright (c) Maginatics, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Jessica Zhang

import types
import json
import time
from urllib import quote
from urllib import urlencode

# from lib.platformhelper import PlatformHelper
# from lib.cmdhelper import CmdHelper
# from lib.loghelper import LogHelper
# from lib.filehelper import FileHelper
from singleton import Singleton
from restfulhelper import RestfulHelper
from userhelper import UserHelper
from usergrouphelper import UserGroupHelper

AUTH_EXCHANGE_URL = "/auth/exchange"
HTTP_PROTOCOL = "http://"
BIFROST_HOST = "bifrost01.qa12h.mozyops.com"

Gigabyte = 1024*1024*1024

class AuthExchange(object):

    @classmethod
    def __init__(self, url="%s%s%s" % (HTTP_PROTOCOL,BIFROST_HOST,AUTH_EXCHANGE_URL), Api_Key=None, x_mozy_partner=None, x_mozy_user=None):
        self.api_key = Api_Key
        self.x_mozy_partner = x_mozy_partner
        self.x_mozy_user = x_mozy_user
        self.timestamp = None
        self.url = url

    @classmethod
    def get_auth_exchange(self):
        get_url = ""
        headers = {'Api-Key': self.api_key,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        if self.x_mozy_partner != None:
            headers['X-MozyPartner'] = "%s" % self.x_mozy_partner
        if self.x_mozy_user != None:
            headers['X-MozyUser'] = self.x_mozy_user
        response = RestfulHelper.send_get(self.url,headers)
        hash = eval(response.text)
        print response.text
        print ('%s %s' % (hash['token_type'],hash['token']))
        return ('%s %s' % (hash['token_type'],hash['token']))

class BifrostHelper(object):
    __metaclass__ = Singleton

    @classmethod
    def __init__(self, base_url= "%s%s" % (HTTP_PROTOCOL,BIFROST_HOST),token=None):
        self.base_url = base_url
        self.token = token

    def cal_byte(unit, value):
        if unit == "B":
            return value
        elif unit == "GB":
            return value * Gigabyte
        elif unit == "TB":
            return value * Gigabyte * 1024

    # Mozy-Dell Integration Related APIs
    @classmethod
    def post_accounts_partners(self,body):
        url = "/accounts/partners"
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url,url))
        print(request_url)
        response = RestfulHelper.send_post(request_url,headers,body)
        print(response.text)

        return response

    @classmethod
    def put_accounts_partner_storage(self,id="",storage_type="Desktop",body={}):
        url = ('/accounts/partner/%s/storage/%s' % (id,storage_type))
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url, url))
        print(request_url)
        response = RestfulHelper.send_put(request_url, headers, body)
        print(response.text)

        return response

    @classmethod
    def put_accounts_partner_id(self,id="",body={}):
        url = ('/accounts/partner/%s' % (id))
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url, url))
        print(request_url)
        response = RestfulHelper.send_put(request_url, headers, body)
        print(response.text)

        return response

    @classmethod
    def delete_accounts_partner_id(self, id=""):
        url = ('/accounts/partner/%s' % (id))
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url, url))
        print(request_url)
        response = RestfulHelper.send_delete(request_url, headers)
        print(response.text)

        return response

    @classmethod
    def get_accounts_partner_id(self, id="", extend_with=None):
        url = ('/accounts/partner/%s' % (id))
        if extend_with != None:
            url = ('/accounts/partner/%s?extend_with=%s' % (id,extend_with))
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url, url))
        response = RestfulHelper.send_get(request_url, headers)

        return response

    @classmethod
    def post_accounts_users(self,body={}):
        url = "/accounts/users"
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url, url))
        print(request_url)
        response = RestfulHelper.send_post(request_url, headers, body)
        print(response.text)

        return response

    @classmethod
    def get_accounts_users(self,parameters={},offset=None,limit=None,order=None,include_sub_partners=None):
        url = "/accounts/users"
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        query_string = ""
        # Add code here whether parameters is a empty dictionary
        for key,value in parameters.items():
            value = quote(str(value))
            query_string += "%s:\"%s\"" % (key,value)
        request_url = ('%s%s' % (self.base_url, url))
        query_string = str(query_string)
        if query_string != "":
            request_url = ('%s%s?q=%s' % (self.base_url, url, query_string))
        else:
            request_url = ('%s%s' % (self.base_url, url))
        print(request_url)
        if offset != None:
            request_url += "&offset=%s" % (offset)
        if limit != None:
            request_url += "&limit=%s" % (limit)
        if order != None:
            request_url += "&order=%s" % (order)
        if include_sub_partners != None and include_sub_partners == True:
            request_url += "&scope=include_sub_partners"
        response = RestfulHelper.send_get(request_url, headers)
        print(response.text)

        return response

    @classmethod
    def post_accounts_containers(self,body={}):
        url = "/accounts/containers"
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url, url))
        print(request_url)
        response = RestfulHelper.send_post(request_url, headers, body)
        print(response.text)

        return response

    @classmethod
    def post_accounts_user_groups(self,body={}):
        url = "/accounts/user_groups"
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url, url))
        print(request_url)
        response = RestfulHelper.send_post(request_url, headers, body)
        print(response.text)

        return response

    @classmethod
    def get_accounts_user_groups(self):
        url = "/accounts/user_groups"
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url, url))
        response = RestfulHelper.send_get(request_url, headers)

        return response
    @classmethod
    def delete_accounts_user_group(self,user_group_id):
        url = "/accounts/user_groups/%s" % (user_group_id)
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url, url))
        response = RestfulHelper.send_delete(request_url, headers)

        return response

    @classmethod
    def delete_accounts_user_id(self,id):
        url = "/accounts/user/%s" % (id)
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url, url))
        print(request_url)
        response = RestfulHelper.send_delete(request_url, headers)
        print(response.text)

        return response

    @classmethod
    def post_accounts_licenses(self, body={}):
        url = "/accounts/licenses"
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url, url))
        print(request_url)
        response = RestfulHelper.send_post(request_url, headers, body)
        print(response.text)

        return response

    @classmethod
    def put_accounts_licenses(self,parameters={},body={}):
        url = "/accounts/licenses"
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        query_string = ""
        if parameters is not None:
            query_string = urlencode(parameters)
        if query_string != "":
            request_url = ('%s%s?%s' % (self.base_url, url, query_string))
        else:
            request_url = ('%s%s' % (self.base_url, url))
        response = RestfulHelper.send_put(request_url, headers, body)
        print(response.text)

        return response

    @classmethod
    def get_accounts_licenses(self,parameters={}):
        url = "/accounts/licenses"
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        query_string = ""
        if parameters is not None:
            query_string = urlencode(parameters)
        if query_string != "":
            request_url = ('%s%s?%s' % (self.base_url, url, query_string))
        else:
            request_url = ('%s%s' % (self.base_url, url))

        print(request_url)
        response = RestfulHelper.send_get(request_url, headers)
        print(response.text)

        return response

    @classmethod
    def get_accounts_partners(self,parameters={}):
        url = "/accounts/partners"
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        query_string = ""
        # Add code here whether parameters is a empty dictionary
        for key,value in parameters.items():
            query_string += key + ':' + value
        request_url = ('%s%s' % (self.base_url, url))
        query_string = str(query_string)
        if query_string != "":
            query_string = quote(query_string)
            request_url = ('%s%s?q=%s' % (self.base_url, url, query_string))
        else:
            request_url = ('%s%s' % (self.base_url, url))
        print(request_url)
        response = RestfulHelper.send_get(request_url, headers)
        print(response.text)

        return response

    @classmethod
    def get_accounts_partner_id(self,id):
        url = "/accounts/partner/%s" % (id)
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url, url))
        response = RestfulHelper.send_get(request_url,headers)

        return response

    @classmethod
    def put_accounts_license_keystring(self,keystring,assigned_email_address):
        url = "/accounts/license/%s" % (keystring)
        headers = {'Authorization': self.token, 'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url  = ('%s%s' % (self.base_url, url))
        print(request_url)
        body = {"assigned_email_address": assigned_email_address}
        response = RestfulHelper.send_put(request_url,headers,body)
        return response

    @classmethod
    def put_accounts_user_storage(self,id="",storage_type="Desktop",body={}):
        url = ('/accounts/user/%s/storage/%s' % (id,storage_type))
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url, url))
        print(request_url)
        response = RestfulHelper.send_put(request_url, headers, body)
        print(response.text)

        return response

    @classmethod
    def put_accounts_user_id(self,id="",body={},extend_with=None):
        url = "/accounts/user/%s" % (id)
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        if extend_with != None:
            url += "?extend_with=%s" % (extend_with)
        request_url = ('%s%s' % (self.base_url, url))
        print(request_url)
        response = RestfulHelper.send_put(request_url, headers, body)
        print(response.text)
        return response

    @classmethod
    def get_accounts_partner_storage(self,id=""):
        url = ('/accounts/partner/%s/storage' % (id))
        headers = {'Authorization': self.token,
                   'Content-Type': "application/json", 'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url, url))
        print(request_url)
        response = RestfulHelper.send_get(request_url, headers)
        print(response.text)

        return response

    @classmethod
    def post_emails_deliver(self,body={}):
        url = "/emails/deliver"
        headers = {'Authorization': self.token, 'Content-Type': "application/json",
                   'Accept': "application/vnd.mozy.bifrost+json;v=1"}
        request_url = ('%s%s' % (self.base_url, url))
        response = RestfulHelper.send_post(request_url, headers, body)
        return response

    @classmethod
    def Create_New_UserGroup(self,group_name,partner_id):
        existing_user_group = self.Check_UserGroup_Exist(group_name)
        if existing_user_group != None:
            return existing_user_group
        else:
            post_user_group_response = self.post_accounts_user_groups({"name": group_name, "partner_id": partner_id})
            if post_user_group_response.status_code == 201:
                content = post_user_group_response.text
                json_content = json.loads(content)
                user_group = UserGroupHelper()
                user_group.name = json_content['items'][0]['data']['name']
                user_group.id = json_content['items'][0]['data']['id']
                return user_group
            else:
                assert "fail with creating a new user group %s" % (post_user_group_response.text)

    @classmethod
    def Check_UserGroup_Exist(self,group_name):
        get_user_groups_response = self.get_accounts_user_groups()
        if get_user_groups_response.status_code == 200:
            content = get_user_groups_response.text
            json_content = json.loads(content)
            for data_hash in json_content['items']:
                data_hash_group_name = str(data_hash['data']['name'])
                if data_hash_group_name == group_name:
                    user_group = UserGroupHelper()
                    user_group.name = data_hash_group_name
                    user_group.id = data_hash['data']['id']
                    return user_group
            return None

        else:
            assert "fail with getting user groups detail"

    @classmethod
    def Create_New_User(self,username,password,user_group_id=None,type=None,sync=None):
        post_body = {"username": username, "password": password}
        if user_group_id != None:
            post_body.update({"user_group_id":user_group_id})
        if type != None:
            post_body.update({"type":str(type)})
        if sync != None:
            post_body.update({"sync":bool(sync)})

        post_user_response = self.post_accounts_users(post_body)
        user = None
        if post_user_response.status_code == 201:
            content = post_user_response.text
            json_content = json.loads(content)
            user = UserHelper()
            user.set_username(username)
            user.set_password(password)
            user.id = json_content['items'][0]['data']['id']
            return user
        else:
            assert "fail with post a new user %s" % (post_user_response.text)

    @classmethod
    def Get_Default_UserGroup(self,partner_id):
        get_partner_response = self.get_accounts_partner_id(partner_id)
        if get_partner_response.status_code == 200:
            content = get_partner_response.text
            json_content = json.loads(content)
            default_user_group = UserGroupHelper()
            default_user_group.id = json_content['items'][0]['data']['default_user_group_id']
            return default_user_group
        else:
            assert "fail with getting default user_group %s" % (get_partner_response.text)

    @classmethod
    def Create_New_Licenses_And_Assign_to_User(self,username,license_type,licenses):
        post_license_response = self.post_accounts_licenses({"license_type": license_type, "licenses": licenses})
        if post_license_response.status_code == 201:
            content = post_license_response.text
            json_content = json.loads(content)
            licenses_array = json_content['items']
            key_strings = []
            for license_keys in licenses_array:
                key_strings.append(license_keys['data']['keystring'])

            for key in key_strings:
                transfer_license_response = self.put_accounts_license_keystring(key,username)
                if transfer_license_response.status_code == 200:
                    print("assign key %s to user %s successfully" % (key,username))
                else:
                    assert "fail with assigning key %s to user %s" % (key_strings, username)
            return key_strings

        else:
            assert "provision license failed with response %s" % (post_license_response.text)

    @classmethod
    def Set_Device_Limit_User(self,username,license_type,licenses):
        parameters = {"assigned_email_address":username,"license_type":license_type}
        current_license_response = self.get_accounts_licenses(parameters)
        assert(current_license_response.status_code == 200)
        content = current_license_response.text
        json_content = json.loads(content)
        current_user_licenses = json_content['total']
        if current_user_licenses > licenses:
            transfer_license_response = self.put_accounts_licenses(parameters.update({"limit":(current_user_licenses - licenses)}),{"assigned_email_address":""})
        else:
            self.post_accounts_licenses({"license_type":license_type, "licenses":(licenses - current_user_licenses)})
            transfer_license_response = self.put_accounts_licenses({"status":"free","limit":(licenses - current_user_licenses),"license_type":license_type},{"assigned_email_address":username})
        print(transfer_license_response.text)
        return transfer_license_response

    @classmethod
    def Create_New_Licenses(self,partner_id,license_type,licenses):
        post_license_response = self.post_accounts_licenses({"license_type": license_type, "licenses": licenses, 'partner_id':partner_id})
        assert(post_license_response.status_code == 201)
        content = post_license_response.text
        json_content = json.loads(content)
        licenses_array = json_content['items']
        key_strings = []
        for license_keys in licenses_array:
            key_strings.append(license_keys['data']['keystring'])
        return key_strings

    @classmethod
    def Delete_User_Group(self,user_group_id):
        delete_user_group_response = self.delete_accounts_user_group(user_group_id)
        if delete_user_group_response.status_code == 200:
            print "delete user group %s successfully" % user_group_id
        else:
            assert "fail with delete user group %s" % delete_user_group_response.text

    @classmethod
    def Suspend_Partner(self,id):
        put_account_partner_response = self.put_accounts_partner_id(id,{"status":"suspended"})
        assert(put_account_partner_response.status_code == 200)

    @classmethod
    def Resume_Partner(self,id):
        put_account_partner_response = self.put_accounts_partner_id(id, {"status": "active"})
        assert (put_account_partner_response.status_code == 200)

    @classmethod
    def Suspend_User(self, id):
        put_account_user_response = self.put_accounts_user_id(id, {"status": "suspended"})
        assert (put_account_user_response.status_code == 200)

    @classmethod
    def Resume_User(self, id):
        put_account_user_response = self.put_accounts_user_id(id, {"status": "active"})
        assert (put_account_user_response.status_code == 200)

    @classmethod
    def Delete_Partner(self,id):
        delete_account_partner_response = self.delete_accounts_partner_id(id)
        assert (delete_account_partner_response.status_code == 200)

    @classmethod
    def Send_Email_Partner(self,admin_id,template='admin_account_created',language='en',details=None):
        if details != None:
            post_email_deliver_response = self.post_emails_deliver({"admin_id": admin_id, "template":template,"language":language, "details":details})
        else:
            post_email_deliver_response = self.post_emails_deliver({"admin_id": admin_id, "template": template, "language": language})
        assert(post_email_deliver_response.status_code == 204)

    @classmethod
    def Send_Email_User(self,user_id,template='new_user_notification',language='en',details=None):
        if details != None:
            post_email_deliver_response = self.post_emails_deliver({"user_id": user_id, "template":template,"language":language, "details":details})
        else:
            post_email_deliver_response = self.post_emails_deliver({"user_id": user_id, "template": template, "language": language})
        assert(post_email_deliver_response.status_code == 204)

    @classmethod
    def Set_StorageLimit_User(self,user_id,storage_type="Desktop",unit="B",value="1", pool_setting="limited"):
        if pool_setting == "limited":
            put_accounts_user_storage_response = self.put_accounts_user_storage(user_id,storage_type,{"pool_setting": pool_setting,
                                                                                                      "pool_limit": {"value":value,"unit":unit }})
        elif pool_setting == "shared":
            put_accounts_user_storage_response = self.put_accounts_user_storage(user_id, storage_type, {"pool_setting": pool_setting})
        assert(put_accounts_user_storage_response.status_code == 200)

    @classmethod
    def Get_Partner_Storage(self,partner_id,storage_type="Desktop",quota="total"):
        get_partner_storage_response = self.get_accounts_partner_storage(partner_id)
        assert (get_partner_storage_response.status_code == 200)
        content = get_partner_storage_response.text
        json_content = json.loads(content)
        storage_array = json_content['items']
        byte = None
        for each_storage in storage_array:
            if each_storage['data']['pool_type'] == storage_type:
                if quota == "total":
                    return self.cal_byte(each_storage['data']['pool_limit']['unit'],each_storage['data']['pool_limit']['value'])
                elif quota == "used":
                    return self(each_storage['data']['used']['unit'],
                                    each_storage['data']['used']['value'])
                elif quota == "available":
                    return self(each_storage['data']['available']['unit'],
                                    each_storage['data']['available']['value'])
        return byte



        









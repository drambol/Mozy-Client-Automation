import os
import inspect
import time
import json
import ast

from behave import *

# from apps.app_lib.datahelper import DataHelper
# from configuration.config_adapter import ConfigAdapter
# from lib.loghelper import LogHelper
from lib.partnerhelper import PartnerHelper
from lib.bifrosthelper import AuthExchange
from lib.bifrosthelper import BifrostHelper
from lib.userhelper import UserHelper
from lib.usergrouphelper import UserGroupHelper
from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.runner_config_loader import RUNNER_CONFIG

AUTH_EXCHANGE_URL = "/auth/exchange"
HTTP_PROTOCOL = "http://"

env = RUNNER_CONFIG.get('ENVIRONMENT') or "QA12"
# env = "PROD"
env_dict = GLOBAL_CONFIG['QA_ENVIRONMENT'].get(env)
bifrost_host = env_dict.get('bifrost.host')

def generate_random_email(prefix):
    time_stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    id_timestamp = time_stamp.replace(":", "_").replace("-", "_")
    return "zhangj79+%s%s@mozy.com" % (prefix,id_timestamp)

def generate_random_string(prefix):
    time_stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    id_timestamp = time_stamp.replace(":", "_").replace("-", "_")
    return "%s%s" % (prefix,id_timestamp)

@when ('I create 1 {partnertype} new partner with')
def step_impl(context,partnertype):
    admin = {}
    admin['username'] = generate_random_email("clientqaautomation+bifrost+test+admin+")
    partner_body = {}
    if env_dict is not None:
        context.api_key = env_dict.get('mozy_dell_integration')['api_key']
        authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), context.api_key)
        token = (authexchange.get_auth_exchange())
        bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)

        if partnertype == "DellMozyPro":
            parent_partner_id = env_dict.get("mozy_dell_integration")['mozypro']['root_partner_id']
            root_role_id = env_dict.get("mozy_dell_integration")['mozypro']['root_role_id']
        elif partnertype == "DellMozyEnterprise":
            parent_partner_id = env_dict.get("mozy_dell_integration")['mozyenterprise']['root_partner_id']
            root_role_id = env_dict.get("mozy_dell_integration")['mozyenterprise']['root_role_id']
        elif partnertype == "DellSubPartner":
            assert(context.root_role_id != None)
            root_role_id = context.root_role_id
            parent_partner_id = context.partner.id
        for row in context.table:
            admin['full_name'] = row.get('admin fullname') or "test ELK"
            admin['password'] = row.get('admin password') or "QAP@SSw0rd"
            partner = PartnerHelper()
            partner.name = generate_random_string(str(row.get('name')))
            partner.root_role_id = root_role_id
            partner.parent_partner_id = parent_partner_id
            partner.admin = admin
            partner_body = {"name":partner.name,"admin":partner.admin,"root_role_id":partner.root_role_id, "parent_partner_id": partner.parent_partner_id}
            if row.get('external id'):
                partner.external_id = str(row.get('external id'))
                partner_body.update({"external_id":partner.external_id})
            if row.get('server plan'):
                partner.add_ons = {"server_plan":bool(str(row.get('server plan')))}
                partner_body.update({'add_ons':partner.add_ons})
            if row.get('sync'):
                partner.sync = bool(str(row.get('sync')))
                partner_body.update({"sync":partner.sync})
            if row.get('security_requirement'):
                partner.security_requirement = str(row.get('security_requirement'))
                partner_body.update({"security_requirement":partner.security_requirement})
            new_partner_response = bifrosthelper.post_accounts_partners(partner_body)
            content = new_partner_response.text
            json_content = json.loads(content)
            partner.id = json_content['items'][0]['data']['id']
            admin_response = json_content['items'][0]['data']['admin']
            partner.admin.update(admin_response)
            if hasattr(context,"partner"):
                context.subpartner = partner
            else:
                context.partner = partner
            context.response = new_partner_response
            print(partner.id)
    pass

@when('I {action} server add-ons for the new created partner')
def step_impl(context,action):
    assert (context.api_key != None)
    authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), context.api_key)
    token = (authexchange.get_auth_exchange())
    bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
    put_body = {"add_ons": {"server_plan": False}}
    if action == "enable":
        put_body = {"add_ons":{"server_plan":True}}
    elif action == "disable":
        put_body = {"add_ons": {"server_plan": False}}
    bifrosthelper.put_accounts_partner_id(context.partner.id,put_body)
    pass

@when('I search partner by')
def step_impl(context):
    for row in context.table:
        external_id = row.get('external id')
        authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), context.api_key)
        token = (authexchange.get_auth_exchange())
        bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
        response = bifrosthelper.get_accounts_partners({"external_id":external_id})
        context.response = response
    pass

@then('I should get {id} as the new created partner')
def step_impl(context):
    assert(context.response != None)
    assert(context.response)
    content = context.response.text
    json_content = json.loads(content)
    assert(json_content['items'][0]['data']['id'] == context.partner.id)

@when('I create a {usertype} new user with')
def step_impl(context,usertype):
    random_user_email = generate_random_email("clientqaautomation+bifrost+test+user+")
    if env_dict is not None:
        context.api_key = env_dict.get('mozy_dell_integration')['api_key']

        partner = PartnerHelper()
        if usertype == "DellSubPartner":
            partner_id = context.partner.id
        elif usertype == "DellMozyProStandalone":
            partner_id = env_dict.get('mozy_dell_integration')['mozypro']['root_partner_id']
        elif usertype == "DellMozyEnterpriseStandalone":
            partner_id = env_dict.get('mozy_dell_integration')['mozyenterprise']['root_partner_id']
        partner.id = partner_id
        if hasattr(context,'partner') == False:
            context.partner = partner
        authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), context.api_key,x_mozy_partner=partner_id)
        token = (authexchange.get_auth_exchange())
        bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)

        for row in context.table:
            useremail = row.get('username') or random_user_email
            password = row.get("password") or "QAP@SSw0rd"
            type = row.get('type')
            sync =row.get('sync')
            if row.get('user group'):
                context.user_group = bifrosthelper.Create_New_UserGroup(str(row.get('user group')), partner_id)
            else:
                # Use default user group
                context.user_group = bifrosthelper.Get_Default_UserGroup(partner_id)
            post_body = {"username": useremail, "password": password}
            if context.user_group.id != None:
                post_body.update({"user_group_id": context.user_group.id})
            if type != None:
                post_body.update({"type": str(type)})
            if sync != None:
                post_body.update({"sync": bool(sync)})

            post_user_response = bifrosthelper.post_accounts_users(post_body)
            context.response = post_user_response
            if post_user_response.status_code == 201:
                content = post_user_response.text
                json_content = json.loads(content)
                user = UserHelper()
                user.set_username(useremail)
                user.set_password(password)
                user.id = json_content['items'][0]['data']['id']
                context.user = user
    pass

@when('I assign storage for the user with')
def step_impl(context):
    if env_dict is not None:
        assert(context.api_key != None)
        authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), context.api_key)
        token = (authexchange.get_auth_exchange())
        bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
        for row in context.table:
            unit = row.get("unit") or "B"
            unit = str(unit)
            type = row.get('type') or "Desktop"
            type = str(type)
            if unit != "GB" and unit != "B":
                unit = "B"
            value = ast.literal_eval(row.get("value"))
            bifrosthelper.Set_StorageLimit_User(context.user.id, type,unit,value)
    pass

@then('I set licenses limit to the new created user')
def step_impl(context):
    if env_dict is not None:
        assert(context.api_key != None)
        assert(context.partner != None)
        partner_id = context.partner.id
        authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), context.api_key,
                                    x_mozy_partner=partner_id)
        token = (authexchange.get_auth_exchange())
        bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
        for row in context.table:
            license_type = row.get('license type') or "Desktop"
            license_number = row.get('licenses') or "1"
            licenses = ast.literal_eval(license_number)
            license_type = str(license_type)
            # context.user.product_keys = bifrosthelper.Create_New_Licenses_And_Assign_to_User(context.user.username,license_type,licenses)
            context.response = bifrosthelper.Set_Device_Limit_User(context.user.username,license_type,licenses)
            # context.user.product_keys
    pass

@when('I search the new created user via bifrost')
def step_impl(context):
    assert(env_dict is not None)
    assert(context.user != None)
    assert(context.partner != None)
    partner_id = context.partner.id
    authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), context.api_key,x_mozy_partner=partner_id)
    token = (authexchange.get_auth_exchange())
    bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
    context.response = bifrosthelper.get_accounts_users({'username':context.user.username},include_sub_partners=True)

@then('a DellMozyPro partner should be created')
def step_impl(context):
    pass

@when('I assign storage for the partner with')
def step_impl(context):
    for row in context.table:
        partner_id = context.partner.id
        api_key = env_dict.get('mozy_dell_integration')['api_key']
        authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), api_key,x_mozy_partner=partner_id)
        token = (authexchange.get_auth_exchange())
        bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)

        unit = row.get("unit") or "B"
        unit = str(unit)
        type = row.get('type') or "Desktop"
        type = str(type)
        if unit != "GB" and unit != "B":
            unit = "B"
        value = ast.literal_eval(row.get("value"))
        response = bifrosthelper.put_accounts_partner_storage(partner_id,type,{"pool_setting":"assigned", "pool_limit":{"unit": unit, "value": value}})
        context.response = response
    pass

@then('I should get response {response_code}')
def step_impl(context,response_code):
    assert(context.response.status_code == ast.literal_eval(response_code))
    if context.table:
        for attribute in context.table.headings:
            response_text = context.response.text
            json_content = json.loads(response_text)
            attribute = str(attribute)
            assert(str(json_content[attribute]) == str(context.table[0].get(attribute)))

@then('the partner storage should be')
def step_impl(context):
    authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), context.api_key)
    token = (authexchange.get_auth_exchange())
    for row in context.table:
        bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
        total_storage = bifrosthelper.Get_Partner_Storage(context.partner.id, row.get('type'), "total")
        if total_storage is not None:
            assert(total_storage == bifrosthelper.cal_byte(row.get('unit'),row.get('value')))
    pass

@when('I provision license for the {partner_type}')
def step_impl(context,partner_type):
    for row in context.table:
        authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), context.api_key)
        token = (authexchange.get_auth_exchange())
        bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
        license_type = str(row.get('license type')) or "Desktop"
        licenses = ast.literal_eval(row.get('licenses'))
        post_body = {"license_type": license_type, "licenses": licenses}
        if partner_type == "subpartner":
            assert(context.subpartner != None)
            partner_id = context.subpartner.id
        else:
            assert(context.partner != None and context.partner.id != "")
            partner_id = context.partner.id
        post_body.update({"partner_id":partner_id})
        # POST Licenses to User Group
        post_license_response = bifrosthelper.post_accounts_licenses(post_body)
        context.response = post_license_response
    pass

@when('I get licenses for the partner')
def step_impl(context):
    authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), context.api_key)
    token = (authexchange.get_auth_exchange())
    bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
    partner_id = context.partner.id
    for row in context.table:
       no_sub_partners = row.get("exclude sub-partner")
       offset = row.get("offset")
       limit = row.get("limit")
       assigned_email_address = row.get("user email")
       status = row.get("status")
       license_type = row.get("license type")

       get_query = {"partner_id":partner_id,"license_type":license_type}
       if no_sub_partners != None:
           get_query.update({"no_sub_partners":no_sub_partners})
       if status != None:
           get_query.update({"status":status})
       if offset != None:
           get_query.update({"offset":offset})
       if assigned_email_address != None:
           get_query.update({"assigned_email_address":assigned_email_address})
       if limit != None:
           get_query.update({"limit":limit})
       context.response = bifrosthelper.get_accounts_licenses(get_query)

@then('get licenses response detail should be')
def step_impl(context):
    response = context.response
    assert(response.status_code == 200)
    content = response.text
    json_content = json.loads(content)
    actual_total = json_content['total']
    actual_count = json_content['count']
    expected_total = expected_count = 0
    for row in context.table:
        if row.get('total') != None:
            expected_total = ast.literal_eval(row.get("total"))
            assert(actual_total == expected_total)
        if row.get('count') != None:
            expected_count = ast.literal_eval(row.get('count'))
            assert(actual_count == expected_count)

@then('5 licenses should be added to the partner')
def step_impl(context):
    pass

@when('I create 1 user under the partner')
def step_impl(context):
    for row in context.table:
        api_key = row.get('API_KEY') or api_key
        context.partner.set_api_key(api_key)
        time_stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        id_timestamp = time_stamp.replace(":", "_").replace("-", "_")
        random_user_email = "bifrost+demo+test+user+%s@mozy.com" % (id_timestamp)
        useremail = row.get('username') or random_user_email
        password = row.get("password") or "QAP@SSw0rd"
        user = UserHelper()
        user.set_username(useremail)
        user.set_password(password)

        authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), context.partner.api_key)
        token = (authexchange.get_auth_exchange())
        bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
        print(context.table)
        response = bifrosthelper.post_accounts_users({"username": user.username, "password": user.password})
        if response.status_code == 201:
            content = response.text
            json_content = json.loads(content)
            user.id = json_content['items'][0]['data']['id']
            context.user = user
            print(user.id)
    pass

@when('I transfer {license_number} licenses to the user')
def step_impl(context,license_number):
    licenses = ast.literal_eval(license_number)
    if len(context.key_strings) >= licenses:
        authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), context.partner.api_key)
        token = (authexchange.get_auth_exchange())
        bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
        for key in context.key_strings:
            transfer_license_response = bifrosthelper.put_accounts_license_keystring(key,context.user.username)
            if transfer_license_response.status_code == 200:
                print("assign key %s to user %s successfully" % (key,context.user.username))
    pass

@then('there should be 2 licenses for the user')
def step_impl(context):
    pass

@when('I act as the partner')
def step_imp(context):
    for row in context.table:
        partner = PartnerHelper()
        partner.id = ast.literal_eval(row.get('partner id'))
        partner.admin = { "username": str(row.get('admin username'))}
        context.partner = partner

    pass

@then('I act as the new created partner')
def step_impl(context):

    pass

@then('I generate {license_number} licenses to default user group')
def step_impl(context,license_number):
    authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), context.partner.api_key)
    token = (authexchange.get_auth_exchange())
    bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
    get_partner_id_response = bifrosthelper.get_accounts_partner_id(context.partner.id)
    if get_partner_id_response.status_code == 200:
        content = get_partner_id_response.text
        json_content = json.loads(content)
        user_group = UserGroupHelper()
        user_group.id = json_content['items'][0]['data']['admin']['user_groups'][0]
        context.user_group = user_group

        for row in context.table:
            license_type = str(row.get('license type')) or "Desktop"
            licenses = ast.literal_eval(license_number)
            # POST Licenses to User Group
            post_license_response = bifrosthelper.post_accounts_licenses({"license_type":license_type,"licenses":licenses})
            if post_license_response.status_code == 201:
                content = post_license_response.text
                json_content = json.loads(content)
                licenses_array = json_content['items']
                key_strings = []
                for license_keys in licenses_array:
                    key_strings.append(license_keys['data']['keystring'])
                context.key_strings = key_strings

    pass

@when('I generate licenses to the new created partner')
def step_impl(context):
    assert((context.api_key != None))
    api_key = context.api_key
    authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), api_key)
    token = (authexchange.get_auth_exchange())
    bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
    for row in context.table:
        license_type = str(row.get('license type')) or "Desktop"
        licenses = ast.literal_eval(row.get('licenses'))
        assert(licenses > 0)
        bifrosthelper.Create_New_Licenses(context.partner.id,license_type,licenses)
    pass

@when('I create user with')
def step_impl(context):
    env = RUNNER_CONFIG.get('ENVIRONMENT') or "QA12"
    env_dict = GLOBAL_CONFIG['QA_ENVIRONMENT'].get(env)
    if env_dict is not None:
        partner_id = env_dict.get('bifrost.partner.id')
        api_key = env_dict.get('bifrost.partner.api_key')
        bifrost_host = env_dict.get('bifrost.host')
        #check new user group, and create user under the user group
        for row in context.table:
            time_stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            id_timestamp = time_stamp.replace(":", "_").replace("-", "_")
            random_user_email = "test+elk+user+%s@mozy.com" % (id_timestamp)
            useremail = row.get('username') or random_user_email
            password = row.get("password") or "QAP@SSw0rd"

            authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), api_key)
            token = (authexchange.get_auth_exchange())
            bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
            print(context.table)

            if row.get('user group'):
                context.user_group = bifrosthelper.Create_New_UserGroup(str(row.get('user group')),partner_id)
            else:
                # Use default user group
                context.user_group = bifrosthelper.Get_Default_UserGroup(partner_id)

            context.user = bifrosthelper.Create_New_User(useremail,password,context.user_group.id)
            context.api_key = api_key
            license_type = row.get('license type') or "Desktop"
            license_number = row.get('licenses') or "1"
            licenses = ast.literal_eval(license_number)
            license_type = str(license_type)
            context.user.product_keys = bifrosthelper.Create_New_Licenses_And_Assign_to_User(context.user.username,license_type,licenses)
    pass

@when('I activate 1 machine for the new created user via bifrost')
def step_impl(context):
    env = RUNNER_CONFIG.get('ENVIRONMENT') or "QA12"
    env_dict = GLOBAL_CONFIG['QA_ENVIRONMENT'].get(env)
    if env_dict is not None:
        api_key = env_dict.get('bifrost.partner.api_key')
        bifrost_host = env_dict.get('bifrost.host')
        for row in context.table:
            if row.get('name'):
                machine_name = str(row.get('name'))
            else:
                machine_name = "testmachine1"
            if row.get('user_id'):
                user_id = row.get("user_id")
            else:
                user_id = context.user.id
            if row.get('type'):
                type = str(row.get('type'))
            else:
                type = "Desktop"
            if row.get('site'):
                site = str(row.get('site'))
            else:
                site = "q12a"
            authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), api_key)
            token = (authexchange.get_auth_exchange())
            bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
            context.machine_id = bifrosthelper.Create_New_Machine(user_id=user_id,name=machine_name,type=type,site=site)
            assert (context.machine_id != -1)

@then('I delete the new created user group')
def step_impl(context):
    env = RUNNER_CONFIG.get('ENVIRONMENT') or "QA12"
    env_dict = GLOBAL_CONFIG['QA_ENVIRONMENT'].get(env)
    if context.api_key:
        api_key = context.api_key
    else:
        api_key = env_dict.get('bifrost.partner.api_key')
    bifrost_host = env_dict.get('bifrost.host')
    authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), api_key)
    token = (authexchange.get_auth_exchange())
    bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
    if context.user_group.id != None:
        bifrosthelper.Delete_User_Group(context.user_group.id)

@when('I {action} the new created partner')
def step_impl(context,action):
    api_key = context.api_key
    authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), api_key)
    token = (authexchange.get_auth_exchange())
    bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
    if context.partner != None and context.partner.id != "":
        if action == "suspend":
            bifrosthelper.Suspend_Partner(context.partner.id)
        elif action == "resume":
            bifrosthelper.Resume_Partner(context.partner.id)
        elif action == "delete":
            bifrosthelper.Delete_Partner(context.partner.id)

@when('I {action} the new created user')
def step_impl(context,action):
    # api_key = env_dict.get('mozy_dell_integration')['api_key']
    api_key = context.api_key
    authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), api_key)
    token = (authexchange.get_auth_exchange())
    bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
    assert(context.user != None)
    assert(context.user.id != "")
    if action == "suspend":
        bifrosthelper.Suspend_User(context.user.id)
    elif action == "resume":
        bifrosthelper.Resume_User(context.user.id)
    elif action == "delete":
        delete_user_response = bifrosthelper.delete_accounts_user_id(context.user.id)
        assert(delete_user_response.status_code == 200)

@then('I activate {machine_num} machine with the new created user')
def step_impl(context,machine_num):
    assert(context.api_key != None)
    api_key = context.api_key
    assert(context.user != None)
    assert(context.user.id != "")
    authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), api_key)
    token = (authexchange.get_auth_exchange())
    bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
    machine_number = ast.literal_eval(machine_num)
    # if machine_number >0:
    #     for i in (0,machine_number):


    pass

@then('I send email to the new created {accounttype}')
def step_impl(context,accounttype):
    assert(context.api_key != None)
    api_key = context.api_key
    authexchange = AuthExchange(('%s%s%s' % (HTTP_PROTOCOL, bifrost_host, AUTH_EXCHANGE_URL)), api_key)
    token = (authexchange.get_auth_exchange())
    bifrosthelper = BifrostHelper(('%s%s' % (HTTP_PROTOCOL, bifrost_host)), token)
    if accounttype == 'partner':
        assert(context.partner != None)
        assert(context.partner.admin != None)
        assert(context.partner.admin['id'] != None)
        if context.partner.admin['id'] != None:
            bifrosthelper.Send_Email_Partner(context.partner.admin['id'])
    elif accounttype == 'user':
        assert(context.user != None)
        assert(context.user.id != None)
        if context.user.id != None:
            bifrosthelper.Send_Email_User(context.user.id)
    pass













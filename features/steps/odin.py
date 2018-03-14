import time
import sure
from configuration.global_config_loader import GLOBAL_CONFIG
from configuration.runner_config_loader import RUNNER_CONFIG
from configuration.mts.mts_config_loader import MTS_CONFIG
from lib.odinhelper import OdinHelper

env = RUNNER_CONFIG.get('ENVIRONMENT') or "QA12"
global_env_dict = GLOBAL_CONFIG['QA_ENVIRONMENT'].get(env)
odin_host = global_env_dict.get('mozy.odinhost')
odin_test_data_dict = MTS_CONFIG.get("%s_ODIN" % env)
api_key = odin_test_data_dict.get("API_KEY")
default_password = 'QAP@SSw0rd'
parent_partner_id = odin_test_data_dict.get("PARTNER_ID")
default_quota = 2L


def generate_random_string(prefix):
    timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    return "%s%s" % (prefix, timestamp)


@given('Use Odin Version {version}')
def step_impl(context, version):
    context.version = version
    context.wsdl_api_prefix = "/api/%s" % version

@then('I use odin to query root partner by id')
def step_impl(context):
    wsdl_api = "%s/partner/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    if not hasattr(context, 'partners'):
        context.partners = {}

    # compose the request_body
    request_body = {
        'api_key': api_key,
        'id': parent_partner_id
    }

    # send SOAP request to get partner
    response = OdinHelper(
        odin_host, wsdl_api, testcase=context.tc.name).get(request_body)

    # check if response size is 1
    response.should.have.key('size').being.equal(1L)
    response.should.have.key('results').being.have.length_of(1)
    partner_info = response['results'][0]
    partner_info.should.be.a(dict)
    partner_info.should.have.key('root_admin').being.be.a(dict)

    partner = {
        'subdomain': partner_info.get('subdomain'),
        'name': partner_info.get('name'),
        'external_id': partner_info.get('external_id'),
        'parent_partner_id': partner_info.get('parent_partner_id'),
        'root_role_id': partner_info.get('root_role_id'),
        'id': parent_partner_id,
        'default_user_group_id': partner_info.get('default_user_group_id'),
        'root_admin_external_id': partner_info['root_admin']['external_id'],
        'root_admin_username': partner_info['root_admin']['username'],
        'root_admin_full_name': partner_info['root_admin']['full_name'],
        'root_admin_id': partner_info['root_admin']['id'],
        'root_admin_user_groups': partner_info['root_admin']['user_groups'],
        'root_admin_roles': partner_info['root_admin']['roles']
    }
    if context.version == '0.1.40':
        partner['phone'] = partner_info['phone']
    if context.version == '0.1.50':
        partner['enable_sync'] = partner_info['enable_sync']
        partner['default_sync_quota'] = partner_info['default_sync_quota']

    # save returned partner_info to context.partners[parent_partner_id]
    context.partners[parent_partner_id] = partner

# create <row_count_of_table> partner(s)
@when('I use odin to create new partner with')
def step_impl(context):
    wsdl_api = "%s/partner/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    if not hasattr(context, 'partners'):
        context.partners = {}

    # loop for each row, which represent a single partner to be created
    for row in context.table:
        # compose the expected partner info
        partner = {}
        partner['name'] = row.get('name') or generate_random_string(
            row.get('name_prefix') or 'odin_mon_partner_')
        partner['root_admin_username'] = row.get('root_admin_username') or \
            "%s@emc.com" % generate_random_string(
                row.get('root_admin_username_prefix') or
                'odin_mon_root_admin_')
        partner['root_admin_password'] = \
            row.get('root_admin_password') or default_password
        partner['root_admin_full_name'] = row.get('root_admin_full_name') or \
            generate_random_string(
                row.get('root_admin_full_name_prefix') or
                'odin_mon_root_admin_name_')
        partner['parent_partner_id'] = row.get('parent_partner_id') or None
        # company_type could be business, reseller, corp (None means business)
        partner['company_type'] = row.get('company_type') or None
        partner['subdomain'] = row.get('subdomain') or (
            row.get('subdomain_prefix') and
            generate_random_string(row.get('subdomain_prefix'))) or None
        partner['root_role'] = row.get('root_role') or None
        partner['external_id'] = row.get('external_id') or (
            row.get('external_id_prefix') and
            generate_random_string(row.get('external_id_prefix'))) or None
        partner['root_admin_external_id'] = \
            row.get('root_admin_external_id') or (
                row.get('root_admin_external_id_prefix') and
                generate_random_string(
                    row.get('root_admin_external_id_prefix'))) or None
        # phone is only available in 0.1.40
        if context.version == '0.1.40':
            partner['phone'] = row.get('phone') or None
        # enable_sync and default_sync_quota are only available in 0.1.50
        # available value of enable_sync: None, True, False
        # available value of default_sync_quota: None, <long>
        if context.version == '0.1.50':
            if row.get('enable_sync') is None:
                partner['enable_sync'] = None
            else:
                partner['enable_sync'] = str(
                    row.get('enable_sync')).lower() in (
                    'true', 'yes', 't', 'y', '1')
            if row.get('default_sync_quota') is None:
                partner['default_sync_quota'] = None
            else:
                partner['default_sync_quota'] = long(
                    row.get('default_sync_quota'))

        # compose the request_body
        request_body = partner.copy()
        request_body['api_key'] = api_key

        # send SOAP request to create partner
        partner_id = OdinHelper(
            odin_host, wsdl_api, testcase=context.tc.name).create(request_body)

        # print('partner %s has been created!' % partner_id)

        # check if the response is a valid id
        partner_id.should.be.a(long)

        # update the expected partner info
        partner['id'] = partner_id
        partner['parent_partner_id'] = \
            partner['parent_partner_id'] or parent_partner_id
        partner['root_admin_username'] = partner['root_admin_username'].lower()
        if context.version == '0.1.50':
            # If parent_partner.enable_sync is True:
            # - set partner.enable_sync to None/True, quota to None/long_var =>
            # -- enable_sync will be True, quota will be 2L/long_var
            # - set partner.enable_sync to False, quota to None/long_var =>
            # -- enable_sync will be False, quota will be None
            # If parent partner.enable_sync is None/False:
            # - set partner.enable_sync to True =>
            # -- raise Exception
            # - set partner.enable_sync to None/False, quota to None/<long> =>
            # -- enable_sync will be None, quota will be None
            if partner['parent_partner_id'] in context.partners:
                parent_partner = context.partners[partner['parent_partner_id']]
                parent_enable_sync = parent_partner['enable_sync']
                parent_default_sync_quota = \
                    parent_partner['default_sync_quota']
            else:
                parent_enable_sync = None
                parent_default_sync_quota = None
            if parent_enable_sync is True:
                if partner['enable_sync'] is False:
                    partner['default_sync_quota'] = None
                else:
                    partner['enable_sync'] = True
                    if partner['default_sync_quota'] is None:
                        partner['default_sync_quota'] = \
                            parent_default_sync_quota or default_quota
            else:
                partner['enable_sync'] = None
                partner['default_sync_quota'] = None

        # add created partner infos to context.partners dict
        # save the last partner id to context.partner_id
        context.partners[partner_id] = partner
        context.partner_id = partner_id

# get context.partner_id
@then('I use odin to query this partner by id')
def step_impl(context):
    wsdl_api = "%s/partner/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    # context.should.have.property('partner_id')
    # context.should.have.property('partners').being.have.key(context.partner_id)
    if not hasattr(context, 'partner_id') or \
            not hasattr(context, 'partners') or \
            context.partner_id not in context.partners:
        raise ValueError("No valid partner has been created before!")

    # compose the request_body
    request_body = {
        'api_key': api_key,
        'id': context.partner_id
    }

    # send SOAP request to get partner
    response = OdinHelper(
        odin_host, wsdl_api,
        testcase=context.tc.name).get(request_body)

    # print('Get partner %s response: %s' % (context.partner_id, response))

    # check if align with context.partners[context.partner_id]
    response.should.have.key('size').being.equal(1L)
    response.should.have.key('results').being.have.length_of(1)
    actual_partner_info = response['results'][0]
    expected_partner_info = context.partners[context.partner_id]
    actual_partner_info.should.have.key(
        'status').being.equal('active')
    actual_partner_info.should.have.key(
        'subdomain').being.equal(expected_partner_info['subdomain'])
    actual_partner_info.should.have.key(
        'name').being.equal(expected_partner_info['name'])
    actual_partner_info.should.have.key(
        'external_id').being.equal(expected_partner_info['external_id'])
    actual_partner_info.should.have.key(
        'parent_partner_id').being.equal(
        expected_partner_info['parent_partner_id'])
    actual_partner_info.should.have.key(
        'root_role_id').being.equal(expected_partner_info['root_role'])
    actual_partner_info.should.have.key('id').being.equal(context.partner_id)
    # if query this partner for the first time
    # add default_user_group_id into context.partners[context.partner_id]
    if 'default_user_group_id' in expected_partner_info:
        actual_partner_info.should.have.key(
            'default_user_group_id').being.equal(
            expected_partner_info['default_user_group_id'])
    else:
        actual_partner_info.should.have.key(
            'default_user_group_id').being.be.a(long)
        expected_partner_info['default_user_group_id'] = \
            actual_partner_info['default_user_group_id']
    actual_partner_info.should.have.key(
        'root_admin').being.have.key(
        'partner_id').being.equal(context.partner_id)
    actual_partner_info['root_admin'].should.have.key(
        'external_id').being.equal(
        expected_partner_info['root_admin_external_id'])
    actual_partner_info['root_admin'].should.have.key(
        'username').being.equal(expected_partner_info['root_admin_username'])
    actual_partner_info['root_admin'].should.have.key(
        'full_name').being.equal(expected_partner_info['root_admin_full_name'])
    # if query this partner for the first time
    # add root_admin_id into context.partners[context.partner_id]
    if 'root_admin_id' in expected_partner_info:
        actual_partner_info['root_admin'].should.have.key(
            'id').being.equal(expected_partner_info['root_admin_id'])
    else:
        actual_partner_info['root_admin'].should.have.key(
            'id').being.be.a(long)
        expected_partner_info['root_admin_id'] = \
            actual_partner_info['root_admin']['id']
    actual_partner_info['root_admin'].should.have.key(
        'parent_admin_id').being.equal(expected_partner_info['root_admin_id'])
    if context.version == '0.1.40':
        actual_partner_info.should.have.key(
            'phone').being.equal(expected_partner_info['phone'])
    if context.version == '0.1.50':
        actual_partner_info.should.have.key(
            'enable_sync').being.equal(expected_partner_info['enable_sync'])
        actual_partner_info.should.have.key(
            'default_sync_quota').being.equal(
            expected_partner_info['default_sync_quota'])
    # TODO: check admin.user_groups
    # TODO: check admin.roles

# create <row_count_of_table> user_group(s) under context.partner_id
@when('I use odin to create new user_group under this partner with')
def step_impl(context):
    wsdl_api = "%s/user_group/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    # context.should.have.property('partner_id')
    # context.should.have.property('partners').being.have.key(context.partner_id)
    if not hasattr(context, 'partner_id') or \
            not hasattr(context, 'partners') or \
            context.partner_id not in context.partners:
        raise ValueError("No valid partner has been created before!")
    if not hasattr(context, 'user_groups'):
        context.user_groups = {}

    # loop for each row, which represent a single user_group to be created
    for row in context.table:
        # compose the expected user_group info
        user_group = {}
        user_group['partner_id'] = context.partner_id
        user_group['name'] = row.get('name') or generate_random_string(
            row.get('name_prefix') or 'odin_mon_user_group_')
        if 'default_server_quotas' in row or 'default_desktop_quotas' in row:
            user_group['default_quotas'] = []
            if 'default_server_quotas' in row:
                user_group['default_quotas'].append(
                    {'type': 'Server', 'quota': row.get(
                        'default_server_quotas')})
            if 'default_desktop_quotas' in row:
                user_group['default_quotas'].append(
                    {'type': 'Desktop', 'quota': row.get(
                        'default_desktop_quotas')})
        user_group['default_for_partner'] = str(
            row.get('default_for_partner')).lower() in (
            'true', 'yes', 't', 'y', '1')
        user_group['external_id'] = row.get('external_id') or (
            row.get('external_id_prefix') and generate_random_string(
                row.get('external_id_prefix'))) or None
        # enable_sync is only available in 0.1.50
        # available value of enable_sync: None, True, False
        if context.version == '0.1.50':
            if row.get('enable_sync') is None:
                user_group['enable_sync'] = None
            else:
                user_group['enable_sync'] = str(
                    row.get('enable_sync')).lower() in (
                    'true', 'yes', 't', 'y', '1')

        # compose the request_body
        request_body = user_group.copy()
        request_body['api_key'] = api_key

        # send SOAP request to create user_group
        user_group_id = OdinHelper(
            odin_host, wsdl_api, testcase=context.tc.name).create(request_body)

        # print('user_group %s has been created!' % user_group_id)

        # check if the response is a valid id
        user_group_id.should.be.a(long)

        # update the expected user_group info
        user_group['id'] = user_group_id
        user_group['default_quotas'] = user_group.get('default_quotas') or \
            [{'type': 'Server', 'quota': default_quota},
                {'type': 'Desktop', 'quota': default_quota}]
        if user_group['default_for_partner']:
            context.partners[context.partner_id]['default_user_group_id'] = \
                user_group_id
        # If partner.enable_sync is True:
        # - set user_group.enable_sync to None/True =>
        # -- enable_sync will be True
        # - set user_group.enable_sync to False =>
        # -- enable_sync will be False
        # If partner.enable_sync is None/False:
        # - set user_group.enable_sync to True =>
        # -- raise Exception
        # - set user_group.enable_sync to None/False =>
        # -- enable_sync will be None
        if context.version == '0.1.50':
            if context.partners[context.partner_id]['enable_sync'] is True:
                if user_group['enable_sync'] is None:
                    user_group['enable_sync'] = True
            else:
                user_group['enable_sync'] = None

        # save created user_group infos to context.user_groups dict
        # save the last user_group id to context.user_group_id
        context.user_groups[user_group_id] = user_group
        context.user_group_id = user_group_id

# get context.user_group_id
@then('I use odin to query this user_group by id')
def step_impl(context):
    wsdl_api = "%s/user_group/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    # context.should.have.property('user_group_id')
    # context.should.have.property(
    #     'user_groups').being.have.key(context.user_group_id)
    if not hasattr(context, 'user_group_id') or \
            not hasattr(context, 'user_groups') or \
            context.user_group_id not in context.user_groups:
        raise ValueError("No valid user_group has been created before!")

    # compose the request_body
    request_body = {
        'api_key': api_key,
        'id': context.user_group_id
    }

    # send SOAP request to get user_group
    response = OdinHelper(
        odin_host, wsdl_api, testcase=context.tc.name).get(request_body)

    # print('Get user_group %s response: %s' % (context.user_group_id, response))

    # check if align with context.user_groups[context.user_group_id]
    response.should.have.key('size').being.equal(1L)
    response.should.have.key('results').being.have.length_of(1)
    actual_user_group_info = response['results'][0]
    expected_user_group_info = context.user_groups[context.user_group_id]
    actual_user_group_info.should.have.key(
        'partner_id').being.equal(expected_user_group_info['partner_id'])
    actual_user_group_info.should.have.key(
        'external_id').being.equal(expected_user_group_info['external_id'])
    actual_user_group_info.should.have.key(
        'default_quotas')
    actual_user_group_info['default_quotas'].sort()
    expected_user_group_info['default_quotas'].sort()
    actual_user_group_info['default_quotas'].should.equal(
        expected_user_group_info['default_quotas'])
    actual_user_group_info.should.have.key(
        'name').being.equal(expected_user_group_info['name'])
    actual_user_group_info.should.have.key(
        'id').being.equal(context.user_group_id)
    if context.version == '0.1.50':
        actual_user_group_info.should.have.key(
            'enable_sync').being.equal(expected_user_group_info['enable_sync'])

# create <row_count_of_table> admin(s) under context.partner_id
@when('I use odin to create new admin under this partner with')
def step_impl(context):
    wsdl_api = "%s/admin/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    # context.should.have.property('partner_id')
    # context.should.have.property('partners').being.have.key(context.partner_id)
    if not hasattr(context, 'partner_id') or \
            not hasattr(context, 'partners') or \
            context.partner_id not in context.partners:
        raise ValueError("No valid partner has been created before!")
    if not hasattr(context, 'admins'):
        context.admins = {}

    # loop for each row, which represent a single admin to be created
    for row in context.table:
        # compose the expected admin info
        admin = {}
        admin['parent_admin_id'] = \
            context.partners[context.partner_id]['root_admin_id']
        admin['username'] = row.get('username') or \
            "%s@emc.com" % generate_random_string(
                row.get('username_prefix') or 'odin_mon_admin_username_')
        admin['password'] = row.get('password') or default_password
        admin['full_name'] = row.get('full_name') or \
            "%s@emc.com" % generate_random_string(
                row.get('full_name_prefix') or 'odin_mon_admin_full_name_')
        admin['external_id'] = row.get('external_id') or (
            row.get('external_id_prefix') and generate_random_string(
                row.get('external_id_prefix'))) or None
        # TODO: user_groups
        # TODO: roles

        # compose the request_body
        request_body = admin.copy()
        request_body['api_key'] = api_key

        # send SOAP request to create admin
        admin_id = OdinHelper(
            odin_host, wsdl_api, testcase=context.tc.name).create(request_body)

        # print('admin %s has been created!' % admin_id)

        # check if the response is a valid id
        admin_id.should.be.a(long)

        # update the expected admin info
        admin['id'] = admin_id
        admin['username'] = admin['username'].lower()
        admin['partner_id'] = context.partner_id

        # save expected admin info to context.admins dict
        # save the last admin id to context.admin_id
        context.admins[admin_id] = admin
        context.admin_id = admin_id

# get context.admin_id
@then('I use odin to query this admin by id')
def step_impl(context):
    wsdl_api = "%s/admin/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    # context.should.have.property('admin_id')
    # context.should.have.property('admins').being.have.key(context.admin_id)
    if not hasattr(context, 'admin_id') or \
            not hasattr(context, 'admins') or \
            context.admin_id not in context.admins:
        raise ValueError("No valid admin has been created before!")

    # compose the request_body
    request_body = {
        'api_key': api_key,
        'id': context.admin_id
    }

    # send SOAP request to get admin
    response = OdinHelper(
        odin_host, wsdl_api, testcase=context.tc.name).get(request_body)

    # print('Get admin %s response: %s' % (context.admin_id, response))

    # check if align with context.admin[context.admin_id]
    response.should.have.key('size').being.equal(1L)
    response.should.have.key('results').being.have.length_of(1)
    actual_admin_info = response['results'][0]
    expected_admin_info = context.admins[context.admin_id]
    actual_admin_info.should.have.key(
        'parent_admin_id').being.equal(expected_admin_info['parent_admin_id'])
    actual_admin_info.should.have.key(
        'partner_id').being.equal(expected_admin_info['partner_id'])
    actual_admin_info.should.have.key(
        'external_id').being.equal(expected_admin_info['external_id'])
    actual_admin_info.should.have.key(
        'username').being.equal(expected_admin_info['username'])
    actual_admin_info.should.have.key(
        'full_name').being.equal(expected_admin_info['full_name'])
    actual_admin_info.should.have.key(
        'id').being.equal(context.admin_id)
    # TODO: user_groups
    # TODO: roles

# deliver email
@when('I use odin to deliver email to this {resource} with')
def step_impl(context, resource):
    wsdl_api = "%s/email/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    if not hasattr(context, 'emails'):
        context.emails = {}
    email = {}
    default_template = None
    if resource == 'admin':
        # context.should.have.property('admin_id')
        if not hasattr(context, 'admin_id'):
            raise ValueError("No valid admin has been created before!")
        email['admin_id'] = context.admin_id
        default_template = 'admin_account_created'
    elif resource == 'user':
        if not hasattr(context, 'user_id'):
            raise ValueError("No valid user has been created before!")
        # context.should.have.property('user_id')
        email['user_id'] = context.user_id
        default_template = 'new_user_notification'
    else:
        raise ValueError("Illegal to send email to %s!" % resource)

    # loop for each row, which represent a single email to be delivered
    for row in context.table:
        # compose the expected email info
        email['template'] = row.get('template') or default_template
        email['email'] = row.get('email') or None
        email['language'] = row.get('language') or None

        # compose the request_body
        request_body = email.copy()
        request_body['api_key'] = api_key

        # send SOAP request to deliver email
        response = OdinHelper(
            odin_host, wsdl_api,
            testcase=context.tc.name).deliver(request_body)

        # print('Send %s email to %s %s response: %s' % (
            # email['template'], resource,
            # email.get('admin_id') or email.get('user_id'), response))

        # check if response is True
        response.should.be.equal(True)

# TODO
# @when('I login {mail_server_link} to check the latest email')

# create <row_count_of_table> user(s) under context.user_group_id
@when('I use odin to create new user under this user_group with')
def step_impl(context):
    wsdl_api = "%s/user/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    # context.should.have.property('user_group_id')
    # context.should.have.property(
    #     'user_groups').being.have.key(context.user_group_id)
    if not hasattr(context, 'user_group_id') or \
            not hasattr(context, 'user_groups') or \
            context.user_group_id not in context.user_groups:
        raise ValueError("No valid user_group has been created before!")
    if not hasattr(context, 'users'):
        context.users = {}

    # loop for each row, which represent a single user to be created
    for row in context.table:
        # compose the expected user info
        user = {}
        user['user_group_id'] = context.user_group_id
        user['username'] = row.get('username') or \
            "%s@emc.com" % generate_random_string(
                row.get('username_prefix') or 'odin_mon_user_username_')
        user['password'] = row.get('password') or default_password
        user['full_name'] = row.get('full_name') or \
            "%s@emc.com" % generate_random_string(
                row.get('full_name_prefix') or 'odin_mon_user_full_name_')
        user['external_id'] = row.get('external_id') or (
            row.get('external_id_prefix') and generate_random_string(
                row.get('external_id_prefix'))) or None
        # TODO: user_groups
        # TODO: roles

        # compose the request_body
        request_body = user.copy()
        request_body['api_key'] = api_key

        # send SOAP request to create user
        user_id = OdinHelper(
            odin_host, wsdl_api,
            testcase=context.tc.name).create(request_body)

        # print('user %s has been created!' % user_id)

        # check if the response is a valid id
        user_id.should.be.a(long)

        # update the expected user info
        user['id'] = user_id
        user['username'] = user['username'].lower()
        if context.version == '0.1.50':
            user['enable_sync'] = False

        # save expected user info to context.users dict
        # save the last user id to context.user_id
        context.users[user_id] = user
        context.user_id = user_id

# get context.user_id
@then('I use odin to query this user by id')
def step_impl(context):
    wsdl_api = "%s/user/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    # context.should.have.property('user_id')
    # context.should.have.property('users').being.have.key(context.user_id)
    if not hasattr(context, 'user_id') or \
            not hasattr(context, 'users') or \
            context.user_id not in context.users:
        raise ValueError("No valid user has been created before!")

    # compose the request_body
    request_body = {
        'api_key': api_key,
        'id': context.user_id
    }

    # send SOAP request to get user
    response = OdinHelper(
        odin_host, wsdl_api,
        testcase=context.tc.name).get(request_body)

    # print('Get user %s response: %s' % (context.user_id, response))

    # check if align with context.users[context.user_id]
    response.should.have.key('size').being.equal(1L)
    response.should.have.key('results').being.have.length_of(1)
    actual_user_info = response['results'][0]
    expected_user_info = context.users[context.user_id]
    actual_user_info.should.have.key(
        'user_group_id').being.equal(expected_user_info['user_group_id'])
    actual_user_info.should.have.key(
        'external_id').being.equal(expected_user_info['external_id'])
    actual_user_info.should.have.key(
        'username').being.equal(expected_user_info['username'])
    actual_user_info.should.have.key(
        'full_name').being.equal(expected_user_info['full_name'])
    actual_user_info.should.have.key(
        'id').being.equal(context.user_id)
    if context.version == '0.1.50':
        actual_user_info.should.have.key(
            'enable_sync').being.equal(expected_user_info['enable_sync'])

# provision <row_count_of_table> resources for context.user_group_id
@when('I use odin to provision resources to this user_group with')
def step_impl(context):
    wsdl_api = "%s/resource/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    # context.should.have.property('user_group_id')
    # context.should.have.property(
    #     'user_groups').being.have.key(context.user_group_id)
    if not hasattr(context, 'user_group_id') or \
            not hasattr(context, 'user_groups') or \
            context.user_group_id not in context.user_groups:
        raise ValueError("No valid user_group has been created before!")
    partner_id = context.user_groups[context.user_group_id]['partner_id']
    if not hasattr(context, 'resources'):
        context.resources = {}
    if context.user_group_id not in context.resources:
        context.resources[context.user_group_id] = {}
    if not hasattr(context, 'licenses'):
        context.licenses = {}

    # loop for each row, which represent a batch of resources to be provisioned
    for row in context.table:
        # compose the request_body
        license_type = row.get('license_type') or 'Desktop'
        licenses = long(row.get('licenses') or 1)
        quota = long(row.get('quota') or 2)
        request_body = {
            'api_key': api_key,
            'partner_id': partner_id,
            'user_group_id': context.user_group_id,
            'license_type': license_type,
            'licenses': licenses,
            'quota': quota
        }

        # send SOAP request to provision resources
        response = OdinHelper(
            odin_host, wsdl_api,
            testcase=context.tc.name).provision(request_body)

        # print('Provision resource to user_group %s response: %s' % (
            # context.user_group_id, response))

        # check if correct resources have been created
        response.should.have.key('size').being.equal(licenses)
        response.should.have.key('results').being.have.length_of(licenses)

        # save created licenses and quotas info to context.resources dict
        user_group_resources = context.resources[context.user_group_id]
        if license_type not in user_group_resources:
            user_group_resources[license_type] = {
                'licenses': [],
                'quota': quota,
                'used_licenses': []
            }
        else:
            user_group_resources[license_type]['quota'] += quota
        for result in response['results']:
            result.should.have.key('license_type').being.equal(license_type)
            result.should.have.key(
                'user_group_id').being.equal(context.user_group_id)
            result.should.have.key('machine_id').being.none
            result.should.have.key('assigned_email_address').being.none
            result.should.have.key('keystring').being.a(str)
            user_group_resources[license_type]['licenses'].append(
                result['keystring'])
            # TODO: expires_at
            # TODO: quota_desired
            # TODO: external_id

            # save the last licenses to context.licenses[license_type]
            context.licenses[license_type] = result['keystring']

# create <row_count_of_table> machine(s) for context.user_id
@when('I use odin to create new machine for this user')
def step_impl(context):
    wsdl_api = "%s/machine/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    # context.should.have.property('user_id')
    # context.should.have.property('users').being.have.key(context.user_id)
    if not hasattr(context, 'user_id') or \
            not hasattr(context, 'users') or \
            context.user_id not in context.users:
        raise ValueError("No valid user has been created before!")
    user_group_id = context.users[context.user_id]['user_group_id']
    if not hasattr(context, 'user_groups') or \
            user_group_id not in context.user_groups:
        raise ValueError("No valid user_group has been created before!")
    # context.should.have.property('licenses')
    if not hasattr(context, 'licenses'):
        raise ValueError("No valid license has been created before!")
    if not hasattr(context, 'machines'):
        context.machines = {}

    # loop for each row, which represent a single machine to be created
    for row in context.table:
        # compose the expected machine info
        machine = {}
        machine['user_id'] = context.user_id
        license_type = row.get('license_type') or 'Desktop'
        context.licenses.should.have.key(license_type)
        context.resources.should.have.key(
            user_group_id).being.have.key(license_type)
        res_license_type = \
            context.resources[user_group_id][license_type]
        res_license_type.should.have.key('licenses')
        res_license_type.should.have.key('quota')
        res_license_type.should.have.key('used_licenses')
        machine['keystring'] = context.licenses[license_type]
        machine['alias'] = row.get('alias') or (
            row.get('alias_prefix') and generate_random_string(
                row.get('alias_prefix'))) or None
        machine['external_id'] = row.get('external_id') or (
            row.get('external_id_prefix') and generate_random_string(
                row.get('external_id_prefix'))) or None
        machine['quota_desired'] = (
            row.get('quota_desired') and long(
                row.get('quota_desired'))) or None
        machine['region'] = row.get('region') or None
        machine['machine_hash'] = row.get('machine_hash') or None

        # compose the request_body
        request_body = machine.copy()
        request_body['api_key'] = api_key

        # send SOAP request to create machine
        machine_id = OdinHelper(
            odin_host, wsdl_api,
            testcase=context.tc.name).create(request_body)

        # print('machine %s has been created!' % machine_id)

        # check if the response is a valid id
        machine_id.should.be.a(long)

        # update the expected machine info
        if machine['quota_desired'] is None:
            for item in context.user_groups[user_group_id]['default_quotas']:
                if item['type'] == license_type:
                    machine['quota_desired'] = item['quota']
                    break

        # save expected machine info to context.machines dict
        # save the last machine id to context.machine_id
        context.machines[machine_id] = machine
        context.machine_id = machine_id

        # move used_license
        # from context.resources[user_group_id][license_type]['licenses']
        # to context.resources[user_group_id][license_type]['used_licenses']
        while res_license_type['licenses'].count(machine['keystring']) > 0:
            res_license_type['licenses'].remove(machine['keystring'])
        res_license_type['used_licenses'].append(machine['keystring'])

        # change the context.licenses[license_type] to new unused license
        if len(res_license_type['licenses']) > 0:
            context.licenses[license_type] = res_license_type['licenses'][0]
        else:
            context.licenses[license_type] = None

# get context.machine_id
@then('I use odin to query this machine by id')
def step_impl(context):
    wsdl_api = "%s/machine/service.wsdl" % context.wsdl_api_prefix

    # check context properties

    if not hasattr(context, 'machine_id') or \
            not hasattr(context, 'machines') or \
            context.machine_id not in context.machines:
        raise ValueError("No valid machine has been created before!")
    # context.should.have.property('machine_id')
    # context.should.have.property('machines').being.have.key(context.machine_id)
    user_id = context.machines[context.machine_id]['user_id']
    # context.should.have.property('users').being.have.key(user_id)
    if not hasattr(context, 'users') or \
            user_id not in context.users:
        raise ValueError("No valid user has been created before!")
    user_group_id = context.users[user_id]['user_group_id']
    # context.should.have.property('user_groups').being.have.key(user_group_id)
    if not hasattr(context, 'user_groups') or \
            user_group_id not in context.user_groups:
        raise ValueError("No valid user_group has been created before!")

    # compose the request_body
    request_body = {
        'api_key': api_key,
        'id': context.machine_id
    }

    # send SOAP request to get machine
    response = OdinHelper(
        odin_host, wsdl_api,
        testcase=context.tc.name).get(request_body)

    # print('Get machine %s response: %s' % (context.machine_id, response))

    # check if align with context.machines[context.machine_id]
    response.should.have.key('size').being.equal(1L)
    response.should.have.key('results').being.have.length_of(1)
    actual_machine_info = response['results'][0]
    expected_machine_info = context.machines[context.machine_id]
    actual_machine_info.should.have.key(
        'status').being.equal('active')
    actual_machine_info.should.have.key(
        'user_id').being.equal(expected_machine_info['user_id'])
    actual_machine_info.should.have.key(
        'external_id').being.equal(expected_machine_info['external_id'])
    actual_machine_info.should.have.key(
        'keystring').being.equal(expected_machine_info['keystring'])
    actual_machine_info.should.have.key(
        'user_id').being.equal(expected_machine_info['user_id'])
    if expected_machine_info['alias'] is None:
        actual_machine_info.should.have.key('alias').being.equal('N/A')
    else:
        actual_machine_info.should.have.key(
            'alias').being.equal(expected_machine_info['alias'])
    actual_machine_info.should.have.key(
        'quota').being.equal(expected_machine_info['quota_desired'])
    actual_machine_info.should.have.key('id').being.equal(context.machine_id)

# delete context.machine_id
@then('I use odin to delete this machine by id')
def step_impl(context):
    wsdl_api = "%s/machine/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    # context.should.have.property('machine_id')
    # context.should.have.property('machines').being.have.key(context.machine_id)
    if not hasattr(context, 'machine_id') or \
            not hasattr(context, 'machines') or \
            context.machine_id not in context.machines:
        raise ValueError("No valid machine has been created before!")
    user_id = context.machines[context.machine_id]['user_id']
    # context.should.have.property('users').being.have.key(user_id)
    if not hasattr(context, 'users') or \
            user_id not in context.users:
        raise ValueError("No valid user has been created before!")
    user_group_id = context.users[user_id]['user_group_id']
    # context.should.have.property('resources').being.have.key(user_group_id)
    if not hasattr(context, 'resources') or \
            user_group_id not in context.resources:
        raise ValueError("No valid user_group has been created before!")
    user_group_resources = context.resources[user_group_id]

    # compose the request_body
    request_body = {
        'api_key': api_key,
        'id': context.machine_id
    }

    # send SOAP request to delete machine
    response = OdinHelper(
        odin_host, wsdl_api,
        testcase=context.tc.name).delete(request_body)

    # print('Delete machine %s response: %s' % (context.machine_id, response))

    # check if have deleted 1 machine
    response.should.be.equal(1L)

    # return license to context
    license = context.machines[context.machine_id]['keystring']
    if 'Desktop' in user_group_resources and \
            'used_licenses' in user_group_resources['Desktop'] and \
            'licenses' in user_group_resources['Desktop'] and \
            license in user_group_resources['Desktop']['used_licenses']:
        user_group_resources['Desktop']['used_licenses'].remove(license)
        user_group_resources['Desktop']['licenses'].append(license)
        context.licenses['Desktop'] = license
    elif 'Server' in user_group_resources and \
            'used_licenses' in user_group_resources['Server'] and \
            'licenses' in user_group_resources['Server'] and \
            license in user_group_resources['Server']['used_licenses']:
        user_group_resources['Server']['used_licenses'].remove(license)
        user_group_resources['Server']['licenses'].append(license)
        context.licenses['Server'] = license
    else:
        raise ValueError("Keystring cannot be found!")
    # remove context.machine_id from context
    context.machines.pop(context.machine_id)
    # select new context.machine_id
    context.machine_id = None
    for machine_id in context.machines:
        if context.machines[machine_id]['user_id'] == context.user_id:
            context.machine_id = machine_id
            break

# delete context.user_id
@then('I use odin to delete this user by id')
def step_impl(context):
    wsdl_api = "%s/user/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    # context.should.have.property('user_id')
    # context.should.have.property('users').being.have.key(context.user_id)
    if not hasattr(context, 'user_id') or \
            not hasattr(context, 'users') or \
            context.user_id not in context.users:
        raise ValueError("No valid user has been created before!")

    # compose the request_body
    request_body = {
        'api_key': api_key,
        'id': context.user_id
    }

    # send SOAP request to delete user
    response = OdinHelper(
        odin_host, wsdl_api,
        testcase=context.tc.name).delete(request_body)

    # print('Delete user %s response: %s' % (context.user_id, response))

    # check if have deleted 1 user
    response.should.be.equal(1L)

    # remove context.user_id from context
    context.users.pop(context.user_id)
    context.user_id = None
    # select new context.user_id
    for user_id in context.users:
        if context.users[user_id]['user_group_id'] == context.user_group_id:
            context.user_id = user_id
            break

# delete context.admin_id
@then('I use odin to delete this admin by id')
def step_impl(context):
    wsdl_api = "%s/admin/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    # context.should.have.property('admin_id')
    # context.should.have.property('admins').being.have.key(context.admin_id)
    if not hasattr(context, 'admin_id') or \
            not hasattr(context, 'admins') or \
            context.admin_id not in context.admins:
        raise ValueError("No valid admin has been created before!")

    # compose the request_body
    request_body = {
        'api_key': api_key,
        'id': context.admin_id
    }

    # send SOAP request to delete admin
    response = OdinHelper(
        odin_host, wsdl_api,
        testcase=context.tc.name).delete(request_body)

    # print('Delete admin %s response: %s' % (context.admin_id, response))

    # check if have deleted 1 admin
    response.should.be.equal(1L)

    # remove context.admin_id from context
    context.admins.pop(context.admin_id)
    context.admin_id = None
    # select new context.admin_id
    for admin_id in context.admins:
        if context.admins[admin_id]['partner_id'] == context.partner_id:
            context.admin_id = admin_id
            break

# delete context.user_group_id
@then('I use odin to delete this user_group by id')
def step_impl(context):
    wsdl_api = "%s/user_group/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    # context.should.have.property('user_group_id')
    # context.should.have.property(
    #     'user_groups').being.have.key(context.user_group_id)
    if not hasattr(context, 'user_group_id') or \
            not hasattr(context, 'user_groups') or \
            context.user_group_id not in context.user_groups:
        raise ValueError("No valid user_group has been created before!")

    # compose the request_body
    request_body = {
        'api_key': api_key,
        'id': context.user_group_id
    }

    # send SOAP request to delete user_group
    response = OdinHelper(
        odin_host, wsdl_api,
        testcase=context.tc.name).delete(request_body)

    # print('Delete user_group %s response: %s' % (
        # context.user_group_id, response))

    # check if have deleted 1 user_group
    response.should.be.equal(1L)

    # TODO: if need release resources first
    # delete resources from context
    if hasattr(context, 'resources') and \
            context.user_group_id in context.resources:
        context.resources.pop(context.user_group_id)
    # remove context.user_group_id from context
    context.user_groups.pop(context.user_group_id)
    context.user_group_id = None
    # select new context.user_group_id
    for user_group_id in context.user_groups:
        if context.user_groups[user_group_id]['partner_id'] == context.partner_id:
            context.user_group_id = user_group_id
            break

# delete context.partner_id
@then('I use odin to delete this partner by id')
def step_impl(context):
    wsdl_api = "%s/partner/service.wsdl" % context.wsdl_api_prefix

    # check context properties
    # context.should.have.property('partner_id')
    # context.should.have.property('partners').being.have.key(context.partner_id)
    if not hasattr(context, 'partner_id') or \
            not hasattr(context, 'partners') or \
            context.partner_id not in context.partners:
        raise ValueError("No valid partner has been created before!")

    # compose the request_body
    request_body = {
        'api_key': api_key,
        'id': context.partner_id
    }

    # send SOAP request to delete partner
    response = OdinHelper(
        odin_host, wsdl_api,
        testcase=context.tc.name).delete(request_body)

    # print('Delete partner %s response: %s' % (context.partner_id, response))

    # check if have deleted 1 partner
    response.should.be.equal(1L)

    # remove context.partner_id from context
    context.partners.pop(context.partner_id)
    # select new context.partner_id
    if len(context.partners) > 0:
        context.partner_id = context.partners[context.partners.keys()[0]]
    else:
        context.partner_id = None

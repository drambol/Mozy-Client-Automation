import os, datetime, sys
from behave import *
from lib.loghelper import LogHelper

@given('I want to do some as pre-condition')
def step_impl(context):
    pass

@when('I want to generate some logs as information level "{text}"')
def step_impl(context, text):
    LogHelper.info(text)

@then('I want to generate some logs as debug level "{text}"')
def step_impl(context, text):
    LogHelper.debug(text)

@then('I want to generate some logs as warning level "{text}"')
def step_impl(context, text):
    LogHelper.warning(text)

@then('I want to generate some logs as error level "{text}"')
def step_impl(context, text):
    LogHelper.error(text)

@then('I want to generate some logs as critical level "{text}"')
def step_impl(context, text):
    LogHelper.critical(text)
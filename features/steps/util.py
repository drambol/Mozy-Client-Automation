from behave import *
import time, datetime

from lib.loghelper import LogHelper
from lib.kpi import KPI


@When('I wait {wait_time} seconds')
def step_impl(context, wait_time):
    time.sleep(int(wait_time))

@Given('I write "{message}" to log file')
def step_impl(context, message):
    LogHelper.info(message)

@When('I log {category} "{kpiname}" KPI {action} time')
def step_impl(context, category, kpiname, action):
    if category.upper()=="WINDOWS":
        category = "Windows"
    elif category.upper()=="LINUX":
        category = "Linux"
    elif category.upper()=="MAC":
        category = "Mac"
    elif category.upper()=="WEB":
        category = "Web"

    if action.upper() == "START":
        kpi = KPI(testcase=context.tc.name, category=category,
                  start_time=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                  name=kpiname, result="Fail")
        context.kpi = kpi

    elif action.upper() == "END":
        context.kpi.end_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        context.kpi.result = "SUCCESS"

        if context.senddb:
            context.kpi.write_to_elasticsearch()
            context.kpi = None
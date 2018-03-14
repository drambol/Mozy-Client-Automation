import unittest
import os
from time import strftime, gmtime

from lib.platformhelper import PlatformHelper
from lib.testrun import TestRun
from lib.testcase import TestCase
from lib.kpi import KPI

class TestKPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.start_time = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
        cls.hostname = PlatformHelper.get_hostname()
        cls.ip = PlatformHelper.get_ip_address()

        cls.tr_id = "Test_Run"
        cls.tr = TestRun(cls.tr_id, cls.start_time, qa_env="QA12",
                     build=123, client="Windows",
                     oem="MozyEnterprise",
                     runby="clientqaautomation@emc.com")
        cls.tr.save_to_elasticsearch()

        cls.tc_id = "KAL-A"
        cls.tc = TestCase(testrun=cls.tr.name,
                      start_time=cls.start_time, hostname=cls.hostname,
                      product="mozypro",
                      ip=cls.ip,
                      tags=["smoke", "activate", "windows", "keyless"],
                      _id=cls.tc_id,
                      build="111")
        result = cls.tc.write_to_elasticsearch()

    def test_writekpitoes(self):
        kpi = KPI(testcase=self.tc.name, category="service", name="/auth",
                  apimethod="GET", apicode=200, result="OK")
        result = kpi.write_to_elasticsearch()
        print result
        kpi = KPI(testcase=self.tc.name, category="service", name="/sync",
                  apimethod="GET", apicode=304, result="Not Modified")
        result = kpi.write_to_elasticsearch()
        print result
        kpi = KPI(testcase=self.tc.name, category="service",
                  name="/get_config", apimethod="GET", apicode=200, result="OK")
        result = kpi.write_to_elasticsearch()
        print result
        kpi = KPI(testcase=self.tc.name, category="service",
                  name="/machine_get_info", apimethod="GET", apicode=200,
                  result="OK")
        result = kpi.write_to_elasticsearch()
        print result
        kpi = KPI(testcase=self.tc.name, category="client",
                  name="backup", result="Pass")
        result = kpi.write_to_elasticsearch()
        print result
        kpi = KPI(testcase=self.tc.name, category="client",
                  name="restore", result="Fail")
        result = kpi.write_to_elasticsearch()


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestKPI())
    runner = unittest.TextTestRunner()
    runner.run(suite)
import unittest
import os
import datetime
from lib.loghelper import LogHelper
from configuration.global_config_loader import GLOBAL_CONFIG

class TestLog(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.lh = LogHelper()
        time = str(datetime.datetime.now()).split(".")[0].replace("-", "").replace(" ", "_").replace(":", "")
        GLOBAL_CONFIG["Logfile"] = os.path.basename(__file__).replace(".py", "") + "_" + time

    def test123(self):
        self.lh.info("This is an info log")
        self.lh.debug("This is a debug log")
        self.lh.error("This is a error log")

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestLog("test123"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
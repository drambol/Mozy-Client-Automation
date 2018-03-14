"""
this script is used to load all the modules that nessassary to Mozy Client Automation
"""

import os
import sys


lib_module = os.path.abspath('{}{}'.format(os.path.dirname(__file__), "/.."))
sys.path += [lib_module]



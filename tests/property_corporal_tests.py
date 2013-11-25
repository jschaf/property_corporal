from nose.tools import *
from property_corporal import consolidated_propery_list as cpl

import property_corporal

def setup():
    pass

def teardown():
    pass

def test_basic():
    cpl.parse_file("tests/cpl.xls")
    print("I ran!")

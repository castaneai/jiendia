# -*- coding: utf8 -*-
import pprint
import unittest
from jiendia.io.tbl import TblArchive, ArchiveMode

class Test(unittest.TestCase):

    def test_tbl(self):
        with TblArchive('data/WEAPON_SPECIAL.TBL', ArchiveMode.READ, 'cp932') as tbl:
            for group in tbl.groups:
                pprint.pprint(group)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
# -*- coding: utf8 -*-
import pprint
import unittest
from jiendia.io.seq import SeqArchive, ArchiveMode

class Test(unittest.TestCase):

    def test_read(self):
        with SeqArchive('data/010_01_01_STAND_R.SEQ', ArchiveMode.READ, 'cp932') as seq:
            self.assertGreater(len(seq.frames), 0)
            pprint.pprint(seq.frames)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
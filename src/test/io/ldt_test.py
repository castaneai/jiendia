# -*- coding: utf8 -*-
import os.path
from jiendia.io.ldt import LdtArchive, ArchiveMode
from pprint import pprint

def test_read():
    data_dir = os.path.dirname(__file__) + '/data'
    with LdtArchive(data_dir + '/ACTION_INTERFACE.LDT', ArchiveMode.READ, 'cp932') as ldt:
        for row in ldt.rows:
            pprint(row)
        assert 0
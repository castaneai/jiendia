# -*- coding: utf8 -*-
import os
import pprint
import jiendia.io

def test_open():
    data_dir = os.path.dirname(__file__) + '/data'
    with jiendia.io.open_archive(data_dir + '/WEAPON_SPECIAL.TBL') as tbl:
        for group in tbl.groups:
            pprint.pprint(group)
    assert 0

# -*- coding: utf8 -*-
import os.path
import pprint
from jiendia.io.tbl import TblArchive, ArchiveMode

def test_tbl():
    data_dir = os.path.dirname(__file__) + '/data'
    with TblArchive(data_dir + '/WEAPON_SPECIAL.TBL', ArchiveMode.READ, 'cp932') as tbl:
        pprint.pprint(tbl.rectangle(80402801))
        item_ids = [group.item_id for group in tbl.groups]
        assert len(item_ids) == len(set(item_ids))

# -*- coding: utf8 -*-
from jiendia.test.io import DATA_DIR

def test_tbl():
    from jiendia.io.tbl import TblArchive
    with TblArchive(DATA_DIR + '/WEAPON_SPECIAL.TBL', encoding = 'cp932') as tbl:
        item_ids = [group.item_id for group in tbl.groups.values()]
        assert len(item_ids) == len(set(item_ids))
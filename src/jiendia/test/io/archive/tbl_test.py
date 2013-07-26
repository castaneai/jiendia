# -*- coding: utf8 -*-
from jiendia.test.io import DATA_DIR

def test_tbl():
    from jiendia.io.archive.tbl import TblArchive
    with TblArchive(DATA_DIR + '/WEAPON_SPECIAL.TBL', encoding = 'cp932') as tbl:
        assert len(tbl.images) > 0

# -*- coding: utf8 -*-
from jiendia.test.io import DATA_DIR

def test_open():
    '''拡張子に応じて開かれるアーカイブの種類を自動的に選択してくれるopen_archiveをテストする'''
    from jiendia.io import open_archive

    from jiendia.io.tbl import Rectangle, RectangleGroup
    with open_archive(DATA_DIR + '/WEAPON_SPECIAL.TBL') as tbl:
        group = tbl.groups[80102401]
        assert isinstance(group, RectangleGroup)

    from jiendia.io.spf import SpfArchive, SpfArchiveEntry
    with open_archive(DATA_DIR + '/CLAIRE.SPF') as spf:
        assert isinstance(spf, SpfArchive)
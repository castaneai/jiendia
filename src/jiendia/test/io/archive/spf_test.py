# -*- coding: utf8 -*-
from jiendia.test.io import DATA_DIR

def test_open():
    u"""SPFアーカイブの中に入っているファイルを認識できているかテストする"""
    from jiendia.io.archive.spf import SpfArchive, SpfArchiveEntry
    with SpfArchive(DATA_DIR + '/CLAIRE.SPF', encoding = 'cp932') as spf:
        assert isinstance(spf.get_entry('DATA/LOGO/LOGO_01.PNG'), SpfArchiveEntry)

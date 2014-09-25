# -*- coding: utf-8 -*-
from jiendia.test import DATA_DIR
from jiendia.spf import SpfArchive


def test_open():
    spf = SpfArchive(DATA_DIR + "/CLAIRE.SPF")
    assert spf.contain_files is not None


def test_open():
    u"""SPFアーカイブの中に入っているファイルを認識できているかテストする"""
    from jiendia.spf import SpfArchive, SpfArchiveEntry
    with SpfArchive(DATA_DIR + '/CLAIRE.SPF', encoding = 'cp932') as spf:
        assert isinstance(spf.get_entry('DATA/LOGO/LOGO_01.PNG'), SpfArchiveEntry)

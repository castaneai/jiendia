# -*- coding: utf8 -*-
from jiendia.test.io import DATA_DIR

def test_read():
    u"""LDTアーカイブの内容を読み取れるかテストする"""
    from jiendia.io.archive.ldt import LdtArchive
    with LdtArchive(DATA_DIR + '/ACTION_INTERFACE.LDT', encoding = 'cp932') as ldt:
        first_row = ldt.rows[0]
        assert first_row['ID'] == 1
        assert first_row['_Name'] == '待機'

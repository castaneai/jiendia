# -*- coding: utf8 -*-
from jiendia.test.io import DATA_DIR

def test_create():
    '''SPFアーカイブファイルの作成をテストする'''

    from jiendia.io import ArchiveMode
    from jiendia.io.spf import SpfArchive
    with SpfArchive(DATA_DIR + '/create_test.spf', mode = ArchiveMode.CREATE, encoding = 'cp932',
            version = 20130106,
            archive_number = 0xff) as spf:
        assert len(spf.entries) == 0
        spf.create_entry('entry_test.txt')
        spf.create_entry('path/to/entry_test2.txt')

    with SpfArchive(DATA_DIR + '/create_test.spf', mode = ArchiveMode.READ, encoding = 'cp932') as spf:
        assert spf.version == 20130106
        assert spf.archive_number == 0xff
        assert spf.get_entry('entry_test.txt') is not None
        assert spf.get_entry('path/to/entry_test2.txt') is not None

def test_open():
    '''SPFアーカイブの中に入っている別種類のアーカイブを開くことができるかテストする'''
    
    from jiendia.io import ArchiveMode
    from jiendia.io.spf import SpfArchive
    with SpfArchive(DATA_DIR + '/create_test.spf', mode = ArchiveMode.CREATE, encoding = 'cp932',
            version = 20130315,
            archive_number = 0xff) as spf:
        spf.create_entry_from_file('010_01_01_STAND_R.SEQ', DATA_DIR + '/010_01_01_STAND_R.SEQ')
        spf.create_entry_from_file('ACTION_INTERFACE.LDT', DATA_DIR + '/ACTION_INTERFACE.LDT')
        
    from jiendia.io.seq import SeqArchive
    from jiendia.io.ldt import LdtArchive
    with SpfArchive(DATA_DIR + '/create_test.spf', mode = ArchiveMode.READ, encoding = 'cp932') as spf:
        with spf.open_entry('010_01_01_STAND_R.SEQ') as seq:
            assert type(seq) == SeqArchive
        with spf.open_entry('ACTION_INTERFACE.LDT') as ldt:
            assert type(ldt) == LdtArchive
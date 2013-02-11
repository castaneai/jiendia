# -*- coding: utf8 -*-
import os.path
from jiendia.io.spf import SpfArchive, ArchiveMode

def test_create():
    '''SPFアーカイブファイルの作成をテストする'''

    data_dir = os.path.dirname(__file__) + '/data'

    with SpfArchive(data_dir + '/create_test.spf', ArchiveMode.CREATE, 'cp932', version = 20130106, archive_number = 0xff) as spf:
        assert len(spf.entries) == 0
        spf.create_entry('entry_test.txt')
        spf.create_entry('path/to/entry_test2.txt')


    with SpfArchive(data_dir + '/create_test.spf', ArchiveMode.READ, 'cp932') as spf:
        assert spf.version == 20130106
        assert spf.archive_number == 0xff
        assert spf.entries[0].entry_name == 'entry_test.txt'
        assert spf.entries[1].entry_name == 'path/to/entry_test2.txt'

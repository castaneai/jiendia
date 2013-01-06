# -*- coding: utf8 -*-
import unittest
from jiendia.io.spf_archive import SpfArchiveFile, SpfArchiveMode

class Test(unittest.TestCase):

    def test_create(self):
        '''SPFアーカイブファイルの作成をテストする'''
        with SpfArchiveFile('create_test.spf', SpfArchiveMode.CREATE, 'cp932',
            version = 20130106, archive_number = 0xff) as spf:
            self.assertEqual(len(spf.entries), 0)
            spf.create_entry('entry_test.txt')
            spf.create_entry('path/to/entry_test2.txt')
            
        with SpfArchiveFile('create_test.spf', SpfArchiveMode.READ, 'cp932') as spf:
            self.assertEqual(spf.version, 20130106)
            self.assertEqual(spf.archive_number, 0xff)
            self.assertEqual(spf.entries[0].entry_name, 'entry_test.txt')
            self.assertEqual(spf.entries[1].entry_name, 'path/to/entry_test2.txt')

if __name__ == "__main__":
    unittest.main()
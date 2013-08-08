# -*- coding: utf-8 -*-
import os
import re
import ldt2sqlite
from jiendia.io.archive.spf import SpfArchive

def check_ext(filename, ext):
    u"""指定したファイル名が拡張子extであるかどうか調べる
    大小文字の違いは関係なく判定される"""
    pattern = '.*\.{0}$'.format(ext)
    return re.match(pattern, filename, re.IGNORECASE) is not None

def spf2sqlite(spf_file, sqlite_file):
    u"""LDTテーブルを含むSPFファイルをSQLiteデータベースファイルに書き込む"""
    with SpfArchive(spf_file) as spf:
        ldt_entry_names = [entry.name for entry in spf.entries if check_ext(entry.name, 'ldt')]
        for ldt_entry_name in ldt_entry_names:
            ldt_file = spf.open_entry(ldt_entry_name)
            table_name = os.path.basename(ldt_entry_name).split('.')[0]
            ldt2sqlite.ldt2sqlite(ldt_file, sqlite_file, table_name)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print(u'Usage: spf2sqlite.py <source SPF file> <dest SQLite file>')
        exit()
    src_spf_file = sys.argv[1]
    dst_sqlite_file = sys.argv[2]
    spf2sqlite(src_spf_file, dst_sqlite_file)
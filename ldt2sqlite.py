# -*- coding: utf-8 -*-
import sys
import os.path
import sqlite3
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + u'/src'))

from jiendia.io.archive.ldt import LdtArchive

def create_str_row(row, columns):
    from jiendia.io.archive.ldt import ColumnType
    result = []
    for val, col in zip(row, columns):
        if col.type == ColumnType.STRING:
            result.append(u"'{0}'".format(str(val).replace(u"'", u"''")))
        else:
            result.append(u'{0}'.format(val))
    return result

def ldt2sqlite(src_file, dst_file):
    table_name = os.path.basename(src_file).split('.')[0]
    with LdtArchive(src_file, encoding = 'cp932') as ldt:
        with sqlite3.connect(dst_file) as conn:
            conn.execute(u'drop table if exists `{0}`'.format(table_name))
            query = u'create table `{0}`({1})'.format(
                table_name,
                u','.join([u'`{0}`'.format(col.name) for col in ldt.columns])
            )
            conn.execute(query)

            for row in ldt.rows:
                query = u'insert into `{0}` values({1})'.format(
                    table_name,
                    ','.join(create_str_row(row, ldt.columns))
                )
                conn.execute(query)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print(u"Usage: python ldt2sqlite.py <source LDT file> <dest SQLite file>")
        exit()
    ldt2sqlite(sys.argv[1], sys.argv[2])

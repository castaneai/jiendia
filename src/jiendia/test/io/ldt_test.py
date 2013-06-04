# -*- coding: utf8 -*-
from jiendia.test.io import DATA_DIR

def test_read():
    '''LDTアーカイブの内容を読み取れるかテストする'''
    from jiendia.io.ldt import LdtArchive
    with LdtArchive(DATA_DIR + '/ACTION_INTERFACE.LDT', encoding = 'cp932') as ldt:
        first_row = ldt.rows[0]
        assert first_row['ID'] == 1
        assert first_row['Name'] == '待機'
        
def test_sql_export():
    import sqlite3
    from jiendia.io.ldt import LdtArchive
    from jiendia.sql.ldt import ldt2sql
    with LdtArchive(DATA_DIR + '/ACTION_INTERFACE.LDT', encoding = 'cp932') as ldt:
        with sqlite3.connect(DATA_DIR + '/action_interface.sqlite') as conn:
            ldt2sql('action_interface', ldt, conn)

    with sqlite3.connect(DATA_DIR + '/action_interface.sqlite') as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute('select * from action_interface limit 1').fetchone()
        assert row['ID'] == 1
        assert row['Name'] == '待機'

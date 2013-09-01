# -*- coding: utf-8 -*-
import sqlite3
import tempfile
from jiendia.util import get_latale_dir
from jiendia.io.archive.spf import SpfArchive
from jiendia.io.archive.ldt import LdtArchive

def get_ldt(ldt_name):
    with SpfArchive(get_latale_dir() + '/ROWID.SPF') as spf:
        ldt_file = spf.open_entry('DATA/LDT/{0}.LDT')
        return LdtArchive(ldt_file)

def get_sqlite_from_ldt(ldt):
    temp_file = tempfile.NamedTemporaryFile()
    return sqlite3.connect(temp_file.name)

def get_valid_tree_id_list(row):
    invalid_tree_id_list = [
        0, # none tree id
        101,
        450,
        451,
        460,
        501,
        503, # グランシンフォニアの音符別演奏
        601,
        602,
        603,
        604,
        605
    ]
    return [int(value) for value in row if int(value) not in invalid_tree_id_list]

def get_skill_tree_id_list(classId, rowid_sqlite):
    u"""指定した職業が持っているスキルツリーのIDリストを返す"""
    select_columns = ['_SubID{0}'.format(i) for i in range(1, 11)]
    query = 'select {0} from SKILL_MAIN_MENU where _Class = {1}'.format(','.join(select_columns), classId)

    skill_tree_id_list = []
    for row in rowid_sqlite.execute(query):
        skill_tree_id_list = skill_tree_id_list + get_valid_tree_id_list(row)
    return skill_tree_id_list

def get_skill_tree_skills(skill_tree_id, rowid_sqlite):
    query = '''
    select
        SKILL.ID,
        SKILL._BaseSlv,
        SKILL._MaxSlv,
        SKILL._GetSkillLv,
        SKILL._GetSkillID,
        SKILL._UpRequireSkillPoint,
        SKILL._UpRequireSkillPointSlv,
        SKILL._UpRequire1_Type,
        SKILL._UpRequire1_ID,
        SKILL._UpRequire1_Value1,
        SKILL._UpRequire1_ValueSlv1,
        SKILL._UpRequire1_Value2,
        SKILL._UpRequire1_ValueSlv2,
        SKILL._UpRequire2_Type,
        SKILL._UpRequire2_ID,
        SKILL._UpRequire2_Value1,
        SKILL._UpRequire2_ValueSlv1,
        SKILL._UpRequire2_Value2,
        SKILL._UpRequire2_ValueSlv2,
        SKILL._Icon,
        SKILL._IconIndex,
        SKILL._Learn_Skill,
        SKILL_TXT._Name,
        SKILL_TXT._Description,
        SKILL_CONTENT._Grid_Index,
        LEARN_SKILL._Require1_Type,
        LEARN_SKILL._Require1_ID,
        LEARN_SKILL._Require1_Value1,
        LEARN_SKILL._Require1_Value2,
        LEARN_SKILL._Require2_Type,
        LEARN_SKILL._Require2_ID,
        LEARN_SKILL._Require2_Value1,
        LEARN_SKILL._Require2_Value2,
        LEARN_SKILL._Require3_Type,
        LEARN_SKILL._Require3_ID,
        LEARN_SKILL._Require3_Value1,
        LEARN_SKILL._Require3_Value2,
        LEARN_SKILL._Require4_Type,
        LEARN_SKILL._Require4_ID,
        LEARN_SKILL._Require4_Value1,
        LEARN_SKILL._Require4_Value2,
        LEARN_SKILL._Require5_Type,
        LEARN_SKILL._Require5_ID,
        LEARN_SKILL._Require5_Value1,
        LEARN_SKILL._Require5_Value2,
        LEARN_SKILL._Require6_Type,
        LEARN_SKILL._Require6_ID,
        LEARN_SKILL._Require6_Value1,
        LEARN_SKILL._Require6_Value2,
        LEARN_SKILL._Require7_Type,
        LEARN_SKILL._Require7_ID,
        LEARN_SKILL._Require7_Value1,
        LEARN_SKILL._Require7_Value2,
        LEARN_SKILL._Require8_Type,
        LEARN_SKILL._Require8_ID,
        LEARN_SKILL._Require8_Value1,
        LEARN_SKILL._Require8_Value2
    from SKILL_CONTENT
    left join SKILL on SKILL_CONTENT._SkillID = SKILL.ID
    left join SKILL_TXT on SKILL_CONTENT._SkillID = SKILL_TXT.ID
    left join LEARN_SKILL on SKILL_CONTENT._SkillID = LEARN_SKILL.ID
     where SKILL_CONTENT._SkillID > 0 and
     SKILL_CONTENT._SubID = {0}'''.format(skill_tree_id)
    rowid_sqlite.row_factory = sqlite3.Row
    skills = []
    for row in rowid_sqlite.execute(query):
        skills.append(dict(row))
    return skills

def get_special_tree_names():
    return {
        226: 'スパイラルソードスキル',
        1226: '短剣スキル',
        2226: '短剣スキル',
        227: '飛燕剣スキル',
        228: 'ガントレットスキル',
        229: 'サイキックスキル',
        230: 'バトルサイズスキル',
        231: 'タクトスキル',
        232: 'ローグナイフスキル',
        233: 'ガンブレイドスキル',
        234: 'ガーディアンスキル',
        424: 'ハイランダー専門スキル',
        425: 'ソードダンサー専門スキル',
        426: 'ダークナイト専門スキル',
        427: 'サイキッカー専門スキル',
        428: 'ファントムメイジ専門スキル',
        429: 'マエストロ専門スキル',
        430: 'ローグマスター専門スキル',
        431: 'ジャッジメント専門スキル',
        432: 'スターシーカー専門スキル',
        2736: '特性スキル',
        2737: '特性スキル',
        2738: '特性スキル',
        2739: '特性スキル',
        2740: '特性スキル',
        2741: '特性スキル',
        2742: '特性スキル',
        2743: '特性スキル',
        2744: '特性スキル',
        2745: '特性スキル',
    }

def get_skill_tree_name(tree_id, sqlite):
    if tree_id in get_special_tree_names():
        return get_special_tree_names()[tree_id]
    query = 'select _Name from UI_TOOLTIP where ID = {0}'.format(805780120 + tree_id)
    name_row = sqlite.execute(query).fetchone()
    if name_row is not None:
        return name_row[0]
    if tree_id < 1000:
        return '???'
    tree_id -= 1000;
    query = 'select _Name from UI_TOOLTIP where ID = {0}'.format(805780120 + tree_id)
    name_row = sqlite.execute(query).fetchone()
    if name_row is not None:
        return name_row[0]
    return '???'

def get_skill_tree(skill_tree_id, rowid_sqlite):
    name = get_skill_tree_name(skill_tree_id, rowid_sqlite)
    print('id: {0}, name: {1}'.format(skill_tree_id, name))
    return {
        'id': skill_tree_id,
        'name': name,
        'skills': get_skill_tree_skills(skill_tree_id, rowid_sqlite)
    }

def get_skill_trees(classId, rowid_sqlite):
    trees = []
    for skill_tree_id in get_skill_tree_id_list(classId, rowid_sqlite):
        trees.append(get_skill_tree(skill_tree_id, rowid_sqlite))
    return trees

def dump_skills(classId, rowid_sqlite):
    import json
    with open('{0}.json'.format(classId), 'w') as file:
        skill_trees = get_skill_trees(classId, rowid_sqlite)
        json.dump(skill_trees, file)

if __name__ == '__main__':
    import sys
    import json
    if len(sys.argv) < 2:
        print('Usage: skill_data.py <ROWID sqlite file path>')
        exit()
    rowid_db_path = sys.argv[1]
    with sqlite3.connect(rowid_db_path) as conn:
        if len(sys.argv) == 3:
            classId = int(sys.argv[2])
            dump_skills(classId, conn)
        else:
            for classId in range(0, 46):
                dump_skills(classId, conn)

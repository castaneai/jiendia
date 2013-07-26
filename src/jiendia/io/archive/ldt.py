# -*- coding: utf8 -*-
import io
from jiendia.io.manipulator import BinaryReader
from jiendia.io.archive.base import BaseArchive, ArchiveMode

class ColumnType:
    UNSIGNED_INT = 0
    STRING = 1
    BOOL = 2
    INT = 3
    FLOAT = 4
    
class Column:
    
    def __init__(self, name, type):
        self._name = name
        self._type = type
        
    @property
    def name(self):
        return self._name
    
    @property
    def type(self):
        return self._type
    
    @property
    def type_str(self):
        if self._type == ColumnType.UNSIGNED_INT:
            return 'unsigned int'
        elif self._type == ColumnType.STRING:
            return 'string'
        elif self._type == ColumnType.BOOL:
            return 'bool'
        elif self._type == ColumnType.INT:
            return 'int'
        elif self._type == ColumnType.FLOAT:
            return 'float'

class LdtArchive(BaseArchive):

    _DEFAULT_ENCODING = 'utf-8'

    def __init__(self, file, mode = BaseArchive._DEFAULT_MODE, encoding = _DEFAULT_ENCODING):
        u"""LDTアーカイブを開く
        LDTは文字列データを含むので文字エンコーディングを指定する必要がある
        指定しない場合はデフォルトのUTF-8エンコーディングとなる"""
        BaseArchive.__init__(self, file, mode)
        self._encoding = encoding
        self._columns = []
        self._rows = []
        if mode in (ArchiveMode.READ, ArchiveMode.UPDATE):
            self._load()

    @property
    def columns(self):
        return tuple(self._columns)

    @property
    def rows(self):
        return tuple(self._rows)

    def _load(self):
        reader = BinaryReader(self._stream)
        self._stream.seek(4, io.SEEK_SET)
        column_count = reader.read_int32()
        row_count = reader.read_int32()

        self._load_columns(column_count)
        self._load_rows(row_count)

    def _load_columns(self, column_count):
        u"""ストリームから列情報を読み取ってself._columnsに書き込む"""
        POS_COLUMNNAME = 12
        POS_COLUMNTYPE = 8204
        COLUMN_NAME_LENGTH = 64
        reader = BinaryReader(self._stream)

        # 列の名前を読み取る
        self._stream.seek(POS_COLUMNNAME, io.SEEK_SET)
        column_names = []
        for _ in range(column_count):
            name = reader.read_string(COLUMN_NAME_LENGTH, self._encoding)
            column_names.append(name)

        # 列の型情報を読み取る
        self._stream.seek(POS_COLUMNTYPE, io.SEEK_SET)
        column_types = []
        for _ in range(column_count):
            type = reader.read_int32()
            column_types.append(type)

        self._columns = []
        # IDカラムはバイナリには記述されていないが、先頭に存在する
        id_column = Column('ID', ColumnType.INT)
        self._columns.append(id_column)
        for name, type in zip(column_names, column_types):
            column = Column(name, type)
            self._columns.append(column)

    def _load_rows(self, row_count):
        POS_ROWDATA = 8716
        reader = BinaryReader(self._stream)

        self._stream.seek(POS_ROWDATA, io.SEEK_SET)
        self._rows = []
        for _ in range(row_count):
            row = {}
            for column in self._columns:
                if column.type in (ColumnType.INT, ColumnType.UNSIGNED_INT, ColumnType.BOOL):
                    row[column.name] = reader.read_int32()
                elif column.type == ColumnType.FLOAT:
                    row[column.name] = reader.read_float()
                elif column.type == ColumnType.STRING:
                    str_len = reader.read_short()
                    row[column.name] = reader.read_string(str_len, self._encoding)
                else:
                    raise TypeError('invalid column type: {0}'.format(column.type))
            self._rows.append(row)

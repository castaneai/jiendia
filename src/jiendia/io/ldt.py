# -*- coding: utf8 -*-
import io
import collections
import pybinary.io

from jiendia.io._base import BaseArchive, ArchiveMode

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
    
    def init(self):
        self._rows = []
        self._columns = []
        
    @property
    def rows(self):
        return tuple(self._rows)
    
    @property
    def columns(self):
        return tuple(self._columns)
        
    def load(self):
        DATATYPE_POS = 8204
        ROWDATA_POS = 8716
        COLUMN_NAME_LENGTH = 64
        
        reader = pybinary.io.BinaryReader(self._stream, self._encoding)
        self._stream.seek(4)
        column_count = reader.read_int32()
        row_count = reader.read_int32()
        
        column_names = []
        for _ in range(column_count):
            name = reader.read_string(COLUMN_NAME_LENGTH).lstrip('_').replace('-', '_').replace(' ', '_')
            column_names.append(name)
            
        self._stream.seek(DATATYPE_POS, io.SEEK_SET)
        
        column_types = []
        for _ in range(column_count):
            type = reader.read_int32()
            column_types.append(type)
            
        # IDカラムはバイナリには記述されていないが、先頭に存在する
        id_column = Column('ID', ColumnType.INT)
        self._columns.append(id_column)
        for name, type in zip(column_names, column_types):
            column = Column(name, type)
            self._columns.append(column)
            
        self._stream.seek(ROWDATA_POS, io.SEEK_SET)
        
        Row = collections.namedtuple('Row', ','.join([col.name for col in self.columns]))
        for _ in range(row_count):
            row = []
            for column in self._columns:
                if column.type in (ColumnType.INT, ColumnType.UNSIGNED_INT, ColumnType.BOOL):
                    row.append(reader.read_int32())
                elif column.type == ColumnType.FLOAT:
                    row.append(reader.read_float())
                elif column.type == ColumnType.STRING:
                    str_len = reader.read_short()
                    row.append(reader.read_string(str_len))
                else:
                    raise TypeError('invalid column type: {0}'.format(column.type))
            row = Row._make(row)
            self._rows.append(row)
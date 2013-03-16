# -*- coding: utf8 -*-
import io
import collections
import pybinary.io
from jiendia.io._base import BaseArchive, ArchiveMode

Rectangle = collections.namedtuple('Rectangle',
    'pattern, x, y, axis_x, axis_y, left, top, right, bottom, filename')

RectangleGroup = collections.namedtuple('RectangleGroup',
    'item_id, depth, rectangles')

class TblArchive(BaseArchive):
    
    def init(self):
        if not self._mode == ArchiveMode.READ:
            raise NotImplementedError('TBL Archive only supports READ mode')
        self._groups = {}
        
    @property
    def groups(self):
        return self._groups
        
    def load(self):
        reader = pybinary.io.BinaryReader(self._stream, self._encoding)
        self._stream.seek(4, io.SEEK_SET)
        group_count = reader.read_int32()
        
        for _ in range(group_count):
            rectangle_count = reader.read_int32()
            group_id_str = reader.read_string(16)
            self._stream.seek(116, io.SEEK_CUR)
            item_id = int(''.join(group_id_str.split('_')[1:]))
            depth = int(group_id_str.split('_')[0])
            rectangles = []
            for __ in range(rectangle_count):
                pattern = reader.read_int32()
                x = reader.read_int32()
                y = reader.read_int32()
                axis_x = reader.read_float()
                axis_y = reader.read_float()
                left = reader.read_int32()
                top = reader.read_int32()
                right = reader.read_int32()
                bottom = reader.read_int32()
                filename = reader.read_string(24)
                self._stream.seek(104, io.SEEK_CUR)
                rectangle = Rectangle._make((pattern, x, y, axis_x, axis_y, left, top, right, bottom, filename))
                rectangles.append(rectangle)
        
            group = RectangleGroup._make((item_id, depth, tuple(rectangles)))
            self._groups[item_id] = group

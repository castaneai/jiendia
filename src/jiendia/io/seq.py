# -*- coding: utf8 -*-
import io
import collections
import pybinary.io
from jiendia.io._base import BaseArchive, ArchiveMode

Frame = collections.namedtuple('Frame', 'number, duration, parts')
FramePart = collections.namedtuple('FramePart', 'depth, pattern, rotation, x, y, visible, flip')


class SeqArchive(BaseArchive):
    
    def __init__(self, stream, mode, encoding):
        if not mode == ArchiveMode.READ:
            raise NotImplementedError('SEQ Archive only supports READ mode')
        self._frames = []
        BaseArchive.__init__(self, stream, mode, encoding)
        
    @property
    def frames(self):
        return tuple(self._frames)
        
    def load(self):      
        reader = pybinary.io.BinaryReader(self._stream, self._encoding)
        self._stream.seek(12, io.SEEK_SET)
        frame_count = reader.read_int32()
        
        for _ in range(frame_count):
            number = reader.read_int32()
            duration = reader.read_float()
            part_count = reader.read_int32()
            
            parts = []
            for __ in range(part_count):
                depth = reader.read_int32()
                pattern = reader.read_int32()
                rotation = reader.read_int32()
                x = reader.read_int32()
                y = reader.read_int32()
                visible = reader.read_short()
                flip = reader.read_short()
                part = FramePart._make((depth, pattern, rotation, x, y, visible, flip))
                parts.append(part)
            frame = Frame._make((number, duration, tuple(parts))) 
            self._frames.append(frame)
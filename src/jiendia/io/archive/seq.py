# -*- coding: utf8 -*-
import io
import collections
from jiendia.io.manipulator import BinaryReader
from jiendia.io.archive.base import BaseArchive, ArchiveMode

AnimationFrame = collections.namedtuple('AnimationFrame', 'number, duration, parts')
AnimationFramePart = collections.namedtuple('AnimationFramePart', 'depth, pattern, rotation, x, y, visible, flip')

class SeqArchive(BaseArchive):
    u"""キャラクターのアニメーションのフレームを格納したアーカイブ"""

    def __init__(self, file, mode = BaseArchive._DEFAULT_MODE):
        if mode != ArchiveMode.READ:
            raise NotImplementedError('SEQアーカイブは読み取り専用です')
        BaseArchive.__init__(self, file, mode)
        self._frames = []
        self._load()

    @property
    def frames(self):
        return tuple(self._frames)

    def _load(self):
        reader = BinaryReader(self._stream)
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
                part = AnimationFramePart._make((depth, pattern, rotation, x, y, visible, flip))
                parts.append(part)
            frame = AnimationFrame._make((number, duration, tuple(parts)))
            self._frames.append(frame)

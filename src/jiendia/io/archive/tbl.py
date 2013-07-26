# -*- coding: utf8 -*-
import io
import collections
from jiendia.io.manipulator import BinaryReader
from jiendia.io.archive.base import BaseArchive, ArchiveMode

Rectangle = collections.namedtuple('Rectangle',
    'pattern, x, y, axis_x, axis_y, left, top, right, bottom, filename')

Image = collections.namedtuple('Image',
    'item_id, depth, rectangles')

class TblArchive(BaseArchive):
    u"""キャラクターの体・装備品などの画像情報を格納するアーカイブ"""

    _DEFAULT_ENCODING = 'utf-8'

    def __init__(self, file, mode = BaseArchive._DEFAULT_MODE, encoding = _DEFAULT_ENCODING):
        if mode != ArchiveMode.READ:
            raise RuntimeError('TBLアーカイブは読み取り専用です')
        BaseArchive.__init__(self, file, mode)
        self._encoding = encoding
        self._images = {}
        if mode in (ArchiveMode.READ, ArchiveMode.UPDATE):
            self._load()

    @property
    def images(self):
        return dict(self._images)

    def get_image(self, item_id):
        u"""指定したアイテムIDの画像情報を取得する
        画像情報は{アイテムID, レイヤの深さ, 句形画像リスト}の三要素からなる"""
        return self._images[item_id]
        
    def _load(self):
        reader = BinaryReader(self._stream)
        self._stream.seek(4, io.SEEK_SET)
        group_count = reader.read_int32()
        
        for _ in range(group_count):
            rectangle_count = reader.read_int32()
            group_id_str = reader.read_string(16, self._encoding)
            self._stream.seek(116, io.SEEK_CUR)
            # グループIDが12_3456_78_90ならば先頭の12がレイヤの深さ, 続く34567890がアイテムID
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
                filename = reader.read_string(24, self._encoding)
                self._stream.seek(104, io.SEEK_CUR)
                rectangle = Rectangle._make((pattern, x, y, axis_x, axis_y, left, top, right, bottom, filename))
                rectangles.append(rectangle)
        
            image = Image._make((item_id, depth, tuple(rectangles)))
            self._images[item_id] = image

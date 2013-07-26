# -*- coding: utf8 -*-
import io
from jiendia.io.manipulator import BinaryReader
from jiendia.io.archive.base import BaseArchive, ArchiveMode

class SpfArchive(BaseArchive):
    u"""ファイルを中に格納したパッケージアーカイブ"""

    _DEFAULT_ENCODING = 'utf-8'
    
    def __init__(self, file, mode = BaseArchive._DEFAULT_MODE, encoding = _DEFAULT_ENCODING):
        if mode != ArchiveMode.READ:
            raise RuntimeError(u'SPFアーカイブは読み取り専用です')
        BaseArchive.__init__(self, file, mode)
        self._encoding = encoding
        self._version = -1
        self._archive_number = -1
        self._entries = {}
        if mode in (ArchiveMode.READ, ArchiveMode.UPDATE):
            self._load()

    @property
    def entries(self):
        return self._entries.values()

    def _load(self):
        reader = BinaryReader(self._stream)
        # ファイルの末尾に書かれたバージョン番号、アーカイブ番号を読み取る
        self._stream.seek(-4, io.SEEK_END)
        self._version = reader.read_int32()
        self._stream.seek(-136, io.SEEK_END)
        self._archive_number = reader.read_int32()
        
        self._stream.seek(-140, io.SEEK_END)
        entry_index_len = reader.read_int32()
        self._stream.seek(-1 * (entry_index_len + 4), io.SEEK_CUR)
        entry_count = int(entry_index_len / 140)
        self._entries = {}
        for _ in range(entry_count):
            entry_name = reader.read_string(128, self._encoding)
            entry_start_pos = reader.read_int32()
            entry_length = reader.read_int32()
            self._entries[entry_name] = SpfArchiveEntry(self, entry_name, entry_start_pos, entry_length)
            self._stream.seek(4, io.SEEK_CUR)

    def get_entry(self, entry_name):
        u"""指定した名前のエントリを取得する"""
        return self._entries[entry_name]

    def open_entry(self, entry_name):
        u"""指定した名前のエントリをファイルとして開く"""
        entry = self.get_entry(entry_name)
        entry_stream = io.BytesIO()
        self._stream.seek(entry.start_pos, io.SEEK_SET)
        entry_stream.write(self._stream.read(entry.length))
        return entry_stream

class SpfArchiveEntry(object):
    u"""SPFアーカイブの中に格納されいてる個々のエントリ"""
    
    def __init__(self, archive, entry_name, entry_start_pos, entry_length):
        self._archive = archive
        self._entry_name = entry_name
        self._start_pos = entry_start_pos
        self._length = entry_length

    @property
    def name(self):
        return self._entry_name

    @property
    def start_pos(self):
        return self._start_pos

    @property
    def length(self):
        return self._length

    @property
    def archive(self):
        return self._archive

# -*- coding: utf-8 -*-
import io
from jiendia import DEFAULT_ENCODING
from jiendia.io.manipulator import BinaryReader
from jiendia.io.archive.base import BaseArchive, ArchiveMode


class SpfArchive(BaseArchive):
    """ファイルを中に格納したパッケージアーカイブ"""

    def __init__(self, file, mode=BaseArchive._DEFAULT_MODE, encoding=DEFAULT_ENCODING):
        if mode != ArchiveMode.READ:
            raise RuntimeError(u'SPFアーカイブは読み取り専用です')
        BaseArchive.__init__(self, file, mode)
        # 含まれているファイル名の文字エンコーディング
        self._encoding = encoding
        # SPFバージョン　ログイン時のチェックに使用される
        self._version = None
        # アーカイブ番号, 多くのSPFに割り振られているが，用途は不明
        self._archive_number = None
        # SPFアーカイブは内部のパスがキーとなっているため，辞書にしてある
        # 同じパスのファイルが重複することはない(zipと同じ)
        self._contain_files = {}
        if mode in (ArchiveMode.READ, ArchiveMode.UPDATE):
            self._load()

    @property
    def contain_files(self):
        return self._contain_files.values()

    def _load(self):
        reader = BinaryReader(self._stream)
        # ファイルの末尾に書かれたバージョン番号、アーカイブ番号を読み取る
        self._stream.seek(-4, io.SEEK_END)
        self._version = reader.read_int32()
        self._stream.seek(-136, io.SEEK_END)
        self._archive_number = reader.read_int32()

        # ファイル一覧を読み取る
        self._stream.seek(-140, io.SEEK_END)
        filelist_length = reader.read_int32()
        self._stream.seek(-1 * (filelist_length + 4), io.SEEK_CUR)
        file_count = int(filelist_length / 140)
        self._contain_files = {}
        for _ in range(file_count):
            path = reader.read_string(128, self._encoding)
            start_pos = reader.read_int32()
            length = reader.read_int32()
            self._contain_files[path] = SpfArchivePartFile(self, path, start_pos, length)
            self._stream.seek(4, io.SEEK_CUR)


class SpfArchivePartFile(object):
    """SPFアーカイブの中に格納されいてる個々のファイル"""
    
    def __init__(self, archive, path, start_pos, length):
        self.archive = archive
        self.path = path
        self.start_pos = start_pos
        self.length = length

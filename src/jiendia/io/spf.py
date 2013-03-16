# -*- coding: utf8 -*-
import io
import struct
import contextlib
import jiendia.io.open
from jiendia.io._base import DEFAULT_MODE, DEFAULT_ENCODING, ArchiveMode, BaseArchive

class SpfArchive(BaseArchive):
    
    def __init__(self, stream, mode = DEFAULT_MODE, encoding = DEFAULT_ENCODING, version = None, archive_number = None):
        if mode == ArchiveMode.CREATE:
            if version is None or archive_number is None:
                raise RuntimeError('create mode requires `version` and `archive_number`')
        self.version = version
        self.archive_number = archive_number
        super().__init__(stream, mode, encoding)

    def init(self):
        self._entries_dict = {}

    @property    
    def entries(self):
        return self._entries_dict.values()
            
    def close(self):
        BaseArchive.close(self)
            
    def load(self):
        self._stream.seek(-4, io.SEEK_END)
        self.version = struct.unpack('<l', self._stream.read(4))[0]
        self._stream.seek(-136, io.SEEK_END)
        self.archive_number = struct.unpack('<l', self._stream.read(4))[0]
        
        self._stream.seek(-140, io.SEEK_END)
        entry_index_len = struct.unpack('<l', self._stream.read(4))[0]
        self._stream.seek(-1 * (entry_index_len + 4), io.SEEK_CUR)
        entry_count = int(entry_index_len / 140)
        entry_infos = []
        for _ in range(entry_count):
            entry_name, start_pos, content_len = struct.unpack('<128s2l', self._stream.read(136))
            entry_name = entry_name.split(b'\x00')[0].decode(self._encoding).replace('\\', '/')
            entry_infos.append({
                'name': entry_name,
                'pos': start_pos,
                'len': content_len,
            })
            self._stream.seek(4, io.SEEK_CUR)
        for info in entry_infos:
            self._stream.seek(info['pos'], io.SEEK_SET)
            data = self._stream.read(info['len'])
            entry_stream = io.BytesIO(data)
            entry = SpfArchiveEntry(self, info['name'], entry_stream)
            self._entries_dict[info['name']] = entry
                    
    def save(self):
        self._stream.truncate(0)
        entry_index_stream = io.BytesIO()
        entry_index_struct = struct.Struct('<128s2lh2B')
        for count, entry in enumerate(self.entries):
            content_start_pos = self._stream.tell()
            with contextlib.closing(entry.open()) as entry_stream:
                entry_stream.seek(0)
                content_bytes = entry_stream.read()
            content_len = len(content_bytes)
            
            self._stream.write(content_bytes)
            entry_index_stream.write(entry_index_struct.pack(
                entry.entry_name.encode(self._encoding), content_start_pos, content_len,
                count + 1, 0, self.archive_number
            ))
        self._stream.write(entry_index_stream.getvalue())
        entry_index_length = len(self.entries) * 140
        self._stream.write(
            struct.pack('<2l128sl', entry_index_length, self.archive_number, b'', self.version)
        )

    def get_entry(self, entry_name):
        return self._entries_dict[entry_name]

    def open_entry(self, entry_name):
        stream = self.get_entry(entry_name).open()
        return jiendia.io.open.get_archive_type(entry_name)(stream)
    
    def create_entry(self, entry_name):
        stream = io.BytesIO()
        return self.create_entry_from_stream(entry_name, stream)
    
    def create_entry_from_file(self, entry_name, path):
        stream = open(path, 'rb')
        return self.create_entry_from_stream(entry_name, stream)
    
    def create_entry_from_stream(self, entry_name, stream):
        entry = SpfArchiveEntry(self, entry_name, stream)
        self._entries_dict[entry_name] = entry
        return entry
        
class SpfArchiveEntry(object):
    
    def __init__(self, archive, entry_name, stream):
        self.archive = archive
        self.entry_name = entry_name
        self.length = None
        if not isinstance(stream, io.BufferedIOBase):
            raise RuntimeError('SPF Archive Entry requires io.BufferedIOBase type.')
        self._stream = stream
    
    def __len__(self):
        if self.length is None:
            return len(self._stream.read())
        return self.length
    
    def open(self):
        return self._stream

    def close(self):
        if not self._stream.closed:
            self._stream.close()
# -*- coding: utf8 -*-
import io
import struct
import contextlib

class SpfArchiveMode(object):
    READ = 0
    CREATE = 1
    UPDATE = 2

class SpfArchive(object):
    
    def __enter__(self):
        return self
    
    def __exit__(self, *exc):
        if self._mode in (SpfArchiveMode.CREATE, SpfArchiveMode.UPDATE):
            self._save()
        self.close()
        
    def __init__(self, stream, mode, encoding, version = None, archive_number = None):
        self.entries = []
        self._stream = stream
        self._mode = mode
        self._encoding = encoding
        self._entries_dict = {}
        if self._mode == SpfArchiveMode.CREATE:
            if version is None or archive_number is None:
                raise RuntimeError('create mode requires `version` and `archive_number`')
            self.version = version
            self.archive_number = archive_number
        else:
            self._init()
            
    def close(self):
        self._stream.close()
        
    def get_entry(self, entry_name):
        return self._entries_dict[entry_name]
    
    def create_entry(self, entry_name):
        entry = SpfArchiveEntry(self, entry_name)
        self.entries.append(entry)
        self._entries_dict[entry_name] = entry
        return entry
        
    def _init(self):
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
            entry_name = entry_name.rstrip(b'\x00').decode(self._encoding).replace('\\', '/')
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
            self.entries.append(entry)
            self._entries_dict[info['name']] = entry
        
    def _save(self):
        self._stream.truncate(0)
        entry_index_stream = io.BytesIO()
        entry_index_struct = struct.Struct('<128s2lh2B')
        for count, entry in enumerate(self.entries):
            content_start_pos = self._stream.tell()
            with contextlib.closing(entry.open()) as entry_stream:
                content_bytes = entry_stream.getvalue()
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
        
class SpfArchiveEntry(object):
    
    def __init__(self, archive, entry_name, stream = None):
        self.archive = archive
        self.entry_name = entry_name
        self.length = None
        if stream is None:
            stream = io.BytesIO()
        self._stream = stream
    
    def __len__(self):
        if self.length is None:
            return len(self._stream.read())
        return self.length
    
    def open(self):
        return self._stream

class SpfArchiveFile(SpfArchive):
    
    def __init__(self, file_path, mode, encoding, version = None, archive_number = None):
        if mode == SpfArchiveMode.CREATE:
            open_mode = 'wb'
        elif mode == SpfArchiveMode.READ:
            open_mode = 'rb'
        elif mode == SpfArchiveMode.UPDATE:
            open_mode = 'r+b'
        stream = open(file_path, open_mode)
        SpfArchive.__init__(self, stream, mode, encoding, version, archive_number)
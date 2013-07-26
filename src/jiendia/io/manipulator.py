# -*- coding: utf-8 -*-
import io
import struct

class BaseManipulator(object):
    u"""バイナリデータを操作するマニピュレータの基本クラス"""

    def __init__(self, stream):
        u"""指定したストリームをバイナリデータとして操作するマニピュレータを作る"""
        if not isinstance(stream, io.IOBase):
            raise RuntimeError('stream requires io.IOBase type')
        self._stream = stream

class BinaryReader(BaseManipulator):
    u"""ストリームからバイナリデータを読み取る専用のクラス"""

    def __init__(self, stream):
        BaseManipulator.__init__(self, stream)
        if not self._stream.readable():
            raise RuntimeError('stream is not readable.')

    def read_byte(self):
        return self._read_as_unpack('b', 1)

    def read_short(self):
        return self._read_as_unpack('h', 2)

    def read_int32(self):
        return self._read_as_unpack('l', 4)

    def read_int64(self):
        return self._read_as_unpack('q', 8)

    def read_float(self):
        return self._read_as_unpack('f', 4)

    def read_string(self, length, encoding):
        u"""パケットから文字列を文字エンコーディングを考慮して読み取る。
        lengthは文字数ではなくバイト数
        ヌル文字が含まれている場合はそこを文字列の終端とする。ヌル文字がない場合は
        最高lengthバイトに達するまで読み込む。
        デコード不可能な文字列はU+FFFD REPLACEMENT CHARACTERに置換される"""
        # TODO: replace以外の選択肢も与えるべき
        data = self._stream.read(length).split(b'\x00')[0]
        return data.decode(encoding, 'replace')

    def read_pascal_string(self, encoding):
        u"""最初の1バイト目に大きさが格納された文字列を読み取る"""
        length = self.read_byte()
        return self.read_string(length, encoding)

    def _read_as_unpack(self, unpack_format, length):
        # TODO: エンディアンを変更可能にする
        return struct.unpack('<' + unpack_format, self._stream.read(length))[0]


class BinaryWriter(BaseManipulator):
    def __init__(self, stream):
        BaseManipulator.__init__(self, stream)

    def write_byte(self, value):
        self._write_as_pack('b', value)

    def write_short(self, value):
        self._write_as_pack('h', value)

    def write_int32(self, value):
        self._write_as_pack('l', value)

    def write_int64(self, value):
        self._write_as_pack('q', value)

    def write_float(self, value):
        self._write_as_pack('f', value)

    def write_string(self, value):
        self._stream.write(value.encode(self.encoding))

    def write_pascal_string(self, value, encoding):
        u"""先頭1バイト目に長さを格納した文字列を書き込む"""
        bytes_data = value.encode(encoding)
        self.write_byte(len(bytes_data))
        self._stream.write(bytes_data)

    def write_string_with_pading(self, value, encoding, length, padding_char=b'\x00'):
        u"""文字列を指定の長さに合うようにpadding_charで埋めて書き込む"""
        value_bytes = value.encode(encoding)
        padding_bytes = padding_char * (length - len(value_bytes))
        self._stream.write(value_bytes + padding_bytes)

    def _write_as_pack(self, pack_format, value):
        self._stream.write(struct.pack('<' + pack_format, value))

# -*- coding: utf8 -*-
class ArchiveMode:
    u"""アーカイブを開く際の方式"""
    READ = 0
    CREATE = 1
    UPDATE = 2

class BaseArchive(object):
    u"""特定データを格納したバイナリアーカイブを表すクラス
    このクラスは抽象クラスなのでこれを継承して個々のアーカイブクラスを作る"""

    _DEFAULT_MODE = ArchiveMode.READ

    def __init__(self, stream, mode = _DEFAULT_MODE):
        u"""アーカイブを開く streamにはファイルのパスかioオブジェクトを渡す"""
        if isinstance(stream, (str, bytes)):
            if mode == ArchiveMode.CREATE:
                open_mode = 'wb'
            elif mode == ArchiveMode.READ:
                open_mode = 'rb'
            elif mode == ArchiveMode.UPDATE:
                open_mode = 'r+b'
            stream = open(stream, open_mode)

        self._stream = stream
        self._mode = mode

        self.init()

        if self._mode in (ArchiveMode.READ, ArchiveMode.UPDATE):
            self.load()

    def __enter__(self):
        return self
    
    def __exit__(self, *exc):
        if self._mode in (ArchiveMode.CREATE, ArchiveMode.UPDATE):
            self.save()
        self.close()
        
    def close(self):
        self._stream.close()

    def init(self):
        pass
        
    def load(self):
        '''既存のストリームからデータ構造を読み取る'''
        raise NotImplementedError()
    
    def save(self):
        '''ストリームに変更を保存する'''
        raise NotImplementedError()

# -*- coding: utf8 -*-
import io

class ArchiveMode:
    u"""アーカイブを開く際の方式"""
    READ = 0
    CREATE = 1
    UPDATE = 2

class BaseArchive(object):
    u"""特定データを格納したバイナリアーカイブを表すクラス
    このクラスは抽象クラスなのでこれを継承して個々のアーカイブクラスを作る"""

    _DEFAULT_MODE = ArchiveMode.READ

    def __init__(self, file, mode = _DEFAULT_MODE):
        u"""アーカイブを開く streamにはファイルのパスかファイルオブジェクトを渡す
        アーカイブはバイナリモードで開かれるので文字エンコーディングは考慮しない"""

        # ファイルパスが与えられた場合ストリームとして開く
        if isinstance(file, (str, bytes)):
            if mode == ArchiveMode.CREATE:
                open_mode = 'wb'
            elif mode == ArchiveMode.READ:
                open_mode = 'rb'
            elif mode == ArchiveMode.UPDATE:
                open_mode = 'r+b'
            file = open(file, open_mode)

        # バッファ機能付きバイナリストリームかどうかちゃんとチェックする
        if not isinstance(file, io.BufferedIOBase):
            raise RuntimeError('jiendiaのアーカイブはバイナリのみを対象にしています。よってio.BufferedIOBaseを継承していないストリームを使用することはできません')

        self._stream = file
        self._mode = mode

    def __enter__(self):
        u"""with文を使ってアーカイブを開くことができる
        使用例:
            with Archive('filename') as archive:
                archive.some_method()
        """
        return self
    
    def __exit__(self, *exc):
        u"""withブロックから抜けた時に実行されるメソッド
        内部のファイルオブジェクト（ストリーム）を閉じる
        ファイルに変更を加えていた場合は変更が書き込まれる"""
        if self._mode in (ArchiveMode.CREATE, ArchiveMode.UPDATE):
            self.save()
        self.close()
        
    def close(self):
        u"""アーカイブを閉じる"""
        self._stream.close()

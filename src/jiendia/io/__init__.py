# -*- coding: utf8 -*-
import os.path
from jiendia.io._base import ArchiveMode
from jiendia.io.spf import SpfArchive
from jiendia.io.tbl import TblArchive
from jiendia.io.seq import SeqArchive

def open_archive(path, mode = ArchiveMode.READ, encoding = 'ascii'):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.spf':
        return SpfArchive(path, mode, encoding)
    if ext == '.tbl':
        return TblArchive(path, mode, encoding)
    if ext == '.seq':
        return SeqArchive(path, mode, encoding)
    else:
        raise RuntimeError('Unknown extension {0}'.format(ext))

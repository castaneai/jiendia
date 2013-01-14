# -*- coding: utf8 -*-
import os.path
from jiendia.io._base import ArchiveMode
from jiendia.io.spf import SpfArchive
from jiendia.io.tbl import TblArchive
from jiendia.io.seq import SeqArchive

encoding = 'cp932'

def open_archive(path):
    ext = os.path.splitext(path)[1].lower() 
    if ext == '.spf':
        return SpfArchive(path, ArchiveMode.READ, encoding)
    if ext == '.tbl':
        return TblArchive(path, ArchiveMode.READ, encoding)
    if ext == '.seq':
        return SeqArchive(path, ArchiveMode.READ, encoding)
    else:
        raise RuntimeError('Unknown extension {0}'.format(ext))
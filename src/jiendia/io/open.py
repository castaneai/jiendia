# -*- coding: utf8 -*-
import os.path
from jiendia.io.archive.base import BaseArchive, DEFAULT_MODE, DEFAULT_ENCODING
from jiendia.io.spf import SpfArchive
from jiendia.io.tbl import TblArchive
from jiendia.io.seq import SeqArchive
from jiendia.io.archive.ldt import LdtArchive

def get_archive_type(filename) -> type:
    ext = os.path.splitext(filename)[1].lower()
    if ext == '.spf':
        return SpfArchive
    elif ext == '.tbl':
        return TblArchive
    elif ext == '.seq':
        return SeqArchive
    elif ext == '.ldt':
        return LdtArchive
    else:
        raise RuntimeError('Unknown file extension {0}'.format(ext))

def open_archive(path, mode = DEFAULT_MODE, encoding = DEFAULT_ENCODING) -> BaseArchive:
    return get_archive_type(path)(path, mode, encoding)
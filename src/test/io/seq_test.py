# -*- coding: utf8 -*-
import os.path
from jiendia.io.seq import SeqArchive, ArchiveMode

def test_read():
    data_dir = os.path.dirname(__file__) + '/data'
    with SeqArchive(data_dir + '/010_01_01_STAND_R.SEQ', ArchiveMode.READ, 'cp932') as seq:
        assert len(seq.frames) > 0
        for index, frame in enumerate(seq.frames):
            assert frame.number == index + 1
            assert len(frame.parts) > 0

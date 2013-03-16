# -*- coding: utf8 -*-
from jiendia.test.io import DATA_DIR

def test_read():
    from jiendia.io.seq import SeqArchive
    with SeqArchive(DATA_DIR + '/010_01_01_STAND_R.SEQ', encoding = 'cp932') as seq:
        assert len(seq.frames) > 0
        for index, frame in enumerate(seq.frames):
            assert frame.number == index + 1
            assert len(frame.parts) > 0

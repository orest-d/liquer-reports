from lqreports.segments import *

class TestSegments:
    def test_register(self):
        r=Register()
        assert len(r)==0
        r.xxx="yyy"
        assert len(r)==1
        assert r["xxx"]=="yyy"
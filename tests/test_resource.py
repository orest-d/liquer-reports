from lqreports.resource import *

class TestResource:
    def test_descriptions(self):
        assert "vue" in resources_description()
    def test_load(self):
        for key in resources_description().keys():
            assert isinstance(load_resource(key), bytes)
            
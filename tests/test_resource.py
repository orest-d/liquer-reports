from lqreports.resource import *
from lqreports.constants import LinkType


class TestResource:
    def test_descriptions(self):
        assert "vue" in resources_description()

    def test_load(self):
        for key in resources_description().keys():
            assert isinstance(load_resource(key), bytes)

    def test_dataurl(self):
        for key in resources_description().keys():
            link = FileResource(key).link(LinkType.DATAURL)
            assert isinstance(link, str)
            assert link.startswith("data:")

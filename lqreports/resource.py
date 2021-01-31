from pathlib import Path
import yaml
from lqreports.util import mimetype_from_extension, dataurl
from lqreports.constants import LinkType

def resources_path():
    return Path(__file__).parent / "resources"


_resources_description = None


def resources_description():
    global _resources_description
    if _resources_description is None:
        with open(resources_path() / "resources.yaml") as f:
            _resources_description = yaml.load(f, Loader=yaml.FullLoader)
    return _resources_description

def load_resource(name):
    return open(resources_path() / resources_description()[name]["filename"]).read()

class Resource(object):
    pass

class FileResource(Resource):
    def __init__(self, name):
        self.name = name
        self.description = resources_description()[name]
        self.data = load_resource(name)

    @property
    def url(self):
        return self.description["url"]

    @property
    def filename(self):
        return self.description["filename"]

    @property
    def extension(self):
        return self.filename.split(".")[-1]

    @property
    def mimetype(self):
        return mimetype_from_extension(self.extension)

    def link(self, link_type=LinkType.LINK):
        if link_type == LinkType.LINK:
            return self.url
        elif link_type == LinkType.DATAURL:
            return dataurl(self.data, self.mimetype)
        raise Exception(f"Unsupported link type: {link_type}")

class LinkResource(Resource):
    def __init__(self, link, name=None):
        self.name = "link"+id(self) if name is None else name
        self.description = {}
        self.data = None
        self.url = link
        self.filename = None
        self.extension = None
        self.mimetype = None

    def link(self, link_type=LinkType.LINK):
        return self.url

if __name__ == "__main__":
    print(resources_description())

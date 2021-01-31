from lqreports.constants import LinkType

class RenderContext(object):
    link_type = LinkType.LINK

class Register(dict):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self[name] = value
class Renderable(object):
    def render(self, render_context=None):
        return ""

class Segment(Renderable):
    prefix=""
    suffix=""
    separator=""

    def __init__(self, name, register):
        assert not name.startswith("_")
        self.name = name
        self.entries=[]
        
    def add(self, entry):
        self.entries.append(entry)
        if isinstance(entry, Segment):
            if entry.name in self.register:
                raise Exception(f"Duplicate segment: {entry.name}")
            else:
                self.register[entry.name]=entry
        return self
    
    def render(self, render_context=None):
        txt=str(self.prefix)
        sep=""
        for i, entry in enumerate(self.entries):
            txt += sep
            sep = self.separator
            if isinstance(entry, str):
                txt+=entry
            elif isinstance(entry, Renderable):
                txt+=entry.render(render_context)
            else:
                raise Exception(f"Unsupported entry type in {self.name}: {type(entry)}, entry number {i+1}")
        txt+=self.suffix
        return txt

class ResourceHtmlLink(Renderable):
    def __init__(self, resource, kind=None):
        self.resource = resource
        self.kind = resource.extension if kind is None else kind
    def render(self, render_context):
        if self.kind == "css":
            link = self.resource.link(render_context.link_type)
            return f"""    <link href="{link}" rel="stylesheet">""" 
        elif self.kind == "js":
            link = self.resource.link(render_context.link_type)
            return f"""    <script src="{link}"></script>""" 
        else:
            raise Exception(f"Unsupported kind: {self.kind}")

class HtmlHeader(Segment):
    prefix = "  <head>\n"
    suffix = "\n  </head>"
    separator="\n"
    def __init__(self, register):
        super().__init__("header", register)
        
    def add_resource(self, resource):
        import lqreports.resource as rs
        if isinstance(resource, str):
            resource = rs.FileResource(resource)
        return self.add(ResourceHtmlLink(resource))
        
if __name__ == "__main__":
    print (HtmlHeader(Register()).add_resource("vuetify_css").render(RenderContext()))
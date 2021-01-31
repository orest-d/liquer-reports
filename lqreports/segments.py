from lqreports.constants import LinkType

class RenderContext(object):
    def __init__(self, link_type=LinkType.LINK):
        self.link_type = link_type

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
        self.register=register
        self.entries=[]
        self.register[name]=self
            
    def add(self, entry):
        self.entries.append(entry)
        if isinstance(entry, Segment):
            if entry.name in self.register:
                if id(self.register[entry.name])!=id(entry):
                    raise Exception(f"Duplicate segment: {entry.name}")
            else:
                self.register[entry.name]=entry
        return self

    def add_resource(self, resource):
        import lqreports.resource as rs
        if isinstance(resource, str):
            resource = rs.FileResource(resource)
        return self.add(ResourceHtmlLink(resource))
    
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
        

class HtmlBody(Segment):
    prefix = "  <body>\n"
    suffix = "\n  </body>"
    separator="\n"
    def __init__(self, register):
        super().__init__("body", register)

class Scripts(Segment):
    separator="\n"
    def __init__(self, register):
        super().__init__("scripts", register)

        
class HtmlDocument(Segment):
    prefix = "<html>\n"
    suffix = "\n</html>"
    separator="\n"
    def __init__(self, register, title="Document"):
        super().__init__("document", register)
        self.add(HtmlHeader(register))
        self.add(HtmlBody(register))
        self.register.body.add(Segment("content",register))
        self.register.body.add(Scripts(register))
        self.title=title
        self.register.header.add(f"<title>{title}</title>")

class VuetifyMain(Segment):
    prefix="""<div id="app">
    <v-app>
      <v-main>
"""
    suffix="""
      </v-main>
    </v-app>
  </div>
"""

class VuetifyDocument(HtmlDocument):
    def __init__(self, register, title="Document"):
        super().__init__(register, title=title)
        self.register.header.add_resource("materialdesignicons")
        self.register.header.add_resource("vuetify_css")
        self.register.content.add(VuetifyMain("main", register))
        self.register.scripts.add_resource("vue")
        self.register.scripts.add_resource("vue_resource")
        self.register.scripts.add_resource("vuetify")

if __name__ == "__main__":
    r = Register()
    doc = VuetifyDocument(r)
    r.main.add("<v-container>Hello world</v-container>")
    #doc.register.header.add_resource("vuetify_css")
    print (doc.render(RenderContext(link_type=LinkType.DATAURL)))
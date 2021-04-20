import sys
sys.path.append("..")

from lqreports.segments import *

if __name__ == '__main__':
    r = Register()
    doc = VuetifyDashboard(r)    
    r.vuetify_script.component("Hello").add_template("<pre><h1>Hello {{greet}}!</pre>").add_data("greet", "world")
    r.v_main.add("<hello></hello>")
    # doc.register.header.add_resource("vuetify_css")
    print(doc.render(RenderContext(link_type=LinkType.LINK)))

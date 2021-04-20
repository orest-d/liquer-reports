import sys
sys.path.append("..")

import matplotlib.pyplot as plt
from lqreports.segments import *

if __name__ == '__main__':
    r = Register()
    doc = (
        VuetifyDashboard(r)
        .with_navigation_drawer()
        .with_app_bar(color="primary")
        .with_plotly()
        .with_panels()
    )
    r.home_panel.add("<h1>Home</h1>")
    doc.panel("panel1", fluid=True).add(
        "<v-row><v-col><h1>Panel 1</h1>Hello {{what}}!</v-col></v-row>"
    )
    doc.panel("panel2").add("<h1>Panel 2</h1>")
    doc.panel("panel3").add("""<plotly-chart :chart="chart1" style="min-height:800px;"></plotly-chart>""")
    doc.panel("panel4").chart("chart2", value=dict(
        uuid= "12345",
        traces= [dict(y=[1,2,3], line=dict(color="blue", width=5, shape="line"))],
        layout= dict(title='Chart 2', xaxis=dict(title="X Axis"), yaxis=dict(title="Y Axis")),
        config= dict()
    ))
    r.vuetify_script.add_method("update_chart2", """
    function(){
        this.chart2.traces[0].x=[1,2,3,4];
        this.chart2.traces[0].y=[10,2,30,4];
    }
    """)
    r.panel4.button("Update chart 2", click="update_chart2()")

    doc.drawer_item("Home", icon="mdi-home", panel="home_panel")
    doc.drawer_item("Google href", href="http://google.com")
    doc.drawer_item("Google to", to="http://google.com")
    doc.add_bar_button("Hello", click="this.alert('Hello')", color="primary")
    doc.add_bar_menu(
        "Second",
        [
            dict(title="first", click="this.alert('Hello1')"),
            dict(title="second", click="this.alert('Hello2')"),
            dict(title="Panel 1", panel="panel1"),
            dict(title="Panel 2", panel="panel2"),
            dict(title="Panel 3 (chart 1)", panel="panel3"),
            dict(title="Panel 4 (chart 2)", panel="panel4"),
        ],
    )
    doc.add_bar_spacer()
    doc.add_bar_button(None, icon="mdi-magnify", click="this.alert('magnify')")
    #    doc.with_dataframe(pd.DataFrame(dict(a=[1,2,3],b=[4,5,6])))
    doc.with_dataframe(pd.read_csv("test.csv")).with_panel_row_action("panel2")
    #r.vuetify_script.add_data("myfilter",False)
    r.vuetify_script.add_method("update_filter", """
    function(){
        console.log("Update filter",this.myfilter);
        if (this.myfilter){
            this.dataframe_data = this.dataframe.data.filter(function(x){
                return ((x[1]>2000) && (x[1]<2005)); 
            });
        }
        else{
            this.dataframe_data = this.dataframe.data;
        }
    }
    """)
    r.vuetify_script.add_watch("myfilter", "function(new_value,old_value){console.log('watch',new_value,old_value);this.update_filter();}")
    r.panel1.switch("myfilter","My filter", value=False)
    r.panel1.dataframe_view()
    r.panel1.add("""{{selected_row}}""")
    r.panel2.add("""<h2>Selected</h2>{{selected_row}}""")
    r.panel2.row_detail()
    plt.plot([0,1],[0,1])
    r.panel2.figure(plt.gcf())
    r.panel1.liquer_logo()

    # r.app.add("<v-main><v-container>Hello {{what}}!</v-container></v-main>")
    #    r.scripts.add(VuetifyScript(r))
    r.vuetify_script.add_data("to_greet", "WORLD")
    r.vuetify_script.add_data("chart1", dict(
        uuid= "1234",
        traces= [
          {
            "y": [0,1,2],
            "line": {
              "color": "#000000",
              "width": 4,
              "shape": "line"
            }
          }
        ],
        layout={
          "title":'Chart 1',
          "xaxis": {
            "title": 'xaxis title'
          },
          "yaxis": {
            "title": 'yaxis title'
          }
        },
        config={
            "responsive":True
        }
    ))

    r.vuetify_script.add_computed(
        "what", "return '*'+this.to_greet+'*';", "this.to_greet=value;"
    )
    r.vuetify_script.add_created("this.to_greet='me';")

    # doc.register.header.add_resource("vuetify_css")
    print(doc.render(RenderContext(link_type=LinkType.LINK)))

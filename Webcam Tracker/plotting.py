from motion_detector import df
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource

df["Start_str"] = df["Start"].dt.strftime("%Y- %m - %d %H:%M:%S")
df["End_str"] = df["End"].dt.strftime("%Y- %m - %d %H:%M:%S")
cds = ColumnDataSource(df)

p = figure(x_axis_type="datetime", width=500, height=350, sizing_mode="stretch_width",title="Motion Graph")

p.yaxis.minor_tick_line_color =  None
p.yaxis[0].ticker.desired_num_ticks=1

hover = HoverTool(tooltips=[("Start","@Start_str"),("End","@End_str")])

p.add_tools(hover)
q = p.quad(left="Start",right="End",bottom=0,top=1, color="blue", source=cds)

output_file("motiongraph.html")

show(p)
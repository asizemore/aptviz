import plotly.graph_objects as go
import plotly.io as pio




my_charcoal = "#3f4142"
my_lightgray = "#ebf0f2"
highlight = "#8D3B34"

# From https://github.com/empet/scientific-colorscales/blob/master/scicolorscales.py
lapaz= [[0.0, 'rgb(26, 12, 101)'],
        [0.1, 'rgb(33, 46, 124)'],
        [0.2, 'rgb(39, 77, 145)'],
        [0.3, 'rgb(49, 105, 159)'],
        [0.4, 'rgb(68, 131, 167)'],
        [0.5, 'rgb(102, 153, 164)'],
        [0.6, 'rgb(141, 163, 152)'],
        [0.7, 'rgb(179, 167, 139)'],
        [0.8, 'rgb(223, 183, 148)'],
        [0.9, 'rgb(253, 217, 197)'],
        [1.0, 'rgb(255, 243, 243)']]

davos= [[0.0, 'rgb(44, 26, 76)'],
        [0.1, 'rgb(40, 59, 110)'],
        [0.2, 'rgb(42, 94, 151)'],
        [0.3, 'rgb(68, 117, 193)'],
        [0.4, 'rgb(96, 137, 190)'],
        [0.5, 'rgb(125, 156, 181)'],
        [0.6, 'rgb(155, 175, 172)'],
        [0.7, 'rgb(186, 196, 163)'],
        [0.8, 'rgb(215, 217, 161)'],
        [0.9, 'rgb(237, 236, 206)'],
        [1.0, 'rgb(255, 255, 255)']]

davos_colors = [color[1] for color in davos]
lapaz_colors = [color[1] for color in lapaz]




dev_temp = go.layout.Template()
dev_temp.data.scatter = [go.Scatter(marker=dict(symbol="circle"))]
dev_temp.layout.font=dict(family="Avenir", color=my_charcoal)
dev_temp.layout.paper_bgcolor = "#fff"
dev_temp.layout.plot_bgcolor = "#fff"
dev_temp.layout.colorscale = dict(sequential=davos_colors)
dev_temp.layout.colorway = davos_colors
dev_temp.layout.xaxis = dict(color=my_charcoal, linewidth = 1, gridcolor = my_lightgray, gridwidth = 0.5)
dev_temp.layout.yaxis = dict(color=my_charcoal, linewidth = 1, gridcolor = my_lightgray, gridwidth = 0.5)
dev_temp.layout.violingap = 0.4
                          
pio.templates["aptviz"] = dev_temp                 

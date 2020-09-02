import numpy as np
from bokeh.plotting import figure, show
from bokeh.io import export_png

x = np.arange(start=0.0, stop=2*np.pi, step=0.1)


for case in range(5):
    f_x = np.cos(case*x*np.pi)/2.0

    fig = figure(title=f'Bokeh example{case}', x_axis_label='x', y_axis_label='f(x) = cos({case}*x*PI)')
    
    fig.line(x, f_x)

    
    export_png(fig, filename=f'../static/bokeh_{case}.png')

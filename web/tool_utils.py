import base64
import io
import random
import os
import sys
import json 

import pandas as pd
from io import StringIO

from flask import render_template
from flask import url_for
from flask import Response

from web.models import Sinus
from web.models import Cosinus
# MATPLOTLIB
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

#SEABORN
import seaborn as sb



# BOKEH
from bokeh.plotting import figure
from bokeh.embed import components

# PLOTLY
import plotly.express as px
import plotly
import plotly.graph_objs as go

# PYGAL
import pygal

def str_to_class(string):
    return getattr(sys.modules[__name__], string)


def make_chart_mplib(model_name):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.grid(True)

    #points = str_to_class(model_name).query.all()
    points = str_to_class(model_name).query.all()
    xx = [point.x for point in points]
    yy = [point.y for point in points]
    axis.plot(xx, yy)
    axis.set_xlabel('x')
    axis.set_ylabel('y')
    axis.set_title('Matplotlib')

    return fig

def make_plot_seaborn(model_name):
    points = str_to_class(model_name).query.all()
    
    xx = [point.x for point in points]
    yy = [point.y for point in points]
    sb.set_style("dark")

    df = pd.DataFrame(list(zip(xx, yy)))
    chart.savefig(img, format='png')
    chart = sns.lineplot(x="timepoint", y="signal", data=df)
    return chart


def make_chart_bokeh(model_name):
    points = str_to_class(model_name).query.all()
    
    xx = [point.x for point in points]
    yy = [point.y for point in points]

    chart = figure(title="Bokeh plot", width=450, height=450, x_axis_label='x', y_axis_label='y')
    chart.line(xx, yy)
    

    return chart

def make_chart_plotly(model_name):
    points = str_to_class(model_name).query.all()
    
    xx = [point.x for point in points]
    yy = [point.y for point in points]
    chart_props = {
        "data": [go.Line(x=xx, y=yy)],
        "layout": go.Layout(title="Plotly chart", xaxis_title="x", yaxis_title="y", width=500, height=500, margin={"l": 20, "t": 30})
    }
    chart_div_html = plotly.offline.plot(chart_props, include_plotlyjs=False, output_type='div')
    return chart_div_html
    

def make_chart_pygal(model_name):
    points = str_to_class(model_name).query.all()
    
    xx = [point.x for point in points]
    yy = [point.y for point in points]

    chart = pygal.XY(show_dots=False, width=450, height=450)
    chart.title = model_name
    chart.add('y', [(point.x, point.y) for point in points])

    return chart


def files_count(lib_name='', path_to_images='.'):
    return len(list(filter(lambda s: s.startswith(lib_name), [f for f in os.listdir(path_to_images) if os.path.isfile(os.path.join(path_to_images, f))])))


def make_points(db, form, model_name, step=0.1,):
    x_range = int((1.0)/step * (form.end.data - form.begin.data))+1
    current_points = set([point.x for point in str_to_class(model_name).query.all()])
    for i in range(x_range):
        dx = i*step
        pt = str_to_class(model_name).make_point(form.begin.data+dx)
        if pt.x not in current_points:
            db.session.add(pt)

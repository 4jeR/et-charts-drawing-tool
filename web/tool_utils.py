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
from web.models import SinusCoefs
from web.models import Cosinus
from web.models import SquareRoot
from web.models import FileDataPoint

# MATPLOTLIB
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

#SEABORN
import seaborn as sb



# BOKEH
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.io import export_png
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
    Model = str_to_class(model_name)

    points = Model.query.all()
    xx = [point.x for point in points]
    yy = [point.y for point in points]
    axis.plot(xx, yy)
    axis.set_xlabel('x')
    axis.set_ylabel('y')
    axis.set_title('Matplotlib')

    return fig

def make_chart_seaborn(model_name):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title('Seaborn')

    axis.grid(True)
    sb.set(style="darkgrid")

    Model = str_to_class(model_name)
    points = Model.query.all()

    data = [
        {'x': point.x, model_name: point.y} for point in points
    ]
    df = pd.DataFrame(data=data)
    sb.lineplot(data=df, ax=axis)
    
    return fig


def make_chart_bokeh(model_name):
    Model = str_to_class(model_name)
    points = Model.query.all()

    xx = [point.x for point in points]
    yy = [point.y for point in points]

    chart = figure(title="Bokeh plot", width=500, height=450, x_axis_label='x', y_axis_label='y')
    chart.line(xx, yy)
    

    return chart

def make_chart_plotly(model_name):
    Model = str_to_class(model_name)
    points = Model.query.all()
    
    xx = [point.x for point in points]
    yy = [point.y for point in points]
    chart_props = {
        "data": [go.Line(x=xx, y=yy)],
        "layout": go.Layout(title="Plotly chart", title_x=0.5, xaxis_title="x", yaxis_title="y", width=500, height=500, margin={"l": 20, "t": 30})
        
    }
    
    chart_div_html = plotly.offline.plot(chart_props, include_plotlyjs=False, output_type='div')
    return chart_div_html
    

def make_chart_pygal(model_name):
    Model = str_to_class(model_name)
    points = Model.query.all()


    chart = pygal.XY(show_dots=False, width=500, height=450)
    chart.title = "Pygal"
    chart.add('y', [(point.x, point.y) for point in points])

    return chart


def files_count(lib_name='', path_to_images='.'):
    return len(list(filter(lambda s: s.startswith(lib_name), [f for f in os.listdir(path_to_images) if os.path.isfile(os.path.join(path_to_images, f))])))


def make_points(db, form, model_name, step=0.1):
    x_range = int((1.0)/step * (form.end.data - form.begin.data))+1
    current_points = set([point.x for point in str_to_class(model_name).query.all()])
    for i in range(x_range):
        dx = i*step
        pt = str_to_class(model_name).make_point(form.begin.data+dx)
        if pt.x not in current_points:
            db.session.add(pt)

def get_data_from_file(filename):
    x = []
    y = []

    with open(f'web/data/{filename}', 'r') as f:
        for line in f:
            x.append(int(line.split(',')[0]))
            y.append(int(line.split(',')[1]))

    return x, y
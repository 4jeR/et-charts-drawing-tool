import base64
import io
import random
import os
import sys

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
from bokeh.plotting import output_file
from bokeh.plotting import show
from bokeh.io.export import get_screenshot_as_png
from bokeh.resources import CDN
from bokeh.embed import file_html




def str_to_class(str):
    return getattr(sys.modules[__name__], str)


def make_plot_mplib(model_name):
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


def make_plot_bokeh(model_name):
    # Generate canvas
    points = str_to_class(model_name).query.all()
    
    xx = [point.x for point in points]
    yy = [point.y for point in points]



    source = ColumnDataSource(data=dict(x=xx, y=yy, name='Bokeh plot'))

    plot = figure(title='Bokeh', x_axis_label='x', y_axis_label='y')
    line = plot.line("x", "y", source=source)

    html = file_html(plot, CDN, "bokeh_test_plot")
    with open('web/templates/bokeh_plot.html', 'w') as f:
        f.write(html)
    
    return render_template('bokeh_plot.html')



def files_count(lib_name='', path_to_images='.'):
    return len(list(filter(lambda s: s.startswith(lib_name), [f for f in os.listdir(path_to_images) if os.path.isfile(os.path.join(path_to_images, f))])))


def make_points(db, form, step=0.1):
    x_range = int((1.0)/step * (form.end.data - form.begin.data))+1
    current_points = set([point.x for point in Sinus.query.all()])
    for i in range(x_range):
        dx = i*step
        pt = Sinus.make_point(form.begin.data+dx)
        if pt.x not in current_points:
            db.session.add(pt)


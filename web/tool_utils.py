import base64
import io
import random
import os
from io import StringIO

from flask import Response
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from web.models import Point

def make_plot_mplib():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    points = Point.query.all()

    xx = [point.x for point in points]
    yy = [point.y for point in points]

    axis.plot(xx, yy)
    axis.set_xlabel('x')
    axis.set_ylabel('y')
    axis.set_title('Matplotlib')
    return fig

def make_plot_seaborn():
    fig, ax = pyplot.subplots()
    points = Point.query.all()
    
    xx = [point.x for point in points]
    yy = [point.y for point in points]
    sb.set_style("dark")


    sb.lineplot(x=xx, y=yy).set_title()
    plt.savefig(img, format='png')
    plt.close()

    return fig




def files_count(lib_name='', path_to_images='.'):
    return len(list(filter(lambda s: s.startswith(lib_name), [f for f in os.listdir(path_to_images) if os.path.isfile(os.path.join(path_to_images, f))])))

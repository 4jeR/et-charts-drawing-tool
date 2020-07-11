import io
import random
from flask import render_template, url_for, flash, redirect, Response
from web import app
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig



@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')



@app.route("/matplotlib")
def route_matplotlib():
    return render_template('matplotlib.html')


@app.route("/seaborn")
def route_seaborn():
    return render_template('seaborn.html')


@app.route("/bokeh")
def route_bokeh():
    return render_template('bokeh.html')

@app.route("/plotly")
def route_plotly():
    return render_template('plotly.html')

@app.route("/pygal")
def route_pygal():
    return render_template('pygal.html')

@app.route("/missingno")
def route_missingno():
    return render_template('missingno.html')


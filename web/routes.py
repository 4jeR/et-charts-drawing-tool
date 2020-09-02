from web.tool_utils import files_count
from web.models import Point
from web.forms import PointForm
from flask import render_template, url_for, flash, redirect, Response
from web import app, db
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import os


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/add_point", methods=['GET', 'POST'])
def route_add_point():
    form = PointForm()
    if form.validate_on_submit():
        point = Point(x=form.x.data, y=form.y.data)
        db.session.add(point)
        db.session.commit()
        flash(f'{point} has been added to the database!', 'success')
        return redirect(url_for('route_add_point'))
    return render_template('add_point.html', form=form)

@app.route("/matplotlib")
def route_matplotlib():
    #images will be caught from database later, for now it is fine !!!!!!
    

    path_to_images = os.getcwd() + '/web/static/plots'
    mplib_charts = [os.path.join(app.config['UPLOAD_FOLDER'], f'mplib_{i}.png') for i in range(1, files_count('mplib', path_to_images))]
    return render_template('matplotlib.html', chart_images=mplib_charts)


@app.route("/seaborn")
def route_seaborn():
    path_to_images = os.getcwd() + '/web/static/plots'
    sb_charts = [os.path.join(app.config['UPLOAD_FOLDER'], f'sborn_{i}.png') for i in range(1, files_count('sborn', path_to_images))]
    return render_template('seaborn.html', chart_images=sb_charts)


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


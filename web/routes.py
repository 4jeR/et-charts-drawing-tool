import os
import math
import io
import random

from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import Response

from web import app 
from web import db
from web.models import Point
from web.forms import PointForm
from web.tool_utils import files_count
from web.tool_utils import make_plot_mplib

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


@app.route('/data/plot/matplotlib')
def route_plot_mplib():
    fig = make_plot_mplib()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/data/plot/seaborn')
def route_plot_seaborn():   
    fig = make_plot_seaborn()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/data/plot/bokeh')
def route_plot_bokeh():
    fig = make_plot_mplib()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/jpg')


@app.route('/data/plot/plotly')
def route_plot_plotly():
    fig = make_plot_mplib()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/jpg')


@app.route('/data/plot/pygal')
def route_plot_pygal():
    fig = make_plot_mplib()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/jpg')


@app.route('/data/plot/missingno')
def route_plot_missingno():
    fig = make_plot_mplib()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/jpg')




@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

#CRUD
#C
@app.route("/data/add", methods=['GET', 'POST'])
def route_add_data():
    form = PointForm()
    if form.validate_on_submit():
        
        func = lambda x: math.cos(math.pi + x*math.pi)/2.0 # this probably will be the class field named for ex.: f_x = ....
                                        # so different models could be placed in the database, for ex.: sinus, sqrt, etc.
        step = 0.1
        x_range = int((1.0)/step * (form.end.data - form.begin.data))+1
        current_points = set([point.x for point in Point.query.all()])
        for i in range(x_range):
            dx = i*step
            pt = Point(x=float(form.begin.data + dx), y=float(func(form.begin.data + dx)))
            if pt.x not in current_points:
               db.session.add(pt)
        
        db.session.commit()
        flash(f'Range <{form.begin.data}, {form.end.data}> has been successfully added to the database!', 'success')
        return redirect(url_for('route_show_data'))
    return render_template('add_data.html', form=form)

#R
@app.route("/data/show", methods=['GET', 'POST'])
def route_show_data():
    points = Point.query.all()
    if not points:
        points = []
    return render_template('show_data.html', points=points)
#U
#todo

#D
@app.route("/data/delete/<int:point_id>", methods=['POST'])
def route_delete_point(point_id):
    point = Point.query.get_or_404(point_id)
    db.session.delete(point)
    db.session.commit()
    flash(f'Point ({point.id} has been succesfully removed from the database', 'success')
    return redirect(url_for('route_show_data'))


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


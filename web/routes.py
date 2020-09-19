import os
import math
import io
import random
import json

from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import Response

from web import app 
from web import db
from web.models import Sinus
from web.models import Cosinus

from web.forms import SinusForm
from web.forms import CosinusForm
from web.forms import SqrtForm

from web.tool_utils import files_count
from web.tool_utils import make_plot_mplib
from web.tool_utils import make_plot_bokeh
from web.tool_utils import make_points
from web.tool_utils import str_to_class

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from bokeh.embed import json_item
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components

@app.route('/data/plot/matplotlib/<string:model_name>')
def route_plot_mplib(model_name):
    fig = make_plot_mplib(model_name)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/data/plot/seaborn/<string:model_name>')
def route_plot_seaborn(model_name):   
    pass
    # fig = make_plot_seaborn(model_name)
    # output = io.BytesIO()
    # FigureCanvas(fig).print_png(output)
    # return Response(output.getvalue(), mimetype='image/png')



@app.route('/data/plot/bokeh/<string:model_name>')
def route_plot_bokeh(model_name):
    plot = make_plot_bokeh(model_name)
    script, div = components(plot)
    kwargs = {'script': script, 'bokehdiv': div}
    return render_template('show_data.html', model_name=model_name, **kwargs)


@app.route('/data/plot/plotly/<string:model_name>')
def route_plot_plotly(model_name):
    pass
    # fig = make_plot_mplib(model_name)
    # output = io.BytesIO()
    # FigureCanvas(fig).print_png(output)
    # return Response(output.getvalue(), mimetype='image/jpg')


@app.route('/data/plot/pygal/<string:model_name>')
def route_plot_pygal(model_name):
    pass
    # fig = make_plot_mplib(model_name)
    # output = io.BytesIO()
    # FigureCanvas(fig).print_png(output)
    # return Response(output.getvalue(), mimetype='image/jpg')


@app.route('/data/plot/missingno/<string:model_name>')
def route_plot_missingno(model_name):
    pass
    # fig = make_plot_mplib(model_name)
    # output = io.BytesIO()
    # FigureCanvas(fig).print_png(output)
    # return Response(output.getvalue(), mimetype='image/jpg')




@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')





# SINUS SINUS SINUS SINUS SINUS SINUS SINUS SINUS SINUS SINUS SINUS SINUS SINUS SINUS SINUS SINUS
#CRUD
#C
@app.route("/data/add/sinus", methods=['GET', 'POST'])
def route_add_data_sinus():
    form = SinusForm()
    if form.validate_on_submit():
        Sinus.set_coefs(a=form.coef_a.data, b=form.coef_b.data, c=form.coef_c.data, x_zero=form.begin.data)
        make_points(db, form, model_name='Sinus', step=0.1)
        db.session.commit()
        flash(f'Range <{form.begin.data}, {form.end.data}> has been successfully added to the database!', 'success')
        return redirect(url_for('route_show_data', model_name='Sinus'))
    return render_template('add_data.html', form=form, model_name='Sinus')

@app.route("/data/add/cosinus", methods=['GET', 'POST'])
def route_add_data_cosinus():
    form = CosinusForm()
    if form.validate_on_submit():
        Cosinus.set_coefs(a=form.coef_a.data, b=form.coef_b.data, c=form.coef_c.data)
        make_points(db, form, model_name='Cosinus', step=0.1)
        db.session.commit()
        flash(f'Range <{form.begin.data}, {form.end.data}> has been successfully added to the database!', 'success')
        return redirect(url_for('route_show_data', model_name='Cosinus'))
    return render_template('add_data.html', form=form, model_name='Cosinus')

@app.route("/data/add/sqrt", methods=['GET', 'POST'])
def route_add_data_sqrt():
    form = CosinusForm()
    if form.validate_on_submit():
        Cosinus.set_coefs(a=form.coef_a.data, b=form.coef_b.data, c=form.coef_c.data)
        make_points(db, form, model_name='Sinus', step=0.1)
        db.session.commit()
        flash(f'Range <{form.begin.data}, {form.end.data}> has been successfully added to the database!', 'success')
        return redirect(url_for('route_show_data', model_name='SquareRoot'))
    return render_template('add_data.html', form=form, model_name='SquareRoot')




#R
@app.route("/data/show/<string:model_name>")
def route_show_data(model_name):
    points = str_to_class(model_name).query.all()
    if not points:
        points = []
    return render_template('show_data.html', points=points, model_name=model_name)
#U

#D
@app.route("/data/delete/<string:model_name>/<int:point_id>", methods=['POST'])
def route_delete_point(model_name, point_id):
    point = str_to_class(model_name).query.get_or_404(point_id)
    db.session.delete(point)
    db.session.commit()
    flash(f'Point ({point.id} has been succesfully removed from the database', 'success')
    return redirect(url_for('route_show_data', model_name=model_name))

@app.route("/data/delete/all/<string:model_name>", methods=['POST'])
def route_delete_all_points(model_name):
    all_points = str_to_class(model_name).query.all()
    for point in all_points:
        db.session.delete(point)
    db.session.commit()
    flash(f'All points have been deleted from sinus', 'success')
    return redirect(url_for('route_show_data', model_name=model_name))





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


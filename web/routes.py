import os
import math
import io
import random
import inspect
from datetime import datetime

from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import Response
from flask import make_response


from web import app 
from web import db

from web.models import Sinus
from web.models import SinusCoefs

from web.models import Cosinus
from web.models import CosinusCoefs

from web.models import SquareRoot
from web.models import SquareRootCoefs

from web.models import FileDataPoint



from web.forms import DataForm
from web.forms import SqrtForm
from web.forms import FromFileForm
from web.forms import SquareFuncForm


from web.tool_utils import files_count
from web.tool_utils import make_chart_mplib
from web.tool_utils import make_chart_seaborn
from web.tool_utils import make_chart_bokeh
from web.tool_utils import make_chart_plotly
from web.tool_utils import make_chart_pygal

from web.tool_utils import make_points
from web.tool_utils import str_to_class
from web.tool_utils import get_data_from_file
from web.tool_utils import export_png


from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from bokeh.embed import components


import chart_studio.tools as plotly_tools


@app.route('/data/plot/matplotlib/<string:model_name>')
def route_plot_mplib(model_name):
    fig = make_chart_mplib(model_name)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/data/plot/seaborn/<string:model_name>')
def route_plot_seaborn(model_name):   
    fig = make_chart_seaborn(model_name)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')











@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')
















#C
@app.route("/data/add/main")
def route_add_data_main():
    fromfile_form = FromFileForm()
    return render_template('add_data_main.html', form=fromfile_form)


@app.route("/data/add/<string:model_name>", methods=['GET', 'POST'])
def route_add_data(model_name):
    defaults = ['Sinus', 'Cosinus', 'Exponential']
    if model_name in defaults:
        form = DataForm()
    elif model_name == 'SquareRoot':
        form = SqrtForm()
    elif model_name == 'SquareFunc':
        form = SquareFuncForm()


    if form.validate_on_submit():
        ModelCoefs = str_to_class(model_name + 'Coefs')
        step_value = form.step.data if form.step.data is not None else 0.3
        
        ''' if form has exact structure as this: begin,end,a,b,c,d,step'''
        coefs_kwargs = dict()
        if model_name in defaults or model_name == 'SquareRoot': # default forms and squareroot aswell have this struct
            coefs_kwargs['a'] = form.coef_a.data
            coefs_kwargs['b'] = form.coef_b.data
            coefs_kwargs['c'] = form.coef_c.data
            coefs_kwargs['d'] = form.coef_d.data
            coefs_kwargs['step'] = form.step.data
        elif model_name == 'SquareFunc':
            coefs_kwargs['a'] = form.coef_a.data
            coefs_kwargs['p'] = form.coef_p.data
            coefs_kwargs['q'] = form.coef_q.data
            coefs_kwargs['step'] = form.step.data


        coefs_record = ModelCoefs(**coefs_kwargs)
        # coefs_record = ModelCoefs(a=form.coef_a.data, b=form.coef_b.data, c=form.coef_c.data, d=form.coef_d.data, step=step_value)
        db.session.add(coefs_record)
        db.session.commit()
        make_points(db, form, model_name=model_name, step=step_value)
        db.session.commit()
        flash(f'Range <{form.begin.data}, {form.end.data}> has been successfully added to the database!', 'success')
        return redirect(url_for('route_show_data', model_name=model_name))
    return render_template('add_data.html', form=form, model_name=model_name)

@app.route("/data/add/fromfile", methods=['GET', 'POST'])
def route_add_data_from_file():
    form = FromFileForm()
    filename = form.filename.data

    if form.validate_on_submit():
        x, y = get_data_from_file(filename)
        for xx, yy in zip(x, y):
            pt = FileDataPoint.make_point(xx, yy)
            db.session.add(pt)
        db.session.commit()
        flash(f'Data from {filename} has been successfully added to the database!', 'success')
        return redirect(url_for('route_show_data', model_name='FileDataPoint', filename=filename))
    return render_template('add_data_file.html', form=form)




















#R
@app.route("/data/show/main")
def route_show_data_main():
    return render_template('show_data_main.html')

@app.route("/data/show/<string:model_name>")
def route_show_data(model_name):
    Model = str_to_class(model_name)
    no_coefs_models = ['FileDataPoint']

    if model_name not in no_coefs_models:
        ModelCoefs = str_to_class(model_name+'Coefs')

    points = Model.query.all()
    if not points:
        points = []

    kwargs = dict()
    if model_name != 'FileDataPoint':
        kwargs['coefs'] = ModelCoefs.get_coefs()

    chart = make_chart_bokeh(model_name)
    script_bokeh, div_bokeh = components(chart)
    kwargs["script_bokeh"] = script_bokeh
    kwargs["div_bokeh"] = div_bokeh

    kwargs["script_plotly"] = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script> '
    kwargs["div_plotly"] = make_chart_plotly(model_name)


    chart = make_chart_pygal(model_name)
    kwargs["src_pygal"] = chart.render_data_uri()


    return render_template('show_data.html', points=points, model_name=model_name, **kwargs)
#U































#D
@app.route("/data/delete/<string:model_name>/<int:point_id>", methods=['POST'])
def route_delete_point(model_name, point_id):
    point = str_to_class(model_name).query.get_or_404(point_id)
    db.session.delete(point)
    db.session.commit()
    if not str_to_class(model_name).query.all():
        db.session.delete(str_to_class(model_name + 'Coefs').query.first())
        db.session.commit()
    flash(f'Point ({point.id}) has been succesfully removed from the database.', 'success')
    return redirect(url_for('route_show_data', model_name=model_name))

@app.route("/data/delete/all/<string:model_name>", methods=['POST'])
def route_delete_all_points(model_name):
    Model = str_to_class(model_name)
    all_points = Model.query.all()
    no_coefs_models = ['FileDataPoint']

    if model_name not in no_coefs_models:
        ModelCoefs = str_to_class(model_name+'Coefs')
        coefs = str_to_class(model_name + 'Coefs').query.first()
        if coefs:
            db.session.delete(coefs)
    for point in all_points:
        db.session.delete(point)
    db.session.commit()
    flash(f'All points have been deleted from {model_name}.', 'success')
    return redirect(url_for('route_show_data', model_name=model_name))


@app.route("/summary")
def route_summary():
    return render_template('summary.html')


''' Download images and codes section '''

@app.route("/data/download/mplib/<string:model_name>/<string:filename>")
def route_download_mplib(model_name, filename):
    """ Downloads image and code. """
    now = datetime.now().strftime("%m-%d_%H-%M-%S")
    chart = make_chart_mplib(model_name)
    chart.savefig(f'web/downloads/images/{now}_{filename}')

    code = inspect.getsource(make_chart_mplib)
    fname_nopng = now + '_' + filename.split('.')[0]  
    with open(f'web/downloads/codes/{fname_nopng}.py', 'w') as f:
        f.write(code) 
    flash(f'Matplotlib chart {model_name} model has been downloaded at web/downloads/images/{now}_{filename}.', 'success')
    flash(f'Matplotlib chart {model_name} code has been saved at web/downloads/codes/{now}_{filename}.', 'success')
    return redirect(url_for('route_show_data', model_name=model_name))


@app.route("/data/download/seaborn/<string:model_name>/<string:filename>")
def route_download_seaborn(model_name, filename):
    """ Downloads image and code. """
    now = datetime.now().strftime("%m-%d_%H-%M-%S")
    chart = make_chart_seaborn(model_name)
    chart.savefig(f'web/downloads/images/{now}_{filename}')

    code = inspect.getsource(make_chart_mplib)
    fname_nopng = now + '_' + filename.split('.')[0]  
    with open(f'web/downloads/codes/{fname_nopng}.py', 'w') as f:
        f.write(code) 
    flash(f'Seaborn chart {model_name} model has been downloaded at web/downloads/images/{now}_{filename}.', 'success')
    flash(f'Seaborn chart {model_name} code has been saved at web/downloads/codes/{now}_{filename}.', 'success')
    return redirect(url_for('route_show_data', model_name=model_name))

@app.route("/data/download/bokeh/<string:model_name>/<string:filename>")
def route_download_bokeh(model_name, filename):
    chart = make_chart_bokeh(model_name)
    export_png(chart, filename=f'web/downloads/images/{filename}')
    flash(f'Matplotlib chart {model_name} model has been downloaded at web/downloads/images/{filename}.', 'success')
    return redirect(url_for('route_show_data', model_name=model_name))


@app.route("/matplotlib")
def route_matplotlib():
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

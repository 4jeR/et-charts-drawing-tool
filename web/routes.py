import io
import os
import json

from flask import Flask
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import Response

from datetime import datetime
from io import BytesIO

from web import app
from web import db

from web.import_forms import *
from web.import_models import *

from web.tool_utils import files_count
from web.tool_utils import make_chart_matplotlib
from web.tool_utils import make_chart_seaborn
from web.tool_utils import make_chart_bokeh
from web.tool_utils import make_chart_plotly
from web.tool_utils import make_chart_pygal
from web.tool_utils import make_points
from web.tool_utils import str_to_object
from web.tool_utils import get_data_from_file
from web.tool_utils import download_image
from web.tool_utils import get_current_time
from web.tool_utils import save_source_code

from bokeh.embed import components as bokeh_components

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg


import chart_studio.tools as plotly_tools


@app.route('/data/plot/matplotlib/<string:model_name>/<string:options>')
def route_plot_matplotlib(model_name, options):
    """ Returns the Response consisting the matplotlib chart image. """
    options_from_string = json.loads(options)
    fig = make_chart_matplotlib(model_name, options_from_string)
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/data/plot/seaborn/<string:model_name>')
def route_plot_seaborn(model_name):
    """ Returns the Response consisting the Seaborn chart image. """
    fig = make_chart_seaborn(model_name)
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route("/")
@app.route("/home")
def home():
    """ Renders home page. """
    return render_template('home.html')


# C
@app.route("/data/add/main")
def route_add_data_main():
    """ Renders main entry point for inserting the data. """
    fromfile_form = FromFileForm()
    return render_template('add_data_main.html', form=fromfile_form)





@app.route("/data/add/<string:model_name>", methods=['GET', 'POST'])
def route_add_data(model_name):
    """ Inserts points to the database to the specific model based on values from forms."""
    defaults = ['Sinus', 'Cosinus', 'Exponential']
    if model_name in defaults:
        form = DataForm()
    elif model_name == 'SquareRoot':
        form = SqrtForm()
    elif model_name == 'SquareFunc':
        form = SquareFuncForm()

    if form.validate_on_submit():
        ModelCoefs = str_to_object(model_name + 'Coefs')
        step_value = form.step.data if form.step.data is not None else 0.3

        ''' if form has exact structure as this: begin,end,a,b,c,d,step'''
        coefs_kwargs = dict()
        # default forms and squareroot aswell have this struct
        if model_name in defaults or model_name == 'SquareRoot':
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
    """ End point for adding the data from file."""
    form = FromFileForm()
    filename = form.filename.data

    if form.validate_on_submit():
        x, y = get_data_from_file(filename)
        for xx, yy in zip(x, y):
            pt = FileDataPoint.make_point(xx, yy)
            db.session.add(pt)
        db.session.commit()
        flash(
            f'Data from {filename} has been successfully added to the database!', 'success')
        return redirect(url_for('route_show_data', model_name='FileDataPoint', filename=filename))
    return render_template('add_data_file.html', form=form)


# R
@app.route("/data/show/main")
def route_show_data_main():
    """ Renders main web page on which you can choose different models. """
    return render_template('show_data_main.html')


@app.route("/data/show/<string:model_name>")
def route_show_data(model_name):
    """ 
    Renders end point on which are shown:
    data table with all points for specific model,
    five charts for each library: Matplotlib, Seaborn, Bokeh, Plotly and Pygal.
    """
    Model = str_to_object(model_name)
    no_coefs_models = ['FileDataPoint'] # TODO: custom user input model - as factory class generator?

    if model_name not in no_coefs_models:
        ModelCoefs = str_to_object(model_name+'Coefs')

    points = Model.query.all()
    if not points:
        points = []


    kw_options = dict()
    # parse dictionary of options from database to string
    kw_options['matplotlib_options'] = json.dumps(MatplotlibPlotOptions.get_options()) 
    # kw_options['seaborn_options'] = json.dumps(SeabornPlotOptions.get_options()) 
    kw_options['bokeh_options'] = json.dumps(BokehPlotOptions.get_options()) 
    # kw_options['plotly_options'] = json.dumps(PlotlyPlotOptions.get_options()) 
    # kw_options['pygal_options'] = json.dumps(PygalPlotOptions.get_options()) 

    ''' get all model charts'''
    kwargs = dict()

    if model_name != 'FileDataPoint':
        kwargs['coefs'] = ModelCoefs.get_coefs()

    chart = make_chart_bokeh(model_name)
    script_bokeh, div_bokeh = bokeh_components(chart)
    kwargs["script_bokeh"] = script_bokeh
    kwargs["div_bokeh"] = div_bokeh

    kwargs["script_plotly"] = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script> '
    kwargs["div_plotly"] = make_chart_plotly(model_name)

    chart = make_chart_pygal(model_name)
    kwargs["src_pygal"] = chart.render_data_uri()

    kwforms = dict()
    kwforms['matplotlib_form'] = MatplotlibOptionsForm()

    return render_template('show_data.html', points=points, model_name=model_name, **kwargs, **kwforms, **kw_options)


# U
@app.route("/data/change_options/matplotlib/<string:model_name>", methods=['GET', 'POST'])
def route_change_options_matplotlib(model_name):
    """ Inserts new option OptionsForm."""
    matplotlib_form = MatplotlibOptionsForm()

    if matplotlib_form.validate_on_submit():
        kwargs = dict()
        kwargs['color'] = matplotlib_form.color.data
        kwargs['line_width'] = matplotlib_form.line_width.data
        kwargs['line_style'] = matplotlib_form.line_style.data
        kwargs['marker'] = matplotlib_form.marker.data

        kwargs['flag_scatter_plot'] = matplotlib_form.flag_scatter_plot.data
        kwargs['flag_show_grid'] = matplotlib_form.flag_show_grid.data
        kwargs['flag_logscale_y'] = matplotlib_form.flag_logscale_y.data
        kwargs['flag_show_legend'] = matplotlib_form.flag_show_legend.data

        new_options = MatplotlibPlotOptions(**kwargs)

        ''' replace old with new options '''
        old_options = MatplotlibPlotOptions.query.first()
        db.session.delete(old_options)
        db.session.commit()

        db.session.add(new_options)
        db.session.commit()
        flash(f'Changed options for Matplotlib!', 'success')
        return redirect(url_for('route_show_data', model_name=model_name))

#TODO: Seaborn options form + route


@app.route("/data/change_options/bokeh/<string:model_name>", methods=['GET', 'POST'])
def route_change_options_bokeh(model_name):
    """ Inserts new option OptionsForm."""
    bokeh_form = BokehOptionsForm()

    if bokeh_form.validate_on_submit():
        kwargs = dict()
        kwargs['color'] = bokeh_form.color.data
        kwargs['line_width'] = bokeh_form.line_width.data
        kwargs['line_style'] = bokeh_form.line_style.data
        kwargs['marker'] = bokeh_form.marker.data

        kwargs['flag_scatter_plot'] = bokeh_form.flag_scatter_plot.data
        kwargs['flag_show_grid'] = bokeh_form.flag_show_grid.data
        kwargs['flag_logscale_y'] = bokeh_form.flag_logscale_y.data
        kwargs['flag_show_legend'] = bokeh_form.flag_show_legend.data

        new_options = BokehPlotOptions(**kwargs)

        ''' replace old with new options '''
        old_options = BokehPlotOptions.query.first()
        db.session.delete(old_options)
        db.session.commit()

        db.session.add(new_options)
        db.session.commit()
        flash(f'Changed options for Bokeh!', 'success')
        return redirect(url_for('route_show_data', model_name=model_name))

#TODO: Plotly options form + route
#TODO: Pygal options form + route


# D
@app.route("/data/delete/<string:model_name>/<int:point_id>", methods=['POST'])
def route_delete_point(model_name, point_id):
    """ Deletes chosen point from the database and redirects again on `route_show_data` route. """
    point = str_to_object(model_name).query.get_or_404(point_id)
    db.session.delete(point)
    db.session.commit()
    if not str_to_object(model_name).query.all():
        db.session.delete(str_to_object(model_name + 'Coefs').query.first())
        db.session.commit()
    flash(f'Point ({point.id}) has been succesfully removed from the database.', 'success')
    return redirect(url_for('route_show_data', model_name=model_name))


@app.route("/data/delete/all/<string:model_name>", methods=['POST'])
def route_delete_all_points(model_name):
    Model = str_to_object(model_name)
    all_points = Model.query.all()
    no_coefs_models = ['FileDataPoint']

    if model_name not in no_coefs_models:
        ModelCoefs = str_to_object(model_name + 'Coefs')
        coefs = ModelCoefs.query.first()
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
@app.route("/data/download/<string:library_name>/<string:model_name>/<string:save_img>/<string:save_src>", methods=['GET', 'POST'])
def route_download_src_img(library_name, model_name, save_img, save_src):
    """ Downloads image and code for given chart library name. """
    now = get_current_time()

    if save_img == '1':
        filename_png = f'{library_name}_{model_name}.png'
        download_image(library_name, model_name, now)
        flash(f'{library_name} chart {model_name} model has been downloaded at web/downloads/images/{now}_{filename_png}.', 'success')
    if save_src == '1':
        filename_py = f'{library_name}_{model_name}.py'
        save_source_code(library_name, model_name, now)
        flash(f'{library_name} chart {model_name} code has been saved at web/downloads/codes/{now}_{filename_py}.', 'success')
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

import io
import os
import json

from flask import Flask
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import Response
from flask import request

from datetime import datetime
from io import BytesIO

from web import app
from web import db
# from web import cache


from web.import_forms import *
from web.import_models import *

from web.help_utils import files_count

from web.help_utils import make_chart_matplotlib
from web.help_utils import make_chart_seaborn
from web.help_utils import make_chart_bokeh
from web.help_utils import make_chart_plotly
from web.help_utils import make_chart_pygal

from web.help_utils import make_points
from web.help_utils import str_to_object
from web.help_utils import download_image
from web.help_utils import get_current_time
from web.help_utils import save_source_code
from web.help_utils import get_data_from_file
from web.help_utils import get_recently_added_record
from web.help_utils import clean_query
from web.help_utils import string_to_mathjax

from web.help_utils import get_default_matplotlib_options
from web.help_utils import get_default_seaborn_options
from web.help_utils import get_default_bokeh_options
from web.help_utils import get_default_plotly_options
from web.help_utils import get_default_pygal_options

from bokeh.embed import components as bokeh_components

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

import chart_studio.tools as plotly_tools


@app.route('/data/plot/matplotlib/<string:model_name>/<string:options>')
@app.route('/data/plot/matplotlib/<string:model_name>/<string:options>/<int:chart_id>')
@app.route('/data/plot/matplotlib/<string:model_name>/<string:options>/<string:data_filename>')
def route_plot_matplotlib(model_name, options, chart_id=-1, data_filename=''):
    """ Returns the Response consisting the matplotlib chart image. """
    options_from_string = json.loads(options)
    fig = make_chart_matplotlib(model_name, chart_id, options_from_string, data_filename)
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/data/plot/seaborn/<string:model_name>/<string:options>')
@app.route('/data/plot/seaborn/<string:model_name>/<string:options>/<int:chart_id>')
@app.route('/data/plot/seaborn/<string:model_name>/<string:options>/<string:data_filename>')
def route_plot_seaborn(model_name, options, chart_id=-1, data_filename=''):
    """ Returns the Response consisting the Seaborn chart image. """
    options_from_string = json.loads(options)
    fig = make_chart_seaborn(model_name, chart_id, options_from_string, data_filename)
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route("/")
@app.route("/home")
def home():
    """ Renders home page. """
    return render_template('home.html')


@app.route("/data/add/main")
def route_add_data_main():
    """ Renders page on which all models can be added do the database. """
    return render_template('add_data_main.html')


@app.route("/data/add/<string:model_name>", methods=['POST'])
@clean_query(db=db)
def route_add_data(model_name):
    """ Inserts points to the database to the specific model based on values from forms."""
    common_models = ['Sinus', 'Cosinus', 'Exponential']
    if model_name in common_models:
        form = DataForm()
    elif model_name == 'SquareRoot':
        form = SqrtForm()
    elif model_name == 'SquareFunc':
        form = SquareFuncForm()
    elif model_name == 'CustomEquation':
        form = CustomEquationForm()


    if form.validate_on_submit():
        Model = str_to_object(model_name)
        form_step_data = form.step.data if form.step.data is not None else 0.1

        ''' if form has exact structure as this: begin,end,a,b,c,d,step'''
        model_kwargs = dict()
        model_kwargs['x_begin'] = form.begin.data
        model_kwargs['x_end'] = form.end.data
        model_kwargs['step'] = form_step_data

        model_kwargs['id_matplotlib_options'] = get_default_matplotlib_options(db, as_dict=False).id
        model_kwargs['id_seaborn_options'] = get_default_seaborn_options(db, as_dict=False).id
        model_kwargs['id_bokeh_options'] = get_default_bokeh_options(db, as_dict=False).id
        model_kwargs['id_plotly_options'] = get_default_plotly_options(db, as_dict=False).id
        model_kwargs['id_pygal_options'] = get_default_pygal_options(db, as_dict=False).id
        

        if model_name in common_models or model_name == 'SquareRoot':
            model_kwargs['a'] = form.coef_a.data
            model_kwargs['b'] = form.coef_b.data
            model_kwargs['c'] = form.coef_c.data
            model_kwargs['d'] = form.coef_d.data
        elif model_name == 'SquareFunc':
            model_kwargs['a'] = form.coef_a.data
            model_kwargs['p'] = form.coef_p.data
            model_kwargs['q'] = form.coef_q.data
        elif model_name == 'CustomEquation':
            model_kwargs['equation'] = form.equation.data

        model_object = Model(**model_kwargs)
        db.session.add(model_object)
        db.session.commit()
        
        chart_id = get_recently_added_record(db, model_name).id

        flash(f'Range <{form.begin.data}, {form.end.data}> has been successfully added to the database!', 'success')
        return redirect(url_for('route_show_data', model_name=model_name, chart_id=chart_id))
    return render_template('add_data.html', form=form, model_name=model_name)


@app.route("/data/fromfile", methods=['GET', 'POST'])
@clean_query(db=db)
def route_add_data_from_file():
    """ End point for adding the data from file."""
    form = FromFileForm()
    filename = form.filename.data

    if form.validate_on_submit():

        get_default_matplotlib_options(db)
        mplib_id = MatplotlibPlotOptions.query.first().id
        
        get_default_seaborn_options(db)
        seaborn_id = SeabornPlotOptions.query.first().id

        get_default_bokeh_options(db)
        bokeh_id = BokehPlotOptions.query.first().id


        get_default_plotly_options(db)
        plotly_id = PlotlyPlotOptions.query.first().id
        
        get_default_pygal_options(db)
        pygal_id = PlotlyPlotOptions.query.first().id


        fpo = FilePlotOptions(
            id_matplotlib_options=mplib_id, 
            id_seaborn_options=seaborn_id, 
            id_bokeh_options=bokeh_id, 
            id_plotly_options=plotly_id, 
            id_pygal_options=pygal_id
        )
        db.session.add(fpo)

        ''' delete old points '''
        previous_data_points = FileDataPoint.query.all()
        if previous_data_points:
            for point_record in previous_data_points:
                db.session.delete(point_record)
            db.session.commit()
        ''' delete old options '''


        x, y = get_data_from_file(filename)
        for xx, yy in zip(x, y):
            pt = FileDataPoint.make_point(xx, yy)
            db.session.add(pt)
        db.session.commit()
        flash(f'Data from {filename} has been successfully added to the database!', 'success')
        return redirect(url_for('route_show_data_from_file'))
    return render_template('add_data_file.html', form=form)


@app.route("/data/show/main")
def route_show_data_main():
    """ Renders main web page on which you can choose different models. """
    return render_template('show_data_main.html')


@app.route("/data/show/fromfile", methods=['GET'])
def route_show_data_from_file():
    Model = str_to_object("FileDataPoint")
    records = Model.query.all()

    kw_options = dict()

    ''' Get options for each library. '''
    matplotlib_options_id = FilePlotOptions.query.first().id_matplotlib_options
    kw_options['matplotlib_options'] = json.dumps(MatplotlibPlotOptions.get_options(matplotlib_options_id))

    seaborn_options_id = FilePlotOptions.query.first().id_seaborn_options
    kw_options['seaborn_options'] = json.dumps(SeabornPlotOptions.get_options(seaborn_options_id))

    bokeh_options_id = FilePlotOptions.query.first().id_bokeh_options
    kw_options['bokeh_options'] = BokehPlotOptions.get_options(bokeh_options_id) 

    plotly_options_id = FilePlotOptions.query.first().id_plotly_options
    kw_options['plotly_options'] = PlotlyPlotOptions.get_options(plotly_options_id) 

    pygal_options_id = FilePlotOptions.query.first().id_pygal_options
    kw_options['pygal_options'] = PygalPlotOptions.get_options(pygal_options_id) 


    kwargs = dict()

    bokeh_chart = make_chart_bokeh("FileDataPoint", -1, kw_options.get('bokeh_options', dict()))
    script_bokeh, div_bokeh = bokeh_components(bokeh_chart)
    kwargs["script_bokeh"] = script_bokeh
    kwargs["div_bokeh"] = div_bokeh

    kwargs["script_plotly"] = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script> '
    kwargs["div_plotly"] = make_chart_plotly("FileDataPoint", -1, kw_options.get('plotly_options', dict()))

    pygal_chart = make_chart_pygal("FileDataPoint", -1, kw_options.get('pygal_options', dict()))
    kwargs["src_pygal"] = pygal_chart.render_data_uri()

    ''' Pass all forms to be shown (view)'''
    kwforms = dict()
    kwforms['matplotlib_form'] = MatplotlibOptionsForm()
    kwforms['seaborn_form'] = SeabornOptionsForm()
    kwforms['bokeh_form'] = BokehOptionsForm()
    kwforms['plotly_form'] = PlotlyOptionsForm()
    kwforms['pygal_form'] = PygalOptionsForm()

    return render_template('show_data.html', model_name="FileDataPoint", chart_id=-1, records=records,  **kwargs, **kwforms, **kw_options)


@app.route("/data/show/<string:model_name>", methods=['GET'])
@app.route("/data/show/<string:model_name>/<int:chart_id>", methods=['GET', 'POST'])
def route_show_data(model_name, chart_id=-1):
    """ 
    Renders end point on which are shown:
    data table with all points for specific model,
    five charts for each library: Matplotlib, Seaborn, Bokeh, Plotly and Pygal.
    """
    
    Model = str_to_object(model_name)
    records = Model.query.all()

    kw_options = dict()
    if chart_id != -1 and model_name != "FileDataPoint":
        ''' Get options for each library. '''
        current_chart = Model.query.get(chart_id)

        matplotlib_options_id = current_chart.id_matplotlib_options
        kw_options['matplotlib_options'] = json.dumps(MatplotlibPlotOptions.get_options(matplotlib_options_id))

        seaborn_options_id = current_chart.id_seaborn_options
        kw_options['seaborn_options'] = json.dumps(SeabornPlotOptions.get_options(seaborn_options_id))

        bokeh_options_id = current_chart.id_bokeh_options
        kw_options['bokeh_options'] = BokehPlotOptions.get_options(bokeh_options_id) 

        plotly_options_id = current_chart.id_plotly_options
        kw_options['plotly_options'] = PlotlyPlotOptions.get_options(plotly_options_id) 

        pygal_options_id = current_chart.id_pygal_options
        kw_options['pygal_options'] = PygalPlotOptions.get_options(pygal_options_id) 

    elif chart_id == -1 and model_name == "FileDataPoint":
        ''' Get options for each library. '''
        current_chart = FilePlotOptions.query.first()
        
        matplotlib_options_id = current_chart.id_matplotlib_options
        kw_options['matplotlib_options'] = json.dumps(MatplotlibPlotOptions.get_options(matplotlib_options_id))

        seaborn_options_id = current_chart.id_seaborn_options
        kw_options['seaborn_options'] = json.dumps(SeabornPlotOptions.get_options(seaborn_options_id))

        bokeh_options_id = current_chart.id_bokeh_options
        kw_options['bokeh_options'] = BokehPlotOptions.get_options(bokeh_options_id) 

        plotly_options_id = current_chart.id_plotly_options
        kw_options['plotly_options'] = PlotlyPlotOptions.get_options(plotly_options_id) 

        pygal_options_id = current_chart.id_pygal_options
        kw_options['pygal_options'] = PygalPlotOptions.get_options(pygal_options_id) 

    getable_models = ['Sinus', 'Cosinus', 'SquareRoot', 'Exponential', 'SquareFunc']

    kwargs = dict()

    if model_name in getable_models:
        kwargs['coefs'] = Model.get_coefs(chart_id)
    elif chart_id != -1 and model_name == 'CustomEquation':
        current_chart = Model.query.get(chart_id)
        kwargs['custom_equation'] = string_to_mathjax(current_chart)


    bokeh_chart = make_chart_bokeh(model_name, chart_id, kw_options.get('bokeh_options', dict()))
    script_bokeh, div_bokeh = bokeh_components(bokeh_chart)
    kwargs["script_bokeh"] = script_bokeh
    kwargs["div_bokeh"] = div_bokeh

    kwargs["script_plotly"] = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script> '
    kwargs["div_plotly"] = make_chart_plotly(model_name, chart_id, kw_options.get('plotly_options', dict()))

    pygal_chart = make_chart_pygal(model_name, chart_id, kw_options.get('pygal_options', dict()))
    kwargs["src_pygal"] = pygal_chart.render_data_uri()

    ''' Pass all forms to be shown (view)'''
    kwforms = dict()
    kwforms['matplotlib_form'] = MatplotlibOptionsForm()
    kwforms['seaborn_form'] = SeabornOptionsForm()
    kwforms['bokeh_form'] = BokehOptionsForm()
    kwforms['plotly_form'] = PlotlyOptionsForm()
    kwforms['pygal_form'] = PygalOptionsForm()

    return render_template('show_data.html', model_name=model_name, chart_id=chart_id, records=records,  **kwargs, **kwforms, **kw_options)


@app.route("/data/change/coefs/<string:model_name>/<int:chart_id>", methods=['POST'])
@clean_query(db=db)
def route_change_coefs(model_name, chart_id=-1):
    Model = str_to_object(model_name)
    model_object = Model.query.get(chart_id)
    

    common_models = ['Sinus', 'Cosinus', 'Exponential']
    if model_name in common_models:
        form = DataForm()
    elif model_name == 'SquareRoot':
        form = SqrtForm()
    elif model_name == 'SquareFunc':
        form = SquareFuncForm()
    elif model_name == 'CustomEquation':
        form = CustomEquationForm()

    coefs = Model.get_coefs(chart_id)    

    if form.validate_on_submit():
        if model_name in common_models or model_name == 'SquareRoot':
            model_object.a = form.coef_a.data
            model_object.b = form.coef_b.data
            model_object.c = form.coef_c.data
            model_object.d = form.coef_d.data
        elif model_name == 'SquareFunc':
            model_object.a = form.coef_a.data
            model_object.p = form.coef_p.data
            model_object.q = form.coef_q.data

        
        
        db.session.commit()
        
        flash(f'Changed coefficients for {chart_id} {model_name}!', 'success')
        return redirect(url_for('route_show_data', model_name=model_name, chart_id=chart_id))
    return render_template("change_data.html", model_name=model_name, chart_id=chart_id, form=form, coefs=coefs)
    

@app.route("/data/change/options/<string:library_name>/<string:model_name>", methods=['GET', 'POST'])
@app.route("/data/change/options/<string:library_name>/<string:model_name>/<int:chart_id>", methods=['GET', 'POST'])
@clean_query(db=db)
def route_change_options(library_name, model_name, chart_id=-1):
    """ Inserts new option OptionsForm."""
    Model = str_to_object(model_name)
    LPO = str_to_object(f'{library_name.capitalize()}PlotOptions')
    LOF = str_to_object(f'{library_name.capitalize()}OptionsForm')
    id_library_options = f'id_{library_name}_options'

    ''' Get values from form. '''
    library_form = LOF()

    if library_form.validate_on_submit():
        kwargs = dict()
        kwargs['color'] = library_form.color.data
        kwargs['bg_color'] = library_form.bg_color.data
        kwargs['line_width'] = library_form.line_width.data
        kwargs['outline_color'] = library_form.outline_color.data
        kwargs['line_style'] = library_form.line_style.data
        kwargs['marker'] = library_form.marker.data

        if library_name != 'seaborn':
            kwargs['flag_bar_plot'] = library_form.flag_bar_plot.data
        kwargs['flag_scatter_plot'] = library_form.flag_scatter_plot.data
        kwargs['flag_show_grid'] = library_form.flag_show_grid.data

        kwargs['x_label'] = library_form.x_label.data
        kwargs['y_label'] = library_form.y_label.data
        kwargs['title'] = library_form.title.data

        if library_name != 'pygal':
            kwargs['flag_logscale_x'] = library_form.flag_logscale_x.data
        kwargs['flag_logscale_y'] = library_form.flag_logscale_y.data

        new_options = LPO(**kwargs)
        db.session.add(new_options)
        db.session.commit()

        ''' get lastly_added record '''
        recently_added = get_recently_added_record(db, LPO.__name__)
        new_options_id = recently_added.id


        if model_name != "FileDataPoint" and chart_id != -1:
            current_chart = Model.query.get(chart_id)
            setattr(current_chart, id_library_options, new_options_id) 
            db.session.commit()
        else:
            fpo_record = FilePlotOptions.query.first()
            setattr(fpo_record, id_library_options, new_options_id) 
            db.session.commit()

        flash(f'Changed options for {library_name}!', 'success')
        if model_name == "FileDataPoint" and chart_id == -1:
            return redirect(url_for('route_show_data_from_file'))
        else:
            return redirect(url_for('route_show_data', model_name=model_name, chart_id=chart_id))


@app.route("/data/delete/<string:model_name>/<int:chart_id>", methods=['POST'])
@clean_query(db=db)
def route_delete_chart(model_name, chart_id):
    """ Deletes chosen point from the database and redirects again on `route_show_data` route. """
    Model = str_to_object(model_name)
    chart = Model.query.get_or_404(chart_id)
    db.session.delete(chart)
    db.session.commit()
    flash(f'Chart ({chart.id}) has been succesfully removed from the database.', 'success')
    chart = get_recently_added_record(db, model_name)
    if chart:
        return redirect(url_for('route_show_data', model_name=model_name, chart_id=chart.id))
    return redirect(url_for('route_show_data', model_name=model_name))


# @app.route("/data/delete/all/<string:model_name>", methods=['POST'])
# @clean_query(db=db)
# def route_delete_all_charts(model_name):
#     ''' Deletes all records from model. '''
#     Model = str_to_object(model_name)
#     all_charts = Model.query.delete()
#     db.session.commit()
#     flash(f'{all_charts} charts have been deleted from {model_name}.', 'success')
#     return redirect(url_for('route_show_data', model_name=model_name))


@app.route("/summary")
def route_summary():
    return render_template('summary.html')


@app.route("/data/download/<string:library_name>/<string:save_img>/<string:save_src>", methods=['GET', 'POST'])
@app.route("/data/download/<string:library_name>/<string:model_name>/<string:save_img>/<string:save_src>", methods=['GET', 'POST'])
@app.route("/data/download/<string:library_name>/<string:model_name>/<int:chart_id>/<string:save_img>/<string:save_src>", methods=['GET', 'POST'])
def route_download_src_img(library_name, model_name="FileDataPoint", chart_id=-1, save_img='0', save_src='0'):
    """ Downloads image and code for given chart library name. """
    now = get_current_time()

    if save_img == '1':
        filename_png = f'{library_name}_{model_name}.png'
        download_image(library_name, model_name, chart_id, now)
        flash(f'{library_name} chart {model_name} model has been downloaded at web/downloads/images/{now}_{filename_png}.', 'success')
    if save_src == '1':
        filename_py = f'{library_name}_{model_name}.py'
        save_source_code(library_name, model_name, chart_id, now)
        flash(f'{library_name} chart {model_name} code has been saved at web/downloads/codes/{now}_{filename_py}.', 'success')
    
    if model_name == "FileDataPoint" and chart_id == -1:
        return redirect(url_for('route_show_data_from_file'))
    else:
        return redirect(url_for('route_show_data', model_name=model_name, chart_id=chart_id))


@app.route("/matplotlib")
def route_matplotlib():
    path_to_images = os.getcwd() + '/web/downloads/images'
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

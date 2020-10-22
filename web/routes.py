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
# from web import cache

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
from web.tool_utils import download_image
from web.tool_utils import get_current_time
from web.tool_utils import save_source_code
from web.tool_utils import get_data_from_file
from web.tool_utils import get_recently_added_record
from web.tool_utils import clean_query



from web.tool_utils import get_default_matplotlib_options
from web.tool_utils import get_default_seaborn_options
from web.tool_utils import get_default_bokeh_options
from web.tool_utils import get_default_plotly_options
from web.tool_utils import get_default_pygal_options


from bokeh.embed import components as bokeh_components

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg


import chart_studio.tools as plotly_tools


@app.route('/data/plot/matplotlib/<string:model_name>/<string:options>')
@app.route('/data/plot/matplotlib/<string:model_name>/<string:options>/<int:chart_id>')
def route_plot_matplotlib(model_name, options, chart_id=-1):
    """ Returns the Response consisting the matplotlib chart image. """
    options_from_string = json.loads(options)
    fig = make_chart_matplotlib(model_name, chart_id, options_from_string)
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/data/plot/seaborn/<string:model_name>/<string:options>')
@app.route('/data/plot/seaborn/<string:model_name>/<string:options>/<int:chart_id>')
def route_plot_seaborn(model_name, options, chart_id=-1):
    """ Returns the Response consisting the Seaborn chart image. """
    options_from_string = json.loads(options)
    fig = make_chart_seaborn(model_name, chart_id, options_from_string)
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
        Model = str_to_object(model_name)
        form_step_data = form.step.data if form.step.data is not None else 0.1

        ''' if form has exact structure as this: begin,end,a,b,c,d,step'''
        model_kwargs = dict()
        # default forms and squareroot aswell have this struct
        model_kwargs['x_begin'] = form.begin.data
        model_kwargs['x_end'] = form.end.data
        model_kwargs['step'] = form_step_data


        model_kwargs['id_matplotlib_options'] = get_default_matplotlib_options(db).id
        model_kwargs['id_seaborn_options'] = get_default_seaborn_options(db).id
        model_kwargs['id_bokeh_options'] = get_default_bokeh_options(db).id
        model_kwargs['id_plotly_options'] = get_default_plotly_options(db).id
        model_kwargs['id_pygal_options'] = get_default_pygal_options(db).id
        
         

        if model_name in defaults or model_name == 'SquareRoot':
            model_kwargs['a'] = form.coef_a.data
            model_kwargs['b'] = form.coef_b.data
            model_kwargs['c'] = form.coef_c.data
            model_kwargs['d'] = form.coef_d.data
        elif model_name == 'SquareFunc':
            model_kwargs['a'] = form.coef_a.data
            model_kwargs['p'] = form.coef_p.data
            model_kwargs['q'] = form.coef_q.data

        model_object = Model(**model_kwargs)
        db.session.add(model_object)
        db.session.commit()
        
        chart_id = get_recently_added_record(db, model_name).id


        flash(f'Range <{form.begin.data}, {form.end.data}> has been successfully added to the database!', 'success')
        return redirect(url_for('route_show_data', model_name=model_name, chart_id=chart_id))
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

@app.route("/data/show/<string:model_name>", methods=['GET', 'POST'])
@app.route("/data/show/<string:model_name>/<int:chart_id>", methods=['GET', 'POST'])
def route_show_data(model_name, chart_id=-1):
    """ 
    Renders end point on which are shown:
    data table with all points for specific model,
    five charts for each library: Matplotlib, Seaborn, Bokeh, Plotly and Pygal.
    """
    Model = str_to_object(model_name)
    charts = Model.query.all()

    kw_options = dict()

    if chart_id != -1:
        ''' Get options for each library. '''
        # parse dictionary of options from database to string
        matplotlib_options_id = Model.query.get(chart_id).id_matplotlib_options
        kw_options['matplotlib_options'] = json.dumps(MatplotlibPlotOptions.get_options(matplotlib_options_id))

        seaborn_options_id = Model.query.get(chart_id).id_seaborn_options
        kw_options['seaborn_options'] = json.dumps(SeabornPlotOptions.get_options(seaborn_options_id))

        bokeh_options_id = Model.query.get(chart_id).id_bokeh_options
        kw_options['bokeh_options'] = BokehPlotOptions.get_options(bokeh_options_id) 

        plotly_options_id = Model.query.get(chart_id).id_plotly_options
        kw_options['plotly_options'] = PlotlyPlotOptions.get_options(plotly_options_id) 

        pygal_options_id = Model.query.get(chart_id).id_pygal_options
        kw_options['pygal_options'] = PygalPlotOptions.get_options(pygal_options_id) 
        


    getable_models = ['Sinus', 'Cosinus', 'SquareRoot', 'Exponential', 'SquareFunc']

    ''' get all model charts'''
    kwargs = dict()

    if model_name in getable_models:
        kwargs['coefs'] = Model.get_coefs(chart_id)

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
    # kwforms['seaborn_form'] = SeabornOptionsForm()
    kwforms['bokeh_form'] = BokehOptionsForm()
    kwforms['plotly_form'] = PlotlyOptionsForm()
    # kwforms['pygal_form'] = PygalOptionsForm()

    return render_template('show_data.html', model_name=model_name, chart_id=chart_id, charts=charts,  **kwargs, **kwforms, **kw_options)


@app.route("/data/change_options/matplotlib/<string:model_name>", methods=['GET', 'POST'])
@app.route("/data/change_options/matplotlib/<string:model_name>/<int:chart_id>", methods=['GET', 'POST'])
@clean_query(db=db)
def route_change_options_matplotlib(model_name, chart_id=-1):
    """ Inserts new option OptionsForm."""
    Model = str_to_object(model_name)
    ''' Get values from form. '''
    matplotlib_form = MatplotlibOptionsForm()

    if matplotlib_form.validate_on_submit():
        kwargs = dict()
        kwargs['color'] = matplotlib_form.color.data
        kwargs['bg_color'] = matplotlib_form.bg_color.data
        kwargs['line_width'] = matplotlib_form.line_width.data
        kwargs['line_style'] = matplotlib_form.line_style.data
        kwargs['marker'] = matplotlib_form.marker.data

        kwargs['flag_scatter_plot'] = matplotlib_form.flag_scatter_plot.data
        kwargs['flag_show_grid'] = matplotlib_form.flag_show_grid.data
        kwargs['flag_logscale_x'] = matplotlib_form.flag_logscale_x.data
        kwargs['flag_logscale_y'] = matplotlib_form.flag_logscale_y.data

        ''' make new instance of options '''
        new_options = MatplotlibPlotOptions(**kwargs)
        ''' append new record '''
        db.session.add(new_options)
        db.session.commit()

        ''' get lastly_added record '''
        recently_added = get_recently_added_record(db, 'MatplotlibPlotOptions')
        new_options_id = recently_added.id

        ''' get old options to be replaced and after replacing, delete the old'''
        current_chart = Model.query.get(chart_id)
        

        current_chart.id_matplotlib_options = new_options_id

        db.session.commit()

        flash(f'Changed options for Matplotlib!', 'success')
        return redirect(url_for('route_show_data', model_name=model_name, chart_id=chart_id))

#TODO: Seaborn options form + route


@app.route("/data/change_options/bokeh/<string:model_name>", methods=['GET', 'POST'])
@app.route("/data/change_options/bokeh/<string:model_name>/<int:chart_id>", methods=['GET', 'POST'])
@clean_query(db=db)
def route_change_options_bokeh(model_name, chart_id=-1):
    """ Inserts new option OptionsForm."""
    Model = str_to_object(model_name)
    ''' Get values from form. '''
    bokeh_form = BokehOptionsForm()

    if bokeh_form.validate_on_submit():
        kwargs = dict()
        kwargs['color'] = bokeh_form.color.data
        kwargs['bg_color'] = bokeh_form.bg_color.data
        kwargs['line_width'] = bokeh_form.line_width.data
        kwargs['line_style'] = bokeh_form.line_style.data
        kwargs['marker'] = bokeh_form.marker.data

        kwargs['flag_scatter_plot'] = bokeh_form.flag_scatter_plot.data
        kwargs['flag_show_grid'] = bokeh_form.flag_show_grid.data
        kwargs['flag_logscale_x'] = bokeh_form.flag_logscale_x.data
        kwargs['flag_logscale_y'] = bokeh_form.flag_logscale_y.data

        new_options = BokehPlotOptions(**kwargs)
        ''' append new record '''
        db.session.add(new_options)
        db.session.commit()

        ''' get lastly_added record '''
        recently_added = get_recently_added_record(db, 'BokehPlotOptions')
        new_options_id = recently_added.id

        ''' get old options to be replaced and after replacing, delete the old'''
        current_chart = Model.query.get(chart_id)

        current_chart.id_bokeh_options = new_options_id

        db.session.commit()
        flash(f'Changed options for Bokeh!', 'success')
        return redirect(url_for('route_show_data', model_name=model_name, chart_id=chart_id))


@app.route("/data/change_options/plotly/<string:model_name>", methods=['GET', 'POST'])
@app.route("/data/change_options/plotly/<string:model_name>/<int:chart_id>", methods=['GET', 'POST'])
@clean_query(db=db)
def route_change_options_plotly(model_name, chart_id=-1):
    """ Inserts new option OptionsForm."""
    Model = str_to_object(model_name)
    ''' Get values from form. '''
    plotly_form = PlotlyOptionsForm()

    if plotly_form.validate_on_submit():
        kwargs = dict()
        kwargs['color'] = plotly_form.color.data
        kwargs['bg_color'] = plotly_form.bg_color.data
        kwargs['line_width'] = plotly_form.line_width.data
        kwargs['line_style'] = plotly_form.line_style.data
        kwargs['marker'] = plotly_form.marker.data

        kwargs['flag_scatter_plot'] = plotly_form.flag_scatter_plot.data
        kwargs['flag_show_grid'] = plotly_form.flag_show_grid.data
        kwargs['flag_logscale_x'] = plotly_form.flag_logscale_x.data
        kwargs['flag_logscale_y'] = plotly_form.flag_logscale_y.data

        new_options = PlotlyPlotOptions(**kwargs)
        ''' append new record '''
        db.session.add(new_options)
        db.session.commit()

        ''' get lastly_added record '''
        recently_added = get_recently_added_record(db, 'PlotlyPlotOptions')
        new_options_id = recently_added.id

        ''' get old options to be replaced and after replacing, delete the old'''
        current_chart = Model.query.get(chart_id)

        current_chart.id_plotly_options = new_options_id

        db.session.commit()
        flash(f'Changed options for Plotly!', 'success')
        return redirect(url_for('route_show_data', model_name=model_name, chart_id=chart_id))

    

#TODO: Pygal options form + route


# D
@app.route("/data/delete/<string:model_name>/<int:chart_id>", methods=['POST'])
@clean_query(db=db)
def route_delete_chart(model_name, chart_id):
    """ Deletes chosen point from the database and redirects again on `route_show_data` route. """
    chart = str_to_object(model_name).query.get_or_404(chart_id)
    db.session.delete(chart)
    db.session.commit()
    flash(f'Point ({chart.id}) has been succesfully removed from the database.', 'success')
    return redirect(url_for('route_show_data', model_name=model_name))


@app.route("/data/delete/all/<string:model_name>", methods=['POST'])
@clean_query(db=db)
def route_delete_all_charts(model_name):
    Model = str_to_object(model_name)
    all_charts = Model.query.all()
    db.session.delete(all_charts)
    db.session.commit()
    flash(f'All charts have been deleted from {model_name}.', 'success')
    return redirect(url_for('route_show_data', model_name=model_name))


@app.route("/summary")
def route_summary():
    return render_template('summary.html')


''' Download images and codes section '''
@app.route("/data/download/<string:library_name>/<string:model_name>/<int:chart_id>/<string:save_img>/<string:save_src>", methods=['GET', 'POST'])
def route_download_src_img(library_name, model_name, chart_id, save_img, save_src):
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
    return redirect(url_for('route_show_data', model_name=model_name, chart_id=chart_id))


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

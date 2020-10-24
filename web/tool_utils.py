import os
import sys
import time
import inspect
from math import cos
from math import exp 
from math import log
from math import sin
from math import sqrt

import pandas as pd
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import functools

from flask import url_for

from web.import_models import *


# MATPLOTLIB
from matplotlib.figure import Figure

#SEABORN
import seaborn as sb

# BOKEH
from bokeh.plotting import figure as bokeh_figure

# PLOTLY
import plotly
import plotly.graph_objs as plotly_go


# PYGAL
import pygal
from pygal import Config as PygalConfig
from pygal.style import Style as PygalStyle

def str_to_object(string_name):
    ''' Returns the string_name as object (function, class, etc.).'''
    return getattr(sys.modules[__name__], string_name)



def make_points(model_name, chart_id):
    points = []
    Model = str_to_object(model_name)
    chart = Model.query.get(chart_id)
    if chart is None:
        print(f"no chart with given id ({chart_id}).")
    else:
        begin = chart.x_begin
        end = chart.x_end
        step = chart.step


        defaults = ['Sinus', 'Cosinus', 'Exponential']
        ''' get all model charts'''
        if model_name in defaults or model_name == 'SquareRoot':
            a = chart.a 
            b = chart.b 
            c = chart.c 
            d = chart.d
        elif model_name == 'SquareFunc':
            a = chart.a
            p = chart.p
            q = chart.q

        x_range = int((1.0)/step * (end - begin))+1

        if model_name == 'Sinus':
            for x in range(x_range):
                xx = float(round(begin+x*step, 3))
                yy = float(round(a*sin(b*xx - c) + d, 3))
                points.append((xx, yy))

        elif model_name == 'Cosinus':
            for x in range(x_range):
                xx = float(round(begin+x*step, 3))
                yy = float(round(a*cos(b*xx - c) + d, 3))
                points.append((xx, yy))

        elif model_name == 'SquareRoot':
            for x in range(x_range):
                xx = float(round(begin+x*step, 3))
                yy = float(round(a*sqrt(b*xx - c) + d, 3))
                points.append((xx, yy))

        elif model_name == 'Exponential':
            for x in range(x_range):
                xx = float(round(begin+x*step, 3))
                yy = float(round(a*exp(b*xx - c) + d, 3))
                points.append((xx, yy))

        elif model_name == 'SquareFunc':
            for x in range(x_range):
                xx = float(round(begin+x*step, 3))
                yy = float(round(a*(xx - p)**2 + q, 3))
                points.append((xx, yy))

    return points



def make_chart_matplotlib(model_name, chart_id, options):
    ''' Fetches the data from database and makes chart figure that will be shown on the webpage '''
    ''' Get data for plotting '''
    if chart_id != -1:
        points = make_points(model_name, chart_id)
    else:
        points = []
    xx = [point[0] for point in points]
    yy = [point[1] for point in points]

    ''' Get the figure object that will be returned '''
    fig = Figure(figsize=(5.0, 5.0))
    chart = fig.add_subplot(1, 1, 1)


    ''' Options for plotting '''
    kwargs = dict()

    kwargs['color']     = options.get('color', 'r')               # set color -> b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
    kwargs['linewidth'] = options.get('line_width', 2)            # set witdh of the line 
    kwargs['linestyle'] = options.get('line_style', 'solid')     # linestyle/ls:      {'-', '--', '-.', ':', ''}
    kwargs['marker']    = options.get('marker', '.')              # markers -> {'', '.', ',', '1', '2', 's', 'x', '+'}

    scatter_plot        = options.get('flag_scatter_plot', False) # dots or solid line
    show_grid           = options.get('flag_show_grid', False)    # show grid or not
    logscale_x          = options.get('flag_logscale_x', False )  # logarithmic scale
    logscale_y          = options.get('flag_logscale_y', False )  # logarithmic scale
    background_color    = options.get('bg_color', '#dbdbdb') # 
    
    chart.set_facecolor(background_color)   # background color
    
    if logscale_x:
        chart.semilogx()  

    if logscale_y:
        chart.semilogy()  

    chart.grid(show_grid, color='#5e5e5e') 
    


    chart.set_xlabel('x')
    chart.set_ylabel('y')
    chart.set_title('Matplotlib')
    
    ''' Plot on the figure and return this object to embed in web page '''
    if scatter_plot:
        kwargs['s'] = 20*kwargs['linewidth'] # marker size
        chart.scatter(xx, yy, **kwargs)
    else:
        kwargs['marker'] = None 
        chart.plot(xx, yy, **kwargs)

    
    return fig


def make_chart_seaborn(model_name, chart_id, options):
    fig = Figure(figsize=(5.0, 5.0))
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title('Seaborn')

    axis.grid(True)
    sb.set(style="darkgrid")

    points = make_points(model_name, chart_id)

    data = [
        {model_name: point[0], model_name: point[1]} for point in points
    ]
    
    df = pd.DataFrame(data=data)
    sb.lineplot(data=df, ax=axis)
    return fig


def make_chart_bokeh(model_name, chart_id, options):
    Model = str_to_object(model_name)
    points = make_points(model_name, chart_id)
    
    fig_kwargs = dict()
    fig_kwargs['title'] = model_name
    fig_kwargs['width'] = 500
    fig_kwargs['height'] = 500
    fig_kwargs['x_axis_label'] = 'x'
    fig_kwargs['y_axis_label'] = 'y'
    fig_kwargs['toolbar_location'] = None
    fig_kwargs['min_border_left'] = 0
    fig_kwargs['min_border_right'] = 45
    fig_kwargs['min_border_top'] = 0
    fig_kwargs['min_border_bottom'] = 0


    scatter_plot = options.get('flag_scatter_plot', False)
    show_grid = options.get('flag_show_grid', True)
    logscale_x = options.get('flag_logscale_x', False)
    logscale_y = options.get('flag_logscale_y', False)

    fig_kwargs['background_fill_color'] = options.get('bg_color', 'white')  # <------------------ ?
    if logscale_x:
        fig_kwargs['x_axis_type'] = "log"   # linear, datetime ,mercator <------------------
    else:
        fig_kwargs['x_axis_type'] = "linear"   

    if logscale_y:
        fig_kwargs['y_axis_type'] = "log"   # linear, datetime ,mercator <------------------
    else:
        fig_kwargs['y_axis_type'] = "linear"  


    bokeh_chart = bokeh_figure(**fig_kwargs)


    
    xx = [point[0] for point in points]
    yy = [point[1] for point in points]

    chart_kwargs = dict()
    # chart_kwargs['x'] = xx  
    # chart_kwargs['y'] = yy 
    chart_kwargs['color'] = options.get('color', 'black') # many colors... <------------------ 
    chart_kwargs['line_width'] = options.get('line_width', 2)
    chart_kwargs['line_dash'] = options.get('line_style', 'solid') # solid' 'dashed' 'dotted' 'dotdash' 'dashdot' <------------------ 

    
    bokeh_chart.xgrid.visible = show_grid
    bokeh_chart.ygrid.visible = show_grid


    if scatter_plot:
        bokeh_chart.scatter(xx, yy, **chart_kwargs)
    else:
        bokeh_chart.line(xx, yy, **chart_kwargs)

    
    xx = [point[0] for point in points]
    yy = [point[1] for point in points]

    chart_kwargs = dict()
    chart_kwargs['x'] = xx  
    chart_kwargs['y'] = yy 
    chart_kwargs['color'] = options.get('color', 'black') # many colors... <------------------ 
    chart_kwargs['line_width'] = options.get('line_width', 2)
    chart_kwargs['line_dash'] = options.get('line_style', 'solid') # solid' 'dashed' 'dotted' 'dotdash' 'dashdot' <------------------ 

    bokeh_chart.xgrid.visible = not show_grid
    bokeh_chart.ygrid.visible = not show_grid


    if scatter_plot:
        bokeh_chart.scatter(**chart_kwargs)
    else:
        bokeh_chart.line(**chart_kwargs)


        
    
    
    return bokeh_chart


def make_chart_plotly(model_name, chart_id, options):
    Model = str_to_object(model_name)
    points = make_points(model_name, chart_id)
    
    xx = [point[0] for point in points]
    yy = [point[1] for point in points]
    
               

    data = [
        plotly_go.Scatter(
            x=xx, 
            y=yy,
            line={
                'color': options.get('color', 'red'),
                'width': options.get('line_width', 2),
                'dash':  options.get('line_style', 'solid')
            },
            marker={
                'symbol': options.get('marker', 'circle'),
                'size': 3*options.get('line_width', 2) 
            },
            fillcolor='black'
        )
    ]

    layout = plotly_go.Layout(
        title=model_name, 
        title_x=0.5, 
        xaxis_title="x", 
        yaxis_title="y", 
        width=500, 
        height=500, 
        margin={'l': 30, 'r': 30, 't': 40, 'b': 5},
        plot_bgcolor=options.get('bg_color', '#dbdbdb'),
        xaxis={
            'showgrid': options.get('flag_show_grid', True),
            'type': 'log' if options.get('flag_logscale_x', True) else 'linear'
        },
        yaxis={
            'showgrid': options.get('flag_show_grid', True),
            'type': 'log' if options.get('flag_logscale_y', True) else 'linear'
        },
        modebar={
            'bgcolor': 'red'
        }
    )

    chart_properties = {
        'data': data,
        'layout': layout
    }
    
    chart_div_html = plotly.offline.plot(chart_properties, include_plotlyjs=False, output_type='div', config={'displayModeBar': False})
    return chart_div_html
    

def make_chart_pygal(model_name, chart_id, options):
    Model = str_to_object(model_name)
    points = make_points(model_name, chart_id)

    xx = [point[0] for point in points]
    yy = [point[1] for point in points]

    ''' options '''
    scatter_plot = options.get('flag_scatter_plot', False)  
    show_grid = options.get('flag_show_grid', True) 
    # logscale_x = options.get('flag_logscale_x', False) 
    logscale_y = options.get('flag_logscale_y', False) 


    pygal_config = PygalConfig()
    pygal_config.show_dots = False

    custom_style = PygalStyle(
        colors=(options.get('color', 'black'),),
        plot_background=options.get('bg_color', 'white')
    )
    pygal_config.style = custom_style

    stroke_options = dict()

    if scatter_plot:
        pygal_config.stroke = True
        stroke_options['dasharray'] = '10, 20'


    if logscale_y:
        pygal_config.logarithmic = True

    stroke_options['width'] = options.get('line_width', 2)
    pygal_config.stroke_style = stroke_options
    pygal_config.title = "Pygal"
    # pygal_config.fill = False    # <----------------------- ?

    pygal_config.show_x_guides = show_grid
    pygal_config.show_y_guides = show_grid

    chart = pygal.XY(pygal_config, width=600, height=600)
    chart.add('y', points)

    return chart


def files_count(lib_name='', path_to_images='.'):
    return len(list(filter(lambda s: s.startswith(lib_name), [f for f in os.listdir(path_to_images) if os.path.isfile(os.path.join(path_to_images, f))])))


def get_data_from_file(filename):
    x_list = []
    y_list = []
    sep = ' '
    with open(f'web/input_data/{filename}', 'r') as f:
        supported = [' ', ',', ':', '\t', '-']
        sep = ' '
        check_line = f.readline()
        for delimiter in supported:
            if len(check_line.split(delimiter))>1:
                sep = delimiter
                break
        f.seek(0)
        for line in f:
            x_list.append(float(line.strip().split(sep)[0]))
            y_list.append(float(line.strip().split(sep)[-1]))

    return x_list, y_list


def get_current_time():
    return datetime.now().strftime("%m-%d_%H-%M-%S")


def save_source_code(library_name, model_name, chart_id, current_time):
    code = inspect.getsource(str_to_object(f'make_chart_{library_name}'))
    

    filename = f'{current_time}_{library_name}_{chart_id}_{model_name}'  
    with open(f'web/downloads/codes/{filename}.py', 'w') as f:
        f.write(code) 


def download_image(library_name, model_name, chart_id, current_time):
    filename = f'{library_name}_{model_name}.png'
    image_url = 'http://localhost:5000/' + url_for('route_show_data', model_name=model_name, chart_id=chart_id)
    save_path = f'web/downloads/images/{current_time}_{filename}'
    window_size = (1920, 1080)
    
    chrome_options = Options()
    chrome_options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
    chrome_options.add_argument("--kiosk") # for full screen -> images are caught entirely, not in half
    chrome_options.add_argument("--headless") # in background
    driver = webdriver.Chrome(executable_path='web/chromedriver', options=chrome_options)
    
    driver.get(image_url)
    button_to_show_chart = driver.find_element_by_id(f'btn-show-chart-{library_name}')
    driver.execute_script("$(arguments[0]).click();", button_to_show_chart)

    wait = WebDriverWait
    wait(driver, 10).until(EC.presence_of_element_located((By.ID, f'card-{library_name}-ss')))
    image_element = driver.find_element_by_id(f'card-{library_name}-ss')
    time.sleep(2.2)
    image_element.screenshot(save_path)
    driver.quit()


def get_recently_added_record(db, model_name):
    TableModel = str_to_object(model_name)
    recently_added = db.session.query(TableModel).order_by(TableModel.id.desc()).first()
    return recently_added


def get_default_matplotlib_options(db):
    mplib_options = MatplotlibPlotOptions.query.first()

    if not mplib_options:
        kwargs = dict()
        kwargs['color'] = 'r'
        kwargs['bg_color'] = '#dbdbdb'
        kwargs['line_width'] = 2
        kwargs['line_style'] = '-'
        kwargs['marker'] = '.'
        kwargs['flag_scatter_plot'] = False
        kwargs['flag_show_grid'] = True
        kwargs['flag_logscale_x'] = False
        kwargs['flag_logscale_y'] = False
        mplib_options = MatplotlibPlotOptions(**kwargs)
        db.session.add(mplib_options)
        db.session.commit()
    
    return mplib_options


def get_default_seaborn_options(db):
    seaborn_options = SeabornPlotOptions.query.first()

    if not seaborn_options:
        kwargs = dict()
        kwargs['color'] = 'r'
        kwargs['line_width'] = 2
        kwargs['line_style'] = '-'
        kwargs['marker'] = '.'
        kwargs['flag_scatter_plot'] = False
        kwargs['flag_show_grid'] = True
        kwargs['flag_logscale_y'] = False
        seaborn_options = SeabornPlotOptions(**kwargs)
        db.session.add(seaborn_options)
        db.session.commit()
    
    return seaborn_options


def get_default_bokeh_options(db):
    bokeh_options = BokehPlotOptions.query.first()

    if not bokeh_options:
        kwargs = dict()
        kwargs['color'] = 'black'
        kwargs['bg_color'] = '#d6d6d6'
        kwargs['line_width'] = 2
        kwargs['line_style'] = 'dashed'
        kwargs['marker'] = 'asterisk'
        kwargs['flag_scatter_plot'] = False
        kwargs['flag_show_grid'] = True
        kwargs['flag_logscale_x'] = False
        kwargs['flag_logscale_y'] = False
        bokeh_options = BokehPlotOptions(**kwargs)
        db.session.add(bokeh_options)
        db.session.commit()
    
    return bokeh_options


def get_default_plotly_options(db):
    plotly_options = PlotlyPlotOptions.query.first()

    if not plotly_options:
        kwargs = dict()
        kwargs['color'] = 'red'
        kwargs['bg_color'] = '#d6d6d6'
        kwargs['line_width'] = 2
        kwargs['line_style'] = 'solid'
        kwargs['marker'] = 'circle'
        kwargs['flag_scatter_plot'] = False
        kwargs['flag_show_grid'] = True
        kwargs['flag_logscale_x'] = False
        kwargs['flag_logscale_y'] = False
        plotly_options = PlotlyPlotOptions(**kwargs)
        db.session.add(plotly_options)
        db.session.commit()
    
    return plotly_options


def get_default_pygal_options(db):
    pygal_options = PygalPlotOptions.query.first()

    if not pygal_options:
        kwargs = dict()
        kwargs['color'] = 'red'
        kwargs['bg_color'] = 'white'
        kwargs['line_width'] = 2
        kwargs['line_style'] = 'dashed'
        kwargs['marker'] = 'circle'
        kwargs['flag_scatter_plot'] = False
        kwargs['flag_show_grid'] = True
        kwargs['flag_logscale_x'] = False
        kwargs['flag_logscale_y'] = False
        pygal_options = PlotlyPlotOptions(**kwargs)
        db.session.add(pygal_options)
        db.session.commit()
    
    return pygal_options



def clean_query(db):
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            wrapper_result = func(*args, **kwargs)
            clean_unused_options(db)
            return wrapper_result
        return _wrapper
    return _decorator


def clean_unused_options(db):
    ''' 
    After each database modification (delete, update) checks for unused 
    library plot options (records) and removes them from the database.
    LPO stands for LibraryPlotOption (class name)
    '''
    LIBS = ('matplotlib', 'seaborn', 'bokeh', 'plotly', 'pygal')

    for lib in LIBS:
        
        LPO = str_to_object(f'{lib.capitalize()}PlotOptions')
        id_library_options = f'id_{lib}_options'

        sin_unused_lib_ids = (id_ for id_, in Sinus.query.with_entities(getattr(Sinus, id_library_options)))
        cos_unused_lib_ids = (id_ for id_, in Cosinus.query.with_entities(getattr(Cosinus, id_library_options)))
        sqrt_unused_lib_ids = (id_ for id_, in SquareRoot.query.with_entities(getattr(SquareRoot, id_library_options)))
        exp_unused_lib_ids = (id_ for id_, in Exponential.query.with_entities(getattr(Exponential, id_library_options)))
        sqf_unused_lib_ids = (id_ for id_, in SquareFunc.query.with_entities(getattr(SquareFunc, id_library_options)))
        
        unused_ids = (
            *sin_unused_lib_ids, 
            *cos_unused_lib_ids, 
            *sqrt_unused_lib_ids, 
            *exp_unused_lib_ids, 
            *sqf_unused_lib_ids
        )
        options_to_delete = LPO.query.filter(
            LPO.id.in_(
                LPO.query.filter(
                    ~LPO.id.in_(unused_ids)
                ).with_entities(LPO.id)
            )
        ).all()
        
        for option in options_to_delete:
            db.session.delete(option)
    
    db.session.commit()


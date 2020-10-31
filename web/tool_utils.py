import os
import sys
import json
import time
import inspect

from math import cos
from math import exp 
from math import log
from math import sin
from math import sqrt
import textwrap
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
from web.import_forms import *

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


def formatted_code(code_str):
    ''' Code formatter, removes trailing whitespaces making python script executable assuming code is valid. '''
    if code_str and code_str[0] == '\n':
        code_str = code_str[1:]
    return textwrap.dedent(code_str)


def make_points(model_name, chart_id):
    ''' Returns the list of points - tuples (x, y) from the database. '''
    points = []
    if chart_id != -1:
        Model = str_to_object(model_name)
        chart = Model.query.get(chart_id)
        if chart is None:
            print(f"no chart with given id ({chart_id}).")
        else:
            begin = chart.x_begin
            end = chart.x_end
            step = chart.step

            defaults = ['Sinus', 'Cosinus', 'Exponential']
            
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

    elif chart_id == -1 and model_name == "FileDataPoint":
        data_points = FileDataPoint.query.all()
        for point in data_points:
            points.append((point.x, point.y))
    return points


def color_hash_to_string(color_hash):
    SUPPORTED_COLORS = {
        "#292928": "black",
        "#474747": "black",
        "#000000": "black",

        "#f5f5f5": "white",
        "#ffffff": "white",
        "#e6e3e1": "white",

        "#5b9bde": "blue", 
        "#4f84bd": "blue", 
        "#3e77cc": "blue", 
        
        "#a1e024": "green", 
        "#92c720": "green", 
        "#81b81a": "green", 

        "#ff6554": "red", 
        "#e00f00": "red", 
        "#c20d00": "red", 

        "#04ebeb": "cyan",
        "#05dbdb": "cyan",
        "#07baba": "cyan",

        "#ff75f8": "magenta", 
        "#d601d2": "magenta", 
        "#ad01aa": "magenta", 

        "#ffff7a": "yellow",
        "#f8ff6e": "yellow",
        "#f7ff07": "yellow"
    }
    try:
        return SUPPORTED_COLORS[color_hash]
    except:
        raise ValueError(f'[color_hash_to_string] {color_hash} is unsupported hash code.')

def get_contrasted_colors(color_hash):
    ''' Returns contrasted colors from JSON file (light, dark) of that color. '''
    
    with open ('colors.json', 'r') as f:
        colors = json.load(f)
    
    LIGHT_TONE = 0
    DARK_TONE  = 2

    light_color = colors.get(color_hash_to_string(color_hash))[LIGHT_TONE]
    dark_color  = colors.get(color_hash_to_string(color_hash))[DARK_TONE]
    
    return (light_color, dark_color)
    


def make_chart_matplotlib(model_name, chart_id, options, data_filename=''):
    ''' Fetches the data from database and makes chart figure that will be shown on the web page. '''
    points = []
    if model_name == "FileData" and data_filename and chart_id == -1:
        xx, yy = get_data_from_file(data_filename)
    else:
        points = make_points(model_name, chart_id)
        xx = [point[0] for point in points]
        yy = [point[1] for point in points]

    ''' Get the figure object that will be returned '''
    fig = Figure(figsize=(5.0, 5.0))
    chart = fig.add_subplot(1, 1, 1)

    
    if options.get('color') == options.get('bg_color'):
        color_to_contrast = options.get('color', '#292928')
        options['bg_color'], options['color'] = get_contrasted_colors(color_to_contrast)

    kwargs = dict()
    
    kwargs['color']     = options.get('color', 'r')              
    kwargs['linewidth'] = options.get('line_width', 2)           
    kwargs['linestyle'] = options.get('line_style', 'solid')    
    kwargs['marker']    = options.get('marker', '.')              

    scatter_plot        = options.get('flag_scatter_plot', False)
    show_grid           = options.get('flag_show_grid', False)    
    logscale_x          = options.get('flag_logscale_x', False )
    logscale_y          = options.get('flag_logscale_y', False )
    background_color    = options.get('bg_color', '#dbdbdb')
    
    chart.set_facecolor(background_color)
    
    if logscale_x:
        chart.semilogx()  

    if logscale_y:
        chart.semilogy()  

    if show_grid:
        chart.grid(color='#5e5e5e') 
    else:
        chart.grid(False)

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


def make_chart_seaborn(model_name, chart_id, options, data_filename=''):
    points = []
    if model_name == "FileData" and data_filename and chart_id == -1:
        xx, yy = get_data_from_file(data_filename)
        points = [(x, y) for x, y in zip(xx, yy)]
    else:
        points = make_points(model_name, chart_id)
    data = [
        {model_name: point[0], model_name: point[1]} for point in points
    ]
    df = pd.DataFrame(data=data)
    
    if options.get('color') == options.get('bg_color'):
        color_to_contrast = options.get('color', '#292928')
        options['bg_color'], options['color'] = get_contrasted_colors(color_to_contrast)

    fig = Figure(figsize=(5.0, 5.0), facecolor='#ebebeb')
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title('Seaborn')
    axis.set_facecolor(options.get('bg_color', 'white'))
    fig.set_edgecolor('red')

    seaborn_style = dict()
    flag_scatter_plot = options.get('flag_scatter_plot', False)
    flag_show_grid = options.get('flag_show_grid', True)
    flag_logscale_x = options.get('flag_logscale_x', False)
    flag_logscale_y = options.get('flag_logscale_y', False)

    if flag_logscale_x:
        axis.set_xscale('log')

    if flag_logscale_y:
        axis.set_yscale('log')


    if flag_show_grid:
        axis.grid(True)
        seaborn_style['style'] = 'darkgrid'
    else:
        axis.grid(False)

    sb.set_theme(**seaborn_style)
    
    plot_kwargs = dict()
    plot_kwargs['legend'] = False
    plot_kwargs['palette'] = [options.get('color', 'black'),]
    plot_kwargs['linewidth'] = options.get('line_width', 3)

    if options.get('line_style', 'solid') == 'dashed':
        plot_kwargs['dashes'] = [(4,6)]

    if flag_scatter_plot:
        sb.scatterplot(data=df, ax=axis, **plot_kwargs)
    else:
        sb.lineplot(data=df, ax=axis, **plot_kwargs)
    return fig


def make_chart_bokeh(model_name, chart_id, options):
    points = make_points(model_name, chart_id)
    xx = [point[0] for point in points]
    yy = [point[1] for point in points]

    if options.get('color') == options.get('bg_color'):
        color_to_contrast = options.get('color', '#292928')
        options['bg_color'], options['color'] = get_contrasted_colors(color_to_contrast)

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
    fig_kwargs['background_fill_color'] = options.get('bg_color', '#cccccc')
    flag_scatter_plot = options.get('flag_scatter_plot', False)
    flag_show_grid = options.get('flag_show_grid', True)
    flag_logscale_x = options.get('flag_logscale_x', False)
    flag_logscale_y = options.get('flag_logscale_y', False)

   
    if flag_logscale_x:
        fig_kwargs['x_axis_type'] = "log"   # linear, datetime ,mercator <------------------
    else:
        fig_kwargs['x_axis_type'] = "linear"   

    if flag_logscale_y:
        fig_kwargs['y_axis_type'] = "log" 
    else:
        fig_kwargs['y_axis_type'] = "linear"  

    bokeh_chart = bokeh_figure(**fig_kwargs)
    bokeh_chart.xgrid.visible = flag_show_grid
    bokeh_chart.ygrid.visible = flag_show_grid
    
    plot_kwargs = dict()
    plot_kwargs['color'] = options.get('color', 'black') # many colors... <------------------ 
    plot_kwargs['line_width'] = options.get('line_width', 2)
    plot_kwargs['line_dash'] = options.get('line_style', 'solid') # solid' 'dashed' 'dotted' 'dotdash' 'dashdot' <------------------ 

    if flag_scatter_plot:
        bokeh_chart.scatter(xx, yy, **plot_kwargs)
    else:
        bokeh_chart.line(xx, yy, **plot_kwargs)
    
    return bokeh_chart


def make_chart_plotly(model_name, chart_id, options):
    points = make_points(model_name, chart_id)
    xx = [point[0] for point in points]
    yy = [point[1] for point in points]
        
    if options.get('color') == options.get('bg_color'):
        color_to_contrast = options.get('color', '#292928')
        options['bg_color'], options['color'] = get_contrasted_colors(color_to_contrast)         

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
            'type': 'log' if options.get('flag_logscale_x', False) else 'linear'
        },
        yaxis={
            'showgrid': options.get('flag_show_grid', True),
            'type': 'log' if options.get('flag_logscale_y', False) else 'linear'
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
   
    points = make_points(model_name, chart_id)

    ''' options '''
    if options.get('color') == options.get('bg_color'):
        color_to_contrast = options.get('color', '#292928')
        options['bg_color'], options['color'] = get_contrasted_colors(color_to_contrast)

    scatter_plot = options.get('flag_scatter_plot', False)  
    show_grid = options.get('flag_show_grid', True) 
    logscale_y = options.get('flag_logscale_y', False) 


    pygal_config = PygalConfig()
    pygal_config.show_dots = False
    pygal_config.style = PygalStyle(
        colors=(options.get('color', 'black'),),
        plot_background=options.get('bg_color', '#cccccc')
    )

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
    ''' Gets data from file as a tuple of (x: list, y: list )    '''
    x_list = []
    y_list = []
    sep = ' '
    with open(f'web/input_data/{filename}', 'r') as f:
        sep = ','
        for line in f:
            x_list.append(float(line.strip().split(sep)[0]))
            y_list.append(float(line.strip().split(sep)[-1]))

    return x_list, y_list


def get_current_time():
    ''' Returns current date in nice format. '''
    return datetime.now().strftime("%m-%d_%H-%M-%S")


def save_source_code(library_name, model_name, chart_id, current_time):
    options = get_lib_options_from_model_and_chart_id(library_name, model_name, chart_id)
    if options.get('color') == options.get('bg_color'):
        color_to_contrast = options['color']
        options['bg_color'], options['color'] = get_contrasted_colors(color_to_contrast)

    points = make_points(model_name, chart_id)
    xx = [point[0] for point in points]
    yy = [point[1] for point in points]
    
    x_str = f'xx = {xx}'
    y_str = f'yy = {yy}'
    
    if library_name == 'matplotlib':
        code = f''' 
        """ AUTO-GENERATED FILE """
        import matplotlib.pyplot as plt

        plt.rcParams['toolbar'] = 'None'
        options = {options}
        {x_str}
        {y_str}
        kwargs = dict()

        kwargs['color']     = options.get('color', 'r')
        kwargs['linewidth'] = options.get('line_width', 2)
        kwargs['linestyle'] = options.get('line_style', 'solid')
        kwargs['marker']    = options.get('marker', '.')

        scatter_plot        = options.get('flag_scatter_plot', False)
        show_grid           = options.get('flag_show_grid', False)
        logscale_x          = options.get('flag_logscale_x', False )
        logscale_y          = options.get('flag_logscale_y', False )
        background_color    = options.get('bg_color', '#dbdbdb')

        fig = plt.figure()
        fig.set_size_inches(6.2, 5.0)
        chart = fig.add_subplot(1, 1, 1)

        if logscale_x:
            chart.semilogx()

        if logscale_y:
            chart.semilogy()

        chart.grid(show_grid)
        chart.set_facecolor(background_color)

        if logscale_x:
            chart.semilogx()  

        if logscale_y:
            chart.semilogy()  

        chart.grid(show_grid, color='#5e5e5e') 

        if scatter_plot:
            kwargs['s'] = 20*kwargs['linewidth']
            chart.scatter(xx, yy, **kwargs)
        else:
            kwargs['marker'] = None 
            chart.plot(xx, yy, **kwargs)

        chart.set_xlabel('x')
        chart.set_ylabel('y')
        chart.set_title('Matplotlib')

        plt.show()
        '''
    elif library_name == 'seaborn':
        code = '''
        """ AUTO-GENERATED FILE """
        import pandas as pd
        import seaborn as sb
        import matplotlib.pyplot as plt

        plt.rcParams['toolbar'] = 'None'

        data = [
            {\' ''' + model_name + ''' \': x, \' ''' + model_name + ''' \': y} for x, y in ''' + f'zip({xx}, {yy})]' + f'''
        df = pd.DataFrame(data=data)

        options = {options}
        fig = plt.figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.set_title('Seaborn')
        ax = plt.axes()
        ax.set_facecolor(options.get('bg_color', 'white'))


        seaborn_style = dict()

        flag_scatter_plot = options.get('flag_scatter_plot', False)
        flag_show_grid = options.get('flag_show_grid', True)
        flag_logscale_x = options.get('flag_logscale_x', False)
        flag_logscale_y = options.get('flag_logscale_y', False)


        if flag_logscale_x:
            axis.set_xscale('log')

        if flag_logscale_y:
            axis.set_yscale('log')


        if flag_show_grid:
            axis.grid(True)
            seaborn_style['style'] = 'darkgrid'
        else:
            axis.grid(False)



        sb.set_theme(**seaborn_style)

        plot_kwargs = dict()
        plot_kwargs['legend'] = False
        plot_kwargs['palette'] = [options.get('color', 'black')]
        plot_kwargs['linewidth'] = options.get('line_width', 3)

        if options.get('line_style', 'solid') == 'dashed':
            plot_kwargs['dashes'] = [(4,6)]

        if flag_scatter_plot:
            sb.scatterplot(data=df, ax=axis, **plot_kwargs)
        else:
            sb.lineplot(data=df, ax=axis, **plot_kwargs)

        plt.show()
        '''
    elif library_name == 'bokeh':
        code = f'''
        """ AUTO-GENERATED FILE """

        from bokeh.plotting import figure as bokeh_figure, show
        from bokeh.io.export import get_screenshot_as_png
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from PIL import Image

        {x_str}
        {y_str}

        options = {options}

        flag_scatter_plot = options.get('flag_scatter_plot', False)
        flag_show_grid = options.get('flag_show_grid', True)
        flag_logscale_x = options.get('flag_logscale_x', False)
        flag_logscale_y = options.get('flag_logscale_y', False)

        fig_kwargs = dict()
        fig_kwargs['title'] = 'Bokeh plot'
        fig_kwargs['x_axis_label'] = 'x'
        fig_kwargs['y_axis_label'] = 'y'
        fig_kwargs['toolbar_location'] = None
        fig_kwargs['min_border_right'] = 45

        if flag_logscale_x:
            fig_kwargs['x_axis_type'] = "log"
        else:
            fig_kwargs['x_axis_type'] = "linear"   

        if flag_logscale_y:
            fig_kwargs['y_axis_type'] = "log"
        else:
            fig_kwargs['y_axis_type'] = "linear"   

        bokeh_chart = bokeh_figure(**fig_kwargs) 

        chart_kwargs = dict()
        chart_kwargs['x'] = xx  
        chart_kwargs['y'] = yy  
        chart_kwargs['color'] = options.get('color', 'black') 
        chart_kwargs['line_width'] = options.get('line_width', 2)
        chart_kwargs['line_dash'] = options.get('line_style', 'solid')

        if not flag_show_grid:
            bokeh_chart.xgrid.visible = False
            bokeh_chart.ygrid.visible = False

        if flag_scatter_plot:
            chart_kwargs['marker'] = options.get('marker', 'asterisk')
            bokeh_chart.scatter(**chart_kwargs)
        else:
            bokeh_chart.line(**chart_kwargs)

        chrome_options = Options()
        chrome_options.add_argument(f"--window-size={500},{500}")
        chrome_options.add_argument("--kiosk")
        chrome_options.add_argument("--headless")
        webdriver = webdriver.Chrome(executable_path='web/chromedriver', options=chrome_options)

        image = get_screenshot_as_png(bokeh_chart, height=500, width=500, driver=webdriver)

        image.show()'''
    elif library_name == 'plotly':
        code = f'''
        import plotly
        import plotly.graph_objs as plotly_go
        import numpy as np

        {x_str}
        {y_str}

        options = {options}
                    
        data = [
            plotly_go.Scatter(
                x=xx, 
                y=yy,
                line=''' + '{' + '''
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
            title='Plotly', 
            title_x=0.5, 
            xaxis_title="x", 
            yaxis_title="y", 
            width=500, 
            height=500, 
            margin={'l': 30, 'r': 30, 't': 40, 'b': 5},
            plot_bgcolor=options.get('bg_color', '#dbdbdb'),
            xaxis={
                'showgrid': options.get('flag_show_grid', True),
                'type': 'log' if options.get('flag_logscale_x', False) else 'linear'
            },
            yaxis={
                'showgrid': options.get('flag_show_grid', True),
                'type': 'log' if options.get('flag_logscale_y', False) else 'linear'
            },
            modebar={
                'bgcolor': 'red'
            }
        )

        chart_properties = {
            'data': data,
            'layout': layout
        }

        fig = plotly_go.Figure(
            data=data,
            layout=layout
        )
        fig.show()'''
    elif library_name == 'pygal':
        code = f''' 
        """ AUTO-GENERATED FILE """
        import pygal
        from pygal import Config as PygalConfig
        from pygal.style import Style as PygalStyle
        from PIL import Image
        import os

        options = {options}
        xx = {x_str}
        yy = {y_str}
        points = [(x, y) for x, y in zip(xx, yy)]

        scatter_plot = options.get('flag_scatter_plot', False)  
        show_grid = options.get('flag_show_grid', True) 
        logscale_y = options.get('flag_logscale_y', False) 


        pygal_config = PygalConfig()
        pygal_config.show_dots = False
        pygal_config.style = PygalStyle(
            colors=(options.get('color', 'black'),),
            plot_background=options.get('bg_color', '#cccccc')
        )   

        stroke_options = dict()

        if scatter_plot:
            pygal_config.stroke = True
            stroke_options['dasharray'] = '10, 20'

        if logscale_y:
            pygal_config.logarithmic = True

        stroke_options['width'] = options.get('line_width', 2)
        pygal_config.stroke_style = stroke_options
        pygal_config.title = "Pygal"

        pygal_config.show_x_guides = show_grid
        pygal_config.show_y_guides = show_grid

        chart = pygal.XY(pygal_config)

        chart.add('y', points)
        chart.render_to_png('pygal.png')
        im = Image.open('pygal.png')
        os.remove("pygal.png")
        im.show() '''

    filename = f'{current_time}_{library_name}_{chart_id}_{model_name}'  
    with open(f'web/downloads/codes/{filename}.py', 'w') as f:
        f.write(formatted_code(code))
        
# download_image('matplotlib', 'FileDataPoint', -1)

def download_image(library_name, model_name, chart_id, current_time):
    filename = f'{library_name}_{model_name}.png'
    if model_name == "FileDataPoint" and chart_id == -1:
        image_url = 'http://localhost:5000/' + url_for('route_show_data_from_file')
    else:    
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
    ''' Helper method to return the most recently added record (helpful when redirecting after database modification).'''
    TableModel = str_to_object(model_name)
    recently_added = db.session.query(TableModel).order_by(TableModel.id.desc()).first()
    return recently_added


def get_default_matplotlib_options(db, as_dict=True):
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
        return kwargs if as_dict else mplib_options
    return mplib_options


def get_default_seaborn_options(db, as_dict=True):
    seaborn_options = SeabornPlotOptions.query.first()

    if not seaborn_options:
        kwargs = dict()
        kwargs['color'] = 'red'
        kwargs['bg_color'] = 'white'
        kwargs['line_width'] = 2
        kwargs['line_style'] = 'dashed'
        kwargs['marker'] = ''
        kwargs['flag_scatter_plot'] = False
        kwargs['flag_show_grid'] = True
        kwargs['flag_logscale_x'] = False
        kwargs['flag_logscale_y'] = False
        seaborn_options = SeabornPlotOptions(**kwargs)
        db.session.add(seaborn_options)
        db.session.commit()
        return kwargs if as_dict else seaborn_options

    return seaborn_options


def get_default_bokeh_options(db, as_dict=True):
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
        return kwargs if as_dict else bokeh_options
    return bokeh_options


def get_default_plotly_options(db, as_dict=True):
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
        return kwargs if as_dict else plotly_options

    return plotly_options


def get_default_pygal_options(db, as_dict=True):
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
        kwargs['flag_logscale_y'] = False
        pygal_options = PygalPlotOptions(**kwargs)
        db.session.add(pygal_options)
        db.session.commit()
        return kwargs if as_dict else pygal_options
    
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

    fpo = FilePlotOptions.query.first()
    if fpo:
        FilePlotOptions.query.filter(FilePlotOptions.id != fpo.id).delete()
        db.session.commit()
    
        used_ids = {
            'matplotlib': fpo.id_matplotlib_options,
            'seaborn':  fpo.id_seaborn_options,
            'bokeh': fpo.id_bokeh_options,
            'plotly': fpo.id_plotly_options,
            'pygal': fpo.id_pygal_options
        }

    for lib in LIBS:
        LPO = str_to_object(f'{lib.capitalize()}PlotOptions')
        id_library_options = f'id_{lib}_options'
        
        sin_unused_lib_ids  = (id_ for id_, in Sinus.query.with_entities(getattr(Sinus, id_library_options)))
        cos_unused_lib_ids  = (id_ for id_, in Cosinus.query.with_entities(getattr(Cosinus, id_library_options)))
        sqrt_unused_lib_ids = (id_ for id_, in SquareRoot.query.with_entities(getattr(SquareRoot, id_library_options)))
        exp_unused_lib_ids  = (id_ for id_, in Exponential.query.with_entities(getattr(Exponential, id_library_options)))
        sqf_unused_lib_ids  = (id_ for id_, in SquareFunc.query.with_entities(getattr(SquareFunc, id_library_options)))
        
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
            if getattr(option, id.__name__) != used_ids.get(lib, -1):
                db.session.delete(option)
    
    db.session.commit()



def get_lib_options_from_model_and_chart_id(library_name, model_name, chart_id):
    Model = str_to_object(model_name)
    LPO = str_to_object(f'{library_name.capitalize()}PlotOptions')
    id_library_options = f'id_{library_name}_options'
    options_id = getattr(Model.query.get(chart_id), id_library_options)
    options = LPO.get_options(options_id)

    return options
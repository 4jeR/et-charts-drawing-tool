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

def str_to_object(string_name):
    ''' Returns the string_name as object (function, class, etc.).'''
    return getattr(sys.modules[__name__], string_name)



def make_points(model_name, chart_id):
    Model = str_to_object(model_name)
    chart = Model.query.get(chart_id)


    begin = getattr(chart, 'x_begin', 0)
    end = getattr(chart, 'x_end', 1)
    step = getattr(chart, 'step', 0.1)

    a = getattr(chart, 'a', 'a')
    b = getattr(chart, 'b', 'b')
    c = getattr(chart, 'c', 'c')
    d = getattr(chart, 'd', 'd')
    p = getattr(chart, 'p', 'p')
    q = getattr(chart, 'q', 'q')

    # coefs = {float(coef) for coef in chart.get_coefs().values()}
    
    print("------------------------------")
    print(f"TEST RANGE for id: {chart_id}:") 
    print(f'start = {begin}')
    print(f'end   = {end}')
    print(f'step  = {step}')
    print(f'a  = {a}')
    print(f'b  = {b}')
    print(f'c  = {c}')
    print(f'd  = {d}')
    print(f'p  = {p}')
    print(f'q  = {q}')
    # print(f'start = {coefs}')
    print("------------------------------")


    
    
    x_range = int((1.0)/step * (end - begin))+1

    points = []
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
    points = make_points(model_name, chart_id)

    xx = [point[0] for point in points]
    yy = [point[1] for point in points]

    print("[MAKE_CHART_MATPLOTLIB]")
    print(f"x: {xx}")
    print(f"y: {yy}")
    ''' Options for plotting '''
    kwargs = dict()

    kwargs['color']     = options.get('color', 'r')               # set color -> b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
    kwargs['linewidth'] = options.get('line_width', 2)            # set witdh of the line 
    kwargs['linestyle'] = options.get('line_style', 'solid')     # linestyle/ls:      {'-', '--', '-.', ':', ''}
    kwargs['marker']    = options.get('marker', '.')              # markers -> {'', '.', ',', '1', '2', 's', 'x', '+'}

    scatter_plot        = options.get('flag_scatter_plot', False) # dots or solid line
    show_grid           = options.get('flag_show_grid', False)    # show grid or not
    logscale_y          = options.get('flag_logscale_y', False )  # logarithmic scale
    show_legend         = options.get('flag_show_legend', False)  # show_legend
  


    ''' Get the figure object that will be returned '''
    fig = Figure(figsize=(5.0, 5.0))
    chart = fig.add_subplot(1, 1, 1)

    if logscale_y:
        chart.semilogy()  # set logscaly for  Y

    chart.grid(show_grid) 
    if show_legend:
        chart.legend()


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


def make_chart_seaborn(model_name):
    fig = Figure(figsize=(5.0, 5.0))
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title('Seaborn')

    axis.grid(True)
    sb.set(style="darkgrid")

    points = make_points(model_name)

    # xx = [point[0] for point in points]
    # yy = [point[1] for point in points]

    data = [
        {model_name: point[0], model_name: point[1]} for point in points
    ]
    
    df = pd.DataFrame(data=data)
    sb.lineplot(data=df, ax=axis)
    return fig


def make_chart_bokeh(model_name):
    # Model = str_to_object(model_name)
    # points = Model.query.all()

    # xx = [point.x for point in points]
    # yy = [point.y for point in points]
    xx = [x for x in range(10)]
    yy = [y*y for y in range(10)]
    bokeh_chart = bokeh_figure(title="Bokeh plot", width=530, height=500, x_axis_label='x', y_axis_label='y')
    bokeh_chart.line(xx, yy)
    

    return bokeh_chart


def make_chart_plotly(model_name):
    # Model = str_to_object(model_name)
    # points = Model.query.all()
    
    # xx = [point.x for point in points]
    # yy = [point.y for point in points]
    xx = [x for x in range(10)]
    yy = [y*y for y in range(10)]  
    chart_props = {
        "data": [plotly_go.Line(x=xx, y=yy)],
        "layout": plotly_go.Layout(title="Plotly chart", title_x=0.5, xaxis_title="x", yaxis_title="y", width=530, height=500, margin={"l": 20, "t": 30})
    }
    
    chart_div_html = plotly.offline.plot(chart_props, include_plotlyjs=False, output_type='div')
    return chart_div_html
    

def make_chart_pygal(model_name):
    # Model = str_to_object(model_name)
    # points = Model.query.all()

    # xx = [x for x in range(10)]
    # yy = [y*y for y in range(10)]

    chart = pygal.XY(show_dots=False, width=520, height=500)
    chart.title = "Pygal"
    # chart.add('y', [(point.x, point.y) for point in points])

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


def save_source_code(library_name, model_name, current_time):
    code = inspect.getsource(str_to_object(f'make_chart_{library_name}'))
    

    filename = f'{current_time}_{library_name}_{model_name}'  
    with open(f'web/downloads/codes/{filename}.py', 'w') as f:
        f.write(code) 


def download_image(library_name, model_name, current_time):
    filename = f'{library_name}_{model_name}.png'
    image_url = 'http://localhost:5000/' + url_for('route_show_data', model_name=model_name)
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
    time.sleep(2)
    image_element.screenshot(save_path)
    driver.quit()



def get_recently_added_record(db, model_name):
    TableModel = str_to_object(model_name)
    recently_added = db.session.query(TableModel).order_by(TableModel.id.desc()).first()
    return recently_added
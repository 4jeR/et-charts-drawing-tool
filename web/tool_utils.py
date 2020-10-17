import os
import sys
import time
import inspect
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


def make_chart_matplotlib(model_name, options):
    ''' Fetches the data from database and makes chart figure that will be shown on the webpage '''
    
    ''' Get data for plotting '''
    Model = str_to_object(model_name)

    points = Model.query.all()
    xx = [point.x for point in points]
    yy = [point.y for point in points]

    ''' Options for plotting '''
    kwargs = dict()

    kwargs['color']     = options.get('color', 'r')               # set color -> b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
    kwargs['linewidth'] = options.get('line_width', 2)            # set witdh of the line 
    kwargs['linestyle'] = options.get('line_style', 'dashed')     # linestyle/ls:      {'-', '--', '-.', ':', ''}
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

    Model = str_to_object(model_name)
    points = Model.query.all()
    data = [
        {model_name: point.x, model_name: point.y} for point in points
    ]
    
    df = pd.DataFrame(data=data)
    sb.lineplot(data=df, ax=axis)
    return fig


def make_chart_bokeh(model_name):
    Model = str_to_object(model_name)
    points = Model.query.all()

    xx = [point.x for point in points]
    yy = [point.y for point in points]

    bokeh_chart = bokeh_figure(title="Bokeh plot", width=530, height=500, x_axis_label='x', y_axis_label='y')
    bokeh_chart.line(xx, yy)
    

    return bokeh_chart


def make_chart_plotly(model_name):
    Model = str_to_object(model_name)
    points = Model.query.all()
    
    xx = [point.x for point in points]
    yy = [point.y for point in points]  
    chart_props = {
        "data": [plotly_go.Line(x=xx, y=yy)],
        "layout": plotly_go.Layout(title="Plotly chart", title_x=0.5, xaxis_title="x", yaxis_title="y", width=530, height=500, margin={"l": 20, "t": 30})
    }
    
    chart_div_html = plotly.offline.plot(chart_props, include_plotlyjs=False, output_type='div')
    return chart_div_html
    

def make_chart_pygal(model_name):
    Model = str_to_object(model_name)
    points = Model.query.all()


    chart = pygal.XY(show_dots=False, width=520, height=500)
    chart.title = "Pygal"
    chart.add('y', [(point.x, point.y) for point in points])

    return chart


def files_count(lib_name='', path_to_images='.'):
    return len(list(filter(lambda s: s.startswith(lib_name), [f for f in os.listdir(path_to_images) if os.path.isfile(os.path.join(path_to_images, f))])))


def make_points(db, form, model_name, step):
    x_range = int((1.0)/step * (form.end.data - form.begin.data))+1
    current_points = set([point.x for point in str_to_object(model_name).query.all()])
    for i in range(x_range):
        dx = i*step
        pt = str_to_object(model_name).make_point(form.begin.data+dx)
        if pt.x not in current_points:
            db.session.add(pt)


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
    driver = webdriver.Chrome(executable_path='web/chromedriver', chrome_options=chrome_options)
    
    driver.get(image_url)
    button_to_show_chart = driver.find_element_by_id(f'btn-show-chart-{library_name}')
    driver.execute_script("$(arguments[0]).click();", button_to_show_chart)

    wait = WebDriverWait
    wait(driver, 10).until(EC.presence_of_element_located((By.ID, f'card-{library_name}-ss')))
    image_element = driver.find_element_by_id(f'card-{library_name}-ss')
    time.sleep(2)
    image_element.screenshot(save_path)
    driver.quit()


def get_html_content(library_name, model_name):
    html = """ 
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <h1>Error loading a file</h1>
    </body>
    </html>
    """
    if library_name == 'matplotlib':
        with open(f'web/templates/show_data.html', 'r') as f:
            html = f.read()
    elif library_name == 'seaborn':
        pass
    elif library_name == 'bokeh':
        pass
    elif library_name == 'plotly':
        pass
    elif library_name == 'pygal':
        pass
    return html

   


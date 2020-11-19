from web import db

""" TODO: Bar plot / pie plot etc... """


class Sinus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x_begin = db.Column(db.Float, unique=False, nullable=False)
    x_end = db.Column(db.Float, unique=False, nullable=False)
    step = db.Column(db.Float, unique=False, nullable=False)

    a = db.Column(db.Float, unique=False, nullable=False)
    b = db.Column(db.Float, unique=False, nullable=False)
    c = db.Column(db.Float, unique=False, nullable=False)
    d = db.Column(db.Float, unique=False, nullable=False)

    id_matplotlib_options = db.Column(db.Integer, unique=False, nullable=False)
    id_seaborn_options = db.Column(db.Integer, unique=False, nullable=False)
    id_bokeh_options = db.Column(db.Integer, unique=False, nullable=False)
    id_plotly_options = db.Column(db.Integer, unique=False, nullable=False)
    id_pygal_options = db.Column(db.Integer, unique=False, nullable=False)
                                                                          

    @staticmethod
    def get_domain_and_step(chart_id):
        ''' Returns the list of 3 elements: begin, end and step of the function. '''
        chart = Sinus.query.get(chart_id)
        if chart:
            return [chart.x_begin, chart.x_end, chart.step] 
        else:
            return [0, 1, 0.1]
    
    @staticmethod
    def get_coefs(chart_id):
        ''' Returns the list of all model coefficients. '''
        chart = Sinus.query.get(chart_id)
        if chart:
            return [chart.a, chart.b, chart.c, chart.d]
        else:
            return ['?', '?', '?', '?']
    

class Cosinus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x_begin = db.Column(db.Float, unique=False, nullable=False)
    x_end = db.Column(db.Float, unique=False, nullable=False)
    step = db.Column(db.Float, unique=False, nullable=False)

    a = db.Column(db.Float, unique=False, nullable=False)
    b = db.Column(db.Float, unique=False, nullable=False)
    c = db.Column(db.Float, unique=False, nullable=False)
    d = db.Column(db.Float, unique=False, nullable=False)

    id_matplotlib_options = db.Column(db.Integer, unique=False, nullable=False)
    id_seaborn_options = db.Column(db.Integer, unique=False, nullable=False)
    id_bokeh_options = db.Column(db.Integer, unique=False, nullable=False)
    id_plotly_options = db.Column(db.Integer, unique=False, nullable=False)
    id_pygal_options = db.Column(db.Integer, unique=False, nullable=False)
   
    @staticmethod
    def get_domain_and_step(chart_id):
        ''' Returns the list of 3 elements: begin, end and step of the function. '''
        chart = Cosinus.query.get(chart_id)
        if chart:
            return [chart.x_begin, chart.x_end, chart.step] 
        else:
            return [0, 1, 0.1]
    
    @staticmethod
    def get_coefs(chart_id):
        ''' Returns the list of all model coefficients. '''
        chart = Cosinus.query.get(chart_id)
        if chart:
            return [chart.a, chart.b, chart.c, chart.d]
        else:
            return ['?', '?', '?', '?']


class SquareRoot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x_begin = db.Column(db.Float, unique=False, nullable=False)
    x_end = db.Column(db.Float, unique=False, nullable=False)
    step = db.Column(db.Float, unique=False, nullable=False)

    a = db.Column(db.Float, unique=False, nullable=False)
    b = db.Column(db.Float, unique=False, nullable=False)
    c = db.Column(db.Float, unique=False, nullable=False)
    d = db.Column(db.Float, unique=False, nullable=False)

    id_matplotlib_options = db.Column(db.Integer, unique=False, nullable=False)
    id_seaborn_options = db.Column(db.Integer, unique=False, nullable=False)
    id_bokeh_options = db.Column(db.Integer, unique=False, nullable=False)
    id_plotly_options = db.Column(db.Integer, unique=False, nullable=False)
    id_pygal_options = db.Column(db.Integer, unique=False, nullable=False)

    @staticmethod
    def get_domain_and_step(chart_id):
        ''' Returns the list of 3 elements: begin, end and step of the function. '''
        chart = SquareRoot.query.get(chart_id)
        if chart:
            return [chart.x_begin, chart.x_end, chart.step] 
        else:
            return [0, 1, 0.1]
    
    @staticmethod
    def get_coefs(chart_id):
        ''' Returns the list of all model coefficients. '''
        chart = SquareRoot.query.get(chart_id)
        if chart:
            return [chart.a, chart.b, chart.c, chart.d]
        else:
            return ['?', '?', '?', '?']


class Exponential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x_begin = db.Column(db.Float, unique=False, nullable=False)
    x_end = db.Column(db.Float, unique=False, nullable=False)
    step = db.Column(db.Float, unique=False, nullable=False)

    a = db.Column(db.Float, unique=False, nullable=False)
    b = db.Column(db.Float, unique=False, nullable=False)
    c = db.Column(db.Float, unique=False, nullable=False)
    d = db.Column(db.Float, unique=False, nullable=False)

    
    id_matplotlib_options = db.Column(db.Integer, unique=False, nullable=False)
    id_seaborn_options = db.Column(db.Integer, unique=False, nullable=False)
    id_bokeh_options = db.Column(db.Integer, unique=False, nullable=False)
    id_plotly_options = db.Column(db.Integer, unique=False, nullable=False)
    id_pygal_options = db.Column(db.Integer, unique=False, nullable=False)

    @staticmethod
    def get_domain_and_step(chart_id):
        ''' Returns the list of 3 elements: begin, end and step of the function. '''
        chart = Exponential.query.get(chart_id)
        if chart:
            return [chart.x_begin, chart.x_end, chart.step] 
        else:
            return [0, 1, 0.1]
    
    @staticmethod
    def get_coefs(chart_id):
        ''' Returns the list of all model coefficients. '''
        chart = Exponential.query.get(chart_id)
        if chart:
            return [chart.a, chart.b, chart.c, chart.d]
        else:
            return ['?', '?', '?', '?']


class SquareFunc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x_begin = db.Column(db.Float, unique=False, nullable=False)
    x_end = db.Column(db.Float, unique=False, nullable=False)
    step = db.Column(db.Float, unique=False, nullable=False)

    a = db.Column(db.Float, unique=False, nullable=False)
    p = db.Column(db.Float, unique=False, nullable=False)
    q = db.Column(db.Float, unique=False, nullable=False)

    id_matplotlib_options = db.Column(db.Integer, unique=False, nullable=False)
    id_seaborn_options = db.Column(db.Integer, unique=False, nullable=False)
    id_bokeh_options = db.Column(db.Integer, unique=False, nullable=False)
    id_plotly_options = db.Column(db.Integer, unique=False, nullable=False)
    id_pygal_options = db.Column(db.Integer, unique=False, nullable=False)

    @staticmethod
    def get_domain_and_step(chart_id):
        ''' Returns the list of 3 elements: begin, end and step of the function. '''
        chart = SquareFunc.query.get(chart_id)
        if chart:
            return [chart.x_begin, chart.x_end, chart.step] 
        else:
            return [0, 1, 0.1]
    
    def get_coefs(chart_id):
        ''' Returns the list of all model coefficients. '''
        chart = SquareFunc.query.get(chart_id)
        if chart:
            return [chart.a, chart.p, chart.q]
        else:
            return ['?', '?', '?']



class CustomEquation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x_begin = db.Column(db.Float, unique=False, nullable=False)
    x_end = db.Column(db.Float, unique=False, nullable=False)
    step = db.Column(db.Float, unique=False, nullable=False)

    equation = db.Column(db.String, unique=False, nullable=False)

    id_matplotlib_options = db.Column(db.Integer, unique=False, nullable=False)
    id_seaborn_options = db.Column(db.Integer, unique=False, nullable=False)
    id_bokeh_options = db.Column(db.Integer, unique=False, nullable=False)
    id_plotly_options = db.Column(db.Integer, unique=False, nullable=False)
    id_pygal_options = db.Column(db.Integer, unique=False, nullable=False)

    @staticmethod
    def get_domain_and_step(chart_id):
        ''' Returns the list of 3 elements: begin, end and step of the function. '''
        chart = CustomEquation.query.get(chart_id)
        if chart:
            return [chart.x_begin, chart.x_end, chart.step] 
        else:
            return [0, 1, 0.1]
    
   



class MatplotlibPlotOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    color = db.Column(db.String, unique=False, nullable=False)
    outline_color = db.Column(db.String, unique=False, nullable=False)
    bg_color = db.Column(db.String, unique=False, nullable=False)
    line_width = db.Column(db.Integer, unique=False, nullable=False)
    line_style = db.Column(db.String, unique=False, nullable=False)
    marker = db.Column(db.String, unique=False, nullable=False)

    flag_bar_plot = db.Column(db.Boolean, unique=False, nullable=False)
    flag_scatter_plot = db.Column(db.Boolean, unique=False, nullable=False)
    flag_show_grid = db.Column(db.Boolean, unique=False, nullable=False)
    flag_logscale_x = db.Column(db.Boolean, unique=False, nullable=False)
    flag_logscale_y = db.Column(db.Boolean, unique=False, nullable=False)
    
    x_label = db.Column(db.String, unique=False, nullable=False)
    y_label = db.Column(db.String, unique=False, nullable=False)
    title = db.Column(db.String, unique=False, nullable=False)

    @staticmethod
    def get_options(options_id):
        ''' Returns the dictionary of options. '''
        chart = MatplotlibPlotOptions.query.get(options_id)
        
        if chart:
            return {
                'color': chart.color, 
                'outline_color': chart.outline_color, 
                'bg_color': chart.bg_color,
                'line_width': chart.line_width,
                'line_style': chart.line_style,
                'marker': chart.marker,
                'flag_bar_plot': chart.flag_bar_plot,
                'flag_scatter_plot': chart.flag_scatter_plot,
                'flag_show_grid': chart.flag_show_grid,
                'flag_logscale_x': chart.flag_logscale_x,
                'flag_logscale_y': chart.flag_logscale_y,
                'x_label': chart.x_label,
                'y_label': chart.y_label,
                'title': chart.title
            }
        else:
            return dict()


class SeabornPlotOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    color = db.Column(db.String, unique=False, nullable=False)
    bg_color = db.Column(db.String, unique=False, nullable=False)
    line_width = db.Column(db.Integer, unique=False, nullable=False)
    line_style = db.Column(db.String, unique=False, nullable=False)
    marker = db.Column(db.String, unique=False, nullable=False)

    flag_scatter_plot = db.Column(db.Boolean, unique=False, nullable=False)
    flag_show_grid = db.Column(db.Boolean, unique=False, nullable=False)
    flag_logscale_x = db.Column(db.Boolean, unique=False, nullable=False)
    flag_logscale_y = db.Column(db.Boolean, unique=False, nullable=False)
    
    x_label = db.Column(db.String, unique=False, nullable=False)
    y_label = db.Column(db.String, unique=False, nullable=False)
    title = db.Column(db.String, unique=False, nullable=False)

    @staticmethod
    def get_options(options_id):
        ''' Returns the dictionary of options. '''
        chart = SeabornPlotOptions.query.get(options_id)
        
        if chart:
            return {
                'color': chart.color, 
                'bg_color': chart.bg_color, 
                'line_width': chart.line_width,
                'line_style': chart.line_style,
                'marker': chart.marker,
                'flag_scatter_plot': chart.flag_scatter_plot,
                'flag_show_grid': chart.flag_show_grid,
                'flag_logscale_x': chart.flag_logscale_x,
                'flag_logscale_y': chart.flag_logscale_y,
                'x_label': chart.x_label,
                'y_label': chart.y_label,
                'title': chart.title
            }
        else:
            return dict()



class BokehPlotOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    color = db.Column(db.String, unique=False, nullable=False)
    bg_color = db.Column(db.String, unique=False, nullable=False)
    line_width = db.Column(db.Integer, unique=False, nullable=False)
    line_style = db.Column(db.String, unique=False, nullable=False)
    marker = db.Column(db.String, unique=False, nullable=False)

    flag_scatter_plot = db.Column(db.Boolean, unique=False, nullable=False)
    flag_show_grid = db.Column(db.Boolean, unique=False, nullable=False)
    flag_logscale_x = db.Column(db.Boolean, unique=False, nullable=False)
    flag_logscale_y = db.Column(db.Boolean, unique=False, nullable=False)
    
    @staticmethod
    def get_options(options_id):
        ''' Returns the dictionary of options. '''
        chart = BokehPlotOptions.query.get(options_id)
        
        if chart:
            return {
                'color': chart.color, 
                'bg_color': chart.bg_color,
                'line_width': chart.line_width,
                'line_style': chart.line_style,
                'marker': chart.marker,
                'flag_scatter_plot': chart.flag_scatter_plot,
                'flag_show_grid': chart.flag_show_grid,
                'flag_logscale_x': chart.flag_logscale_x,
                'flag_logscale_y': chart.flag_logscale_y
            }
        else:
            return dict()


class PlotlyPlotOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    color = db.Column(db.String, unique=False, nullable=False)
    bg_color = db.Column(db.String, unique=False, nullable=False)
    line_width = db.Column(db.Integer, unique=False, nullable=False)
    line_style = db.Column(db.String, unique=False, nullable=False)
    marker = db.Column(db.String, unique=False, nullable=False)

    flag_scatter_plot = db.Column(db.Boolean, unique=False, nullable=False)
    flag_show_grid = db.Column(db.Boolean, unique=False, nullable=False)
    flag_logscale_x = db.Column(db.Boolean, unique=False, nullable=False)
    flag_logscale_y = db.Column(db.Boolean, unique=False, nullable=False)
    
    @staticmethod
    def get_options(options_id):
        ''' Returns the dictionary of options. '''
        chart = PlotlyPlotOptions.query.get(options_id)
        
        if chart:
            return {
                'color': chart.color, 
                'bg_color': chart.bg_color, 
                'line_width': chart.line_width,
                'line_style': chart.line_style,
                'marker': chart.marker,
                'flag_scatter_plot': chart.flag_scatter_plot,
                'flag_show_grid': chart.flag_show_grid,
                'flag_logscale_x': chart.flag_logscale_x,
                'flag_logscale_y': chart.flag_logscale_y
            }
        else:
            return dict()



class PygalPlotOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    color = db.Column(db.String, unique=False, nullable=False)
    bg_color = db.Column(db.String, unique=False, nullable=False)
    line_width = db.Column(db.Integer, unique=False, nullable=False)
    line_style = db.Column(db.String, unique=False, nullable=False)
    marker = db.Column(db.String, unique=False, nullable=False)

    flag_scatter_plot = db.Column(db.Boolean, unique=False, nullable=False)
    flag_show_grid = db.Column(db.Boolean, unique=False, nullable=False)
    flag_logscale_y = db.Column(db.Boolean, unique=False, nullable=False)
    
    @staticmethod
    def get_options(options_id):
        ''' Returns the dictionary of options. '''
        chart = PygalPlotOptions.query.get(options_id)
        
        if chart:
            return {
                'color': chart.color, 
                'bg_color': chart.bg_color, 
                'line_width': chart.line_width,
                'line_style': chart.line_style,
                'marker': chart.marker,
                'flag_scatter_plot': chart.flag_scatter_plot,
                'flag_show_grid': chart.flag_show_grid,
                'flag_logscale_y': chart.flag_logscale_y
            }
        else:
            return dict()


class FileDataPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, unique=False, nullable=False)
    y = db.Column(db.Float, unique=False, nullable=False)

    @staticmethod
    def make_point(xx, yy):
        ''' Returns the FileDataPoint (x, y). '''
        return FileDataPoint(x=float(round(xx, 3)), y=float(round(yy, 3)))




class FilePlotOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    id_matplotlib_options = db.Column(db.Integer, unique=False, nullable=False)
    id_seaborn_options = db.Column(db.Integer, unique=False, nullable=False)
    id_bokeh_options = db.Column(db.Integer, unique=False, nullable=False)
    id_plotly_options = db.Column(db.Integer, unique=False, nullable=False)
    id_pygal_options = db.Column(db.Integer, unique=False, nullable=False)
    



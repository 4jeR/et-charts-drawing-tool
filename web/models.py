from web import db




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
        ''' Returns the range - list consisting two floats. '''
        coefs_ok = Sinus.query.get(chart_id)
        if coefs_ok:
            return [coefs_ok.x_begin, coefs_ok.x_end, coefs_ok.step] 
        else:
            return [0, 1, 0.1]
    
    @staticmethod
    def get_coefs(chart_id):
        ''' Returns the list of all model coefficients. '''
        coefs_ok = Sinus.query.get(chart_id)
        if coefs_ok:
            return [coefs_ok.a, coefs_ok.b, coefs_ok.c, coefs_ok.d]
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
        ''' Returns the range - list consisting two floats. '''
        coefs_ok = Cosinus.query.get(chart_id)
        if coefs_ok:
            return [coefs_ok.x_begin, coefs_ok.x_end, coefs_ok.step] 
        else:
            return [0, 1, 0.1]
    
    @staticmethod
    def get_coefs(chart_id):
        ''' Returns the list of all model coefficients. '''
        coefs_ok = Cosinus.query.get(chart_id)
        if coefs_ok:
            return [coefs_ok.a, coefs_ok.b, coefs_ok.c, coefs_ok.d]
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
        ''' Returns the range - list consisting two floats. '''
        coefs_ok = SquareRoot.query.get(chart_id)
        if coefs_ok:
            return [coefs_ok.x_begin, coefs_ok.x_end, coefs_ok.step] 
        else:
            return [0, 1, 0.1]
    
    @staticmethod
    def get_coefs(chart_id):
        ''' Returns the list of all model coefficients. '''
        coefs_ok = SquareRoot.query.get(chart_id)
        if coefs_ok:
            return [coefs_ok.a, coefs_ok.b, coefs_ok.c, coefs_ok.d]
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
        ''' Returns the range - list consisting two floats. '''
        coefs_ok = Exponential.query.get(chart_id)
        if coefs_ok:
            return [coefs_ok.x_begin, coefs_ok.x_end, coefs_ok.step] 
        else:
            return [0, 1, 0.1]
    
    @staticmethod
    def get_coefs(chart_id):
        ''' Returns the list of all model coefficients. '''
        coefs_ok = Exponential.query.get(chart_id)
        if coefs_ok:
            return [coefs_ok.a, coefs_ok.b, coefs_ok.c, coefs_ok.d]
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
        ''' Returns the range - list consisting two floats. '''
        coefs_ok = SquareFunc.query.get(chart_id)
        if coefs_ok:
            return [coefs_ok.x_begin, coefs_ok.x_end, coefs_ok.step] 
        else:
            return [0, 1, 0.1]
    
    def get_coefs(chart_id):
        ''' Returns the list of all model coefficients. '''
        coefs_ok = SquareFunc.query.get(chart_id)
        if coefs_ok:
            return [coefs_ok.a, coefs_ok.p, coefs_ok.q]
        else:
            return ['a', 'p', 'q']



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
        ''' Returns the range - list consisting two floats. '''
        coefs_ok = CustomEquation.query.get(chart_id)
        if coefs_ok:
            return [coefs_ok.x_begin, coefs_ok.x_end, coefs_ok.step] 
        else:
            return [0, 1, 0.1]
    
   



class MatplotlibPlotOptions(db.Model):
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
        coefs_ok = MatplotlibPlotOptions.query.get(options_id)
        
        if coefs_ok:
            return {
                'color': coefs_ok.color, 
                'bg_color': coefs_ok.bg_color,
                'line_width': coefs_ok.line_width,
                'line_style': coefs_ok.line_style,
                'marker': coefs_ok.marker,
                'flag_scatter_plot': coefs_ok.flag_scatter_plot,
                'flag_show_grid': coefs_ok.flag_show_grid,
                'flag_logscale_x': coefs_ok.flag_logscale_x,
                'flag_logscale_y': coefs_ok.flag_logscale_y
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
    
    @staticmethod
    def get_options(options_id):
        ''' Returns the dictionary of options. '''
        coefs_ok = SeabornPlotOptions.query.get(options_id)
        
        if coefs_ok:
            return {
                'color': coefs_ok.color, 
                'bg_color': coefs_ok.bg_color, 
                'line_width': coefs_ok.line_width,
                'line_style': coefs_ok.line_style,
                'marker': coefs_ok.marker,
                'flag_scatter_plot': coefs_ok.flag_scatter_plot,
                'flag_show_grid': coefs_ok.flag_show_grid,
                'flag_logscale_x': coefs_ok.flag_logscale_x,
                'flag_logscale_y': coefs_ok.flag_logscale_y
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
        coefs_ok = BokehPlotOptions.query.get(options_id)
        
        if coefs_ok:
            return {
                'color': coefs_ok.color, 
                'bg_color': coefs_ok.bg_color,
                'line_width': coefs_ok.line_width,
                'line_style': coefs_ok.line_style,
                'marker': coefs_ok.marker,
                'flag_scatter_plot': coefs_ok.flag_scatter_plot,
                'flag_show_grid': coefs_ok.flag_show_grid,
                'flag_logscale_x': coefs_ok.flag_logscale_x,
                'flag_logscale_y': coefs_ok.flag_logscale_y
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
        coefs_ok = PlotlyPlotOptions.query.get(options_id)
        
        if coefs_ok:
            return {
                'color': coefs_ok.color, 
                'bg_color': coefs_ok.bg_color, 
                'line_width': coefs_ok.line_width,
                'line_style': coefs_ok.line_style,
                'marker': coefs_ok.marker,
                'flag_scatter_plot': coefs_ok.flag_scatter_plot,
                'flag_show_grid': coefs_ok.flag_show_grid,
                'flag_logscale_x': coefs_ok.flag_logscale_x,
                'flag_logscale_y': coefs_ok.flag_logscale_y
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
        coefs_ok = PygalPlotOptions.query.get(options_id)
        
        if coefs_ok:
            return {
                'color': coefs_ok.color, 
                'bg_color': coefs_ok.bg_color, 
                'line_width': coefs_ok.line_width,
                'line_style': coefs_ok.line_style,
                'marker': coefs_ok.marker,
                'flag_scatter_plot': coefs_ok.flag_scatter_plot,
                'flag_show_grid': coefs_ok.flag_show_grid,
                'flag_logscale_y': coefs_ok.flag_logscale_y
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
    



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
    


'''   20.10.2020 
TODO: 
- Remodel all models below to be-like-this ^ 
- Fix bug with deleting all charts
- Remodel OptionsForms for each library (currently for Matplotlib) to specify only its chart id
- Fix taking image of the chart
- if len(charts) == 0 -> dont show cards with libraries
- Simulate click the 'changed library' card by JavaScript (like the selenium screenshooters)
'''
# class Image(db.Model):
#     __tablename__ = 'image'
#     image_id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(8))
#     # the one-to-one relation
#     blindmap = relationship("Blindmap", uselist=False, backref="image")

# class Blindmap(db.Model):
#     __tablename__ = 'blindmap'
#     module_id = db.Column(db.Integer, primary_key = True)
#     image_id = db.Column(db.Integer, ForeignKey('image.image_id'))


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


class FileDataPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, unique=False, nullable=False)
    y = db.Column(db.Float, unique=False, nullable=False)

    id_matplotlib_options = db.Column(db.Integer, unique=False, nullable=False)
    id_seaborn_options = db.Column(db.Integer, unique=False, nullable=False)
    id_bokeh_options = db.Column(db.Integer, unique=False, nullable=False)
    id_plotly_options = db.Column(db.Integer, unique=False, nullable=False)
    id_pygal_options = db.Column(db.Integer, unique=False, nullable=False)

    @staticmethod
    def make_point(xx, yy):
        ''' Returns the FileDataPoint (x, y). '''
        return FileDataPoint(x=float(round(xx, 3)), y=float(round(yy, 3)))



class MatplotlibPlotOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    color = db.Column(db.String, unique=False, nullable=False)
    line_width = db.Column(db.Integer, unique=False, nullable=False)
    line_style = db.Column(db.String, unique=False, nullable=False)
    marker = db.Column(db.String, unique=False, nullable=False)

    flag_scatter_plot = db.Column(db.Boolean, unique=False, nullable=False)
    flag_show_grid = db.Column(db.Boolean, unique=False, nullable=False)
    flag_logscale_y = db.Column(db.Boolean, unique=False, nullable=False)
    flag_show_legend = db.Column(db.Boolean, unique=False, nullable=False)
    
    @staticmethod
    def get_options(options_id):
        ''' Returns the list of all model coefficients. '''
        coefs_ok = MatplotlibPlotOptions.query.get(options_id)
        
        if coefs_ok:
            return {
                'color': coefs_ok.color, 
                'line_width': coefs_ok.line_width,
                'line_style': coefs_ok.line_style,
                'marker': coefs_ok.marker,
                'flag_scatter_plot': coefs_ok.flag_scatter_plot,
                'flag_show_grid': coefs_ok.flag_show_grid,
                'flag_logscale_y': coefs_ok.flag_logscale_y,
                'flag_show_legend': coefs_ok.flag_show_legend
            }
        else:
            return dict()


class SeabornPlotOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    color = db.Column(db.String, unique=False, nullable=False)
    line_width = db.Column(db.Integer, unique=False, nullable=False)
    line_style = db.Column(db.String, unique=False, nullable=False)
    marker = db.Column(db.String, unique=False, nullable=False)

    flag_scatter_plot = db.Column(db.Boolean, unique=False, nullable=False)
    flag_show_grid = db.Column(db.Boolean, unique=False, nullable=False)
    flag_logscale_y = db.Column(db.Boolean, unique=False, nullable=False)
    flag_show_legend = db.Column(db.Boolean, unique=False, nullable=False)
    
    @staticmethod
    def get_options(options_id):
        ''' Returns the list of all model coefficients. '''
        coefs_ok = SeabornPlotOptions.query.get(options_id)
        
        if coefs_ok:
            return {
                'color': coefs_ok.color, 
                'line_width': coefs_ok.line_width,
                'line_style': coefs_ok.line_style,
                'marker': coefs_ok.marker,
                'flag_scatter_plot': coefs_ok.flag_scatter_plot,
                'flag_show_grid': coefs_ok.flag_show_grid,
                'flag_logscale_y': coefs_ok.flag_logscale_y,
                'flag_show_legend': coefs_ok.flag_show_legend
            }
        else:
            return dict()



class BokehPlotOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    color = db.Column(db.String, unique=False, nullable=False)
    line_width = db.Column(db.Integer, unique=False, nullable=False)
    line_style = db.Column(db.String, unique=False, nullable=False)
    marker = db.Column(db.String, unique=False, nullable=False)

    flag_scatter_plot = db.Column(db.Boolean, unique=False, nullable=False)
    flag_show_grid = db.Column(db.Boolean, unique=False, nullable=False)
    flag_logscale_y = db.Column(db.Boolean, unique=False, nullable=False)
    flag_show_legend = db.Column(db.Boolean, unique=False, nullable=False)
    
    @staticmethod
    def get_options(options_id):
        ''' Returns the list of all model coefficients. '''
        coefs_ok = BokehPlotOptions.query.get(options_id)
        
        if coefs_ok:
            return {
                'color': coefs_ok.color, 
                'line_width': coefs_ok.line_width,
                'line_style': coefs_ok.line_style,
                'marker': coefs_ok.marker,
                'flag_scatter_plot': coefs_ok.flag_scatter_plot,
                'flag_show_grid': coefs_ok.flag_show_grid,
                'flag_logscale_y': coefs_ok.flag_logscale_y,
                'flag_show_legend': coefs_ok.flag_show_legend
            }
        else:
            return dict()


class PlotlyPlotOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    color = db.Column(db.String, unique=False, nullable=False)
    line_width = db.Column(db.Integer, unique=False, nullable=False)
    line_style = db.Column(db.String, unique=False, nullable=False)
    marker = db.Column(db.String, unique=False, nullable=False)

    flag_scatter_plot = db.Column(db.Boolean, unique=False, nullable=False)
    flag_show_grid = db.Column(db.Boolean, unique=False, nullable=False)
    flag_logscale_y = db.Column(db.Boolean, unique=False, nullable=False)
    flag_show_legend = db.Column(db.Boolean, unique=False, nullable=False)
    
    @staticmethod
    def get_options(options_id):
        ''' Returns the list of all model coefficients. '''
        coefs_ok = PlotlyPlotOptions.query.get(options_id)
        
        if coefs_ok:
            return {
                'color': coefs_ok.color, 
                'line_width': coefs_ok.line_width,
                'line_style': coefs_ok.line_style,
                'marker': coefs_ok.marker,
                'flag_scatter_plot': coefs_ok.flag_scatter_plot,
                'flag_show_grid': coefs_ok.flag_show_grid,
                'flag_logscale_y': coefs_ok.flag_logscale_y,
                'flag_show_legend': coefs_ok.flag_show_legend
            }
        else:
            return dict()



class PygalPlotOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    color = db.Column(db.String, unique=False, nullable=False)
    line_width = db.Column(db.Integer, unique=False, nullable=False)
    line_style = db.Column(db.String, unique=False, nullable=False)
    marker = db.Column(db.String, unique=False, nullable=False)

    flag_scatter_plot = db.Column(db.Boolean, unique=False, nullable=False)
    flag_show_grid = db.Column(db.Boolean, unique=False, nullable=False)
    flag_logscale_y = db.Column(db.Boolean, unique=False, nullable=False)
    flag_show_legend = db.Column(db.Boolean, unique=False, nullable=False)
    
    @staticmethod
    def get_options(options_id):
        ''' Returns the list of all model coefficients. '''
        coefs_ok = PygalPlotOptions.query.get(options_id)
        
        if coefs_ok:
            return {
                'color': coefs_ok.color, 
                'line_width': coefs_ok.line_width,
                'line_style': coefs_ok.line_style,
                'marker': coefs_ok.marker,
                'flag_scatter_plot': coefs_ok.flag_scatter_plot,
                'flag_show_grid': coefs_ok.flag_show_grid,
                'flag_logscale_y': coefs_ok.flag_logscale_y,
                'flag_show_legend': coefs_ok.flag_show_legend
            }
        else:
            return dict()
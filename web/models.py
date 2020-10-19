from web import db

from math import cos
from math import exp 
from math import log
from math import sin
from math import sqrt


class Sinus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, unique=False, nullable=False)
    y = db.Column(db.Float, unique=False, nullable=False)

    @staticmethod
    def make_point(x):
        ''' Returns the point (x, y) where y is calculated from equation (based on model coefficients). '''
        coefs = SinusCoefs.query.first()
        xx = float(round(x, 3))
        yy = float(round(coefs.a*sin(coefs.b*x - coefs.c) + coefs.d, 3)) 
        return Sinus(x=xx, y=yy)


class SinusCoefs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.Float, unique=False, nullable=False)
    b = db.Column(db.Float, unique=False, nullable=False)
    c = db.Column(db.Float, unique=False, nullable=False)
    d = db.Column(db.Float, unique=False, nullable=False)
    step = db.Column(db.Float, unique=False, nullable=False)

    @staticmethod
    def get_coefs():
        ''' Returns the list of all model coefficients. '''
        coefs_ok = SinusCoefs.query.first()
        
        if coefs_ok:
            return [coefs_ok.a, coefs_ok.b, coefs_ok.c, coefs_ok.d, coefs_ok.step] 
        else:
            return ['?' for i in range(5)]


class Cosinus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, unique=False, nullable=False)
    y = db.Column(db.Float, unique=False, nullable=False)


    @staticmethod
    def make_point(x):
        ''' Returns the point (x, y) where y is calculated from equation (based on model coefficients). '''
        coefs = CosinusCoefs.query.first()
        xx = float(round(x, 3))
        yy = float(round(coefs.a*cos(coefs.b*x - coefs.c) + coefs.d, 3))
        return Cosinus(x=xx, y=yy)


class CosinusCoefs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.Float, unique=False, nullable=False)
    b = db.Column(db.Float, unique=False, nullable=False)
    c = db.Column(db.Float, unique=False, nullable=False)
    d = db.Column(db.Float, unique=False, nullable=False)
    step = db.Column(db.Float, unique=False, nullable=False)

    @staticmethod
    def get_coefs():
        ''' Returns the list of all model coefficients. '''
        coefs_ok = CosinusCoefs.query.first()
        
        if coefs_ok:
            return [coefs_ok.a, coefs_ok.b, coefs_ok.c, coefs_ok.d, coefs_ok.step] 
        else:
            return ['?' for i in range(5)]


class SquareRoot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, unique=False, nullable=False)
    y = db.Column(db.Float, unique=False, nullable=False)

    @staticmethod
    def make_point(x):
        ''' Returns the point (x, y) where y is calculated from equation (based on model coefficients). '''
        coefs = SquareRootCoefs.query.first()
        xx = float(round(x, 3))
        yy = float(round(coefs.a*sqrt(coefs.b*x - coefs.c) + coefs.d, 3))
        return SquareRoot(x=xx, y=yy)


class SquareRootCoefs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.Float, unique=False, nullable=False)
    b = db.Column(db.Float, unique=False, nullable=False)
    c = db.Column(db.Float, unique=False, nullable=False)
    d = db.Column(db.Float, unique=False, nullable=False)
    step = db.Column(db.Float, unique=False, nullable=False)

    @staticmethod
    def get_coefs():
        ''' Returns the list of all model coefficients. '''
        coefs_ok = SquareRootCoefs.query.first()
        
        if coefs_ok:
            return [coefs_ok.a, coefs_ok.b, coefs_ok.c, coefs_ok.d, coefs_ok.step] 
        else:
            return ['?' for i in range(5)]


class Exponential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, unique=False, nullable=False)
    y = db.Column(db.Float, unique=False, nullable=False)

    @staticmethod
    def make_point(x):
        ''' Returns the point (x, y) where y is calculated from equation (based on model coefficients). '''
        coefs = ExponentialCoefs.query.first()
        xx = float(round(x, 3))
        yy = float(round(coefs.a*exp(coefs.b*(x - coefs.c)) + coefs.d, 3))
        return Exponential(x=xx, y=yy)


class ExponentialCoefs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.Float, unique=False, nullable=False)
    b = db.Column(db.Float, unique=False, nullable=False)
    c = db.Column(db.Float, unique=False, nullable=False)
    d = db.Column(db.Float, unique=False, nullable=False)
    step = db.Column(db.Float, unique=False, nullable=False)

    @staticmethod
    def get_coefs():
        ''' Returns the list of all model coefficients. '''
        coefs_ok = ExponentialCoefs.query.first()
        
        if coefs_ok:
            return [coefs_ok.a, coefs_ok.b, coefs_ok.c, coefs_ok.d, coefs_ok.step] 
        else:
            return ['?' for i in range(5)]


class SquareFunc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, unique=False, nullable=False)
    y = db.Column(db.Float, unique=False, nullable=False)

    @staticmethod
    def make_point(x):
        ''' Returns the point (x, y) where y is calculated from equation (based on model coefficients). '''
        coefs = SquareFuncCoefs.query.first()
        xx = float(round(x, 3))
        yy = float(round(coefs.a*((x - coefs.p)**2) + coefs.q, 3))
        return SquareFunc(x=xx, y=yy)


class SquareFuncCoefs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.Float, unique=False, nullable=False)
    p = db.Column(db.Float, unique=False, nullable=False)
    q = db.Column(db.Float, unique=False, nullable=False)
    step = db.Column(db.Float, unique=False, nullable=False)
    
    @staticmethod
    def get_coefs():
        ''' Returns the list of all model coefficients. '''
        coefs_ok = SquareFuncCoefs.query.first()
        
        if coefs_ok:
            return [coefs_ok.a, coefs_ok.p, coefs_ok.q, coefs_ok.step] 
        else:
            return ['?' for i in range(5)]


class FileDataPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, unique=False, nullable=False)
    y = db.Column(db.Float, unique=False, nullable=False)

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
    def get_options():
        ''' Returns the list of all model coefficients. '''
        coefs_ok = MatplotlibPlotOptions.query.first()
        
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
    def get_options():
        ''' Returns the list of all model coefficients. '''
        coefs_ok = MatplotlibPlotOptions.query.first()
        
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
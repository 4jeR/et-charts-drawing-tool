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
        xx = float(x)
        yy = float(coefs.a*sin(coefs.b*x - coefs.c) + coefs.d)
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
        xx = float(x)
        yy = float(coefs.a*cos(coefs.b*x - coefs.c) + coefs.d)
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
        xx = float(x)
        yy = float(coefs.a*sqrt(coefs.b*x - coefs.c) + coefs.d)
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
        xx = float(x)
        yy = float(coefs.a*exp(coefs.b*(x - coefs.c)) + coefs.d)
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
        xx = float(x)
        yy = float(coefs.a*((x - coefs.p)**2) + coefs.q)
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
        return FileDataPoint(x=float(xx), y=float(yy))
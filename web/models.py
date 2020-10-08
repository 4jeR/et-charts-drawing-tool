from web import db
from math import sin
from math import cos
from math import exp 
from math import sqrt
from math import log


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

    def __repr__(self):
        return f"{self.id}. Cosinus Point({self.x}, {self.y}) | a={self.a}, b={self.b}, c={self.c}, d={self.d}"

    @staticmethod
    def set_coefs(a=1, b=1, c=0, d=0, x_zero=0):
        Cosinus.a = a
        Cosinus.b = b
        Cosinus.c = c
        Cosinus.d = d
        Cosinus.x_zero = x_zero

    
    @staticmethod
    def get_coefs():
        ''' Returns the list of all model coefficients. '''
        coefs = [Cosinus.a, Cosinus.b, Cosinus.c, Cosinus.d]
        return coefs if all(coefs) else ['?' for i in range(4)]

    @staticmethod
    def make_point(x):
        xx = float(x)
        yy = float(Cosinus.a*cos(Cosinus.b*x - Cosinus.c) + Cosinus.d)
        return Cosinus(x=xx, y=yy)


class SquareRoot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, unique=False, nullable=False)
    y = db.Column(db.Float, unique=False, nullable=False)

    a = None
    b = None
    c = None
    d = None
    def __repr__(self):
        return f"{self.id}. Sqrt Point({self.x}, {self.y}) | a={self.a}, b={self.b}, c={self.c}, d={self.d}"

    @staticmethod
    def set_coefs(a=1, b=1, c=0, d=0, x_zero=0):
        SquareRoot.a = a
        SquareRoot.b = b
        SquareRoot.c = c
        SquareRoot.d = d
        SquareRoot.x_zero = x_zero
    
    @staticmethod
    def get_coefs():
        ''' Returns the list of all model coefficients. '''
        coefs = [SquareRoot.a, SquareRoot.b, SquareRoot.c, SquareRoot.d]
        return coefs if all(coefs) else ['?' for i in range(4)]

    @staticmethod
    def make_point(x):
        xx = float(x)
        yy = float(SquareRoot.a*sqrt(SquareRoot.b*x - SquareRoot.c) + SquareRoot.d)
        return SquareRoot(x=xx, y=yy)


class FileDataPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, unique=False, nullable=False)
    y = db.Column(db.Float, unique=False, nullable=False)

    
    def __repr__(self):
        return f"{self.id}. File Data Point({self.x}, {self.y})"
    
    @staticmethod
    def make_point(xx, yy):
        ''' Returns the FileDataPoint (x, y). '''
        return FileDataPoint(x=float(xx), y=float(yy))
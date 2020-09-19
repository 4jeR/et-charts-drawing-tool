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

    a = 1
    b = 1
    c = 0
    def __repr__(self):
        return f"{self.id}. Sinus Point({self.x}, {self.y}) | a={self.a}, b={self.b}, c={self.c}"

    
    # a*sin(x_zero + b*x) + c
    @staticmethod
    def set_coefs(a=1, b=1, c=0, x_zero=0):
        Sinus.a = a
        Sinus.b = b
        Sinus.c = c
        Sinus.x_zero = x_zero
    
    @staticmethod
    def make_point(x):
        xx = float(x)
        yy = float(Sinus.a*sin(Sinus.b*x)+Sinus.c)
        return Sinus(x=xx, y=yy)


class Cosinus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, unique=False, nullable=False)
    y = db.Column(db.Float, unique=False, nullable=False)

    a = 1
    b = 1
    c = 0
    def __repr__(self):
        return f"{self.id}. Cosinus Point({self.x}, {self.y}) | a={self.a}, b={self.b}, c={self.c}"


    # a*sin(x_zero + b*x) + c
    @staticmethod
    def set_coefs(a=1, b=1, c=0, x_zero=0):
        Cosinus.a = a
        Cosinus.b = b
        Cosinus.c = c
    
    @staticmethod
    def make_point(x):
        xx = float(x)
        yy = float(Cosinus.a*cos(Cosinus.b*x)+Cosinus.c)
        return Cosinus(x=xx, y=yy)


class SquareRoot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, unique=False, nullable=False)
    y = db.Column(db.Float, unique=False, nullable=False)

    a = 1
    b = 1
    c = 0
    def __repr__(self):
        return f"{self.id}. Sqrt Point({self.x}, {self.y}) | a={self.a}, b={self.b}, c={self.c}"


    # a*sin(x_zero + b*x) + c
    @staticmethod
    def set_coefs(a=1, b=1, c=0, x_zero=0):
        SquareRoot.a = a
        SquareRoot.b = b
        SquareRoot.c = c
        SquareRoot.x_zero = x_zero
    
    @staticmethod
    def make_point(x):
        xx = float(x)
        yy = float(SquareRoot.a*sqrt(SquareRoot.b*x)+SquareRoot.c)
        return SquareRoot(x=xx, y=yy)
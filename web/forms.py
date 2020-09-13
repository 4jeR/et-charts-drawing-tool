from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, FloatField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from web.models import *


class DataForm(FlaskForm):
    begin = FloatField('begin', validators=[DataRequired()])
    end = FloatField('end', validators=[DataRequired()])
    
class SinusForm(DataForm):
    coef_a = FloatField('a', validators=[DataRequired()])
    coef_b = FloatField('b', validators=[DataRequired()])
    coef_c = FloatField('c', validators=[DataRequired()])


    submit = SubmitField('Add data')

class CosinusForm(DataForm):
    coef_a = FloatField('a', validators=[DataRequired()])
    coef_b = FloatField('b', validators=[DataRequired()])
    coef_c = FloatField('c', validators=[DataRequired()])


    submit = SubmitField('Add data')
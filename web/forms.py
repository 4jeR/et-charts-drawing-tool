from flask_wtf import FlaskForm
from wtforms import StringField 
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms import SelectField
from wtforms import IntegerField
from wtforms import FloatField

from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError
from wtforms.validators import Length
from web.models import *


class DataForm(FlaskForm):
    begin = FloatField('begin', validators=[DataRequired()])
    end = FloatField('end', validators=[DataRequired()])
    
    coef_a = FloatField('a', validators=[DataRequired()])
    coef_b = FloatField('b', validators=[DataRequired()])
    coef_c = FloatField('c', validators=[DataRequired()])

    submit = SubmitField('Add data')


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


class SqrtForm(DataForm):
    coef_a = FloatField('a', validators=[DataRequired()])
    coef_b = FloatField('b', validators=[DataRequired()])
    coef_c = FloatField('c', validators=[DataRequired()])


    submit = SubmitField('Add data')
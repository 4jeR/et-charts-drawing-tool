from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, FloatField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from web.models import *


class PointForm(FlaskForm):
    x = FloatField('x', validators=[DataRequired()])
    y = FloatField('y', validators=[DataRequired()])
    
    submit = SubmitField('Add point')
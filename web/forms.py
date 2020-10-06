from flask_wtf import FlaskForm
from wtforms import StringField 
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms import SelectField
from wtforms import IntegerField
from wtforms import FloatField

from wtforms.validators import DataRequired
from wtforms.validators import InputRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError
from wtforms.validators import Length
from web.models import *


class DataForm(FlaskForm):
    begin = FloatField('begin', validators=[InputRequired()])
    end = FloatField('end', validators=[InputRequired()])
    
    coef_a = FloatField('a', validators=[DataRequired('Non-zero value.')])
    coef_b = FloatField('b', validators=[InputRequired()])
    coef_c = FloatField('c', validators=[InputRequired()])

    submit = SubmitField('Add data')

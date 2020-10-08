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
from wtforms.validators import NumberRange
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError
from wtforms.validators import Length
from web.models import *



def validate_begin_end(FormName):
    def _validate_begin_end(form, field):
        min_value = -FormName.coef_c.data / FormName.coef_b.data 
        if field.data >= min_value and field.data >= min_value:
            raise ValidationError(f'Min value must be atleast {min_value}')

    return _validate_begin_end

class DataForm(FlaskForm):
    begin = FloatField('begin', validators=[InputRequired()])
    end = FloatField('end', validators=[InputRequired()])
    
    coef_a = FloatField('a', validators=[DataRequired('Non-zero value.')])
    coef_b = FloatField('b', validators=[DataRequired('Non-zero value.')])
    coef_c = FloatField('c', validators=[InputRequired()])
    coef_d = FloatField('d', validators=[InputRequired()])
    step = FloatField('step', validators=[InputRequired()])

    submit = SubmitField('Add data')


class SqrtForm(FlaskForm):
    """ TODO: on submit check if begin and end are >= -c/b """

    
    begin = FloatField('begin', validators=[InputRequired()])
    end = FloatField('end', validators=[InputRequired()])

    coef_a = FloatField('a', validators=[DataRequired('Non-zero value.')])
    coef_b = FloatField('b', validators=[DataRequired('Non-zero value.')])
    coef_c = FloatField('c', validators=[InputRequired()])
    coef_d = FloatField('d', validators=[InputRequired()])
    step = FloatField('step', validators=[InputRequired()])

    submit = SubmitField('Add data')

    '''
    def validate(self):
        min_value = -self.coef_c.data / self.coef_b.data  
        if self.begin.data < min_value or self.end.data < min_value:
            return False
        else: 
            return True
        raise ValidationError(f'Min value must be atleast {min_value}')
    '''


class FromFileForm(FlaskForm):
    filename = StringField('Filename:',  validators=[DataRequired(), Length(min=3, max=40)])
    
    submit = SubmitField('Add data')

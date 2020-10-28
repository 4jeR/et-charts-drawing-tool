from flask_wtf import FlaskForm

from wtforms import BooleanField
from wtforms import FloatField
from wtforms import IntegerField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField 
from wtforms import SubmitField
from wtforms import FileField


from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import NumberRange
from wtforms.validators import Optional
from wtforms.validators import ValidationError


''' TODO: fix this function '''
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
    step = FloatField('step', validators=[Optional()])

    submit = SubmitField('Add data')


class SqrtForm(FlaskForm):
    """ TODO: on submit check if begin and end are >= -c/b """

    
    begin = FloatField('begin', validators=[InputRequired()])
    end = FloatField('end', validators=[InputRequired()])

    coef_a = FloatField('a', validators=[DataRequired('Non-zero value.')])
    coef_b = FloatField('b', validators=[DataRequired('Non-zero value.')])
    coef_c = FloatField('c', validators=[InputRequired()])
    coef_d = FloatField('d', validators=[InputRequired()])
    step = FloatField('step', validators=[Optional()])

    submit = SubmitField('Add data')


class SquareFuncForm(FlaskForm):
    begin = FloatField('begin', validators=[InputRequired()])
    end = FloatField('end', validators=[InputRequired()])

    coef_a = FloatField('a', validators=[InputRequired()])
    coef_p = FloatField('p', validators=[InputRequired()])
    coef_q = FloatField('q', validators=[InputRequired()])
    step = FloatField('step', validators=[Optional()])

    submit = SubmitField('Add data')


class FromFileForm(FlaskForm):
    filename = FileField('Filename:',  validators=[DataRequired()])
    
    submit = SubmitField('Add data')




class MatplotlibOptionsForm(FlaskForm):
    
    color = SelectField('Line color: ', choices=[
            ('#292928', 'black'),
            ('#f5f5f5', 'white'), 
            ('#92c720', 'green'), 
            ('#e00f00', 'red'),
            ('#05dbdb', 'cyan'),
            ('#d601d2', 'magenta'),
            ('#f8ff6e', 'yellow'),
            ('#4f84bd', 'blue')
        ]
    )

    bg_color = SelectField('Background color: ', choices=[
            ('#292928', 'black'),
            ('#f5f5f5', 'white'), 
            ('#92c720', 'green'), 
            ('#e00f00', 'red'),
            ('#05dbdb', 'cyan'),
            ('#d601d2', 'magenta'),
            ('#f8ff6e', 'yellow'),
            ('#4f84bd', 'blue')
        ]
    )


    line_width = SelectField('Line width: ', choices=[(val, val) for val in range(1, 11)])

    line_style = SelectField('Style: ', choices=[
            ('solid',  'solid'), 
            ('dashed', 'dashed'), 
            ('dotted',  'dotted'),
            ('dashed-dotted', 'dashed-dotted')
        ]
    )
    
    marker = SelectField('Marker: ', choices=[
            ('.', 'dot'), 
            ('+', 'plus'),
            ('*', 'star'),
            ('x', 'cross'),
            ('s', 'square'),
            ('o', 'circle'), 
            ('d', 'diamond'),
            ('^', 'triangle'),
            ('_', 'underscore')
        ]
    )

    flag_scatter_plot = BooleanField("Scatter:")
    flag_show_grid = BooleanField("Grid:")
    flag_logscale_x = BooleanField("Log scale X:")
    flag_logscale_y = BooleanField("Log scale Y:")
    
    submit = SubmitField('Add data')


class SeabornOptionsForm(FlaskForm):
    
    color = SelectField('Line color: ', choices=[
            ('#292928', 'black'),
            ('#f5f5f5', 'white'), 
            ('#92c720', 'green'), 
            ('#e00f00', 'red'),
            ('#05dbdb', 'cyan'),
            ('#d601d2', 'magenta'),
            ('#f8ff6e', 'yellow'),
            ('#4f84bd', 'blue')
        ]
    )

    bg_color = SelectField('Background color: ', choices=[
            ('#292928', 'black'),
            ('#f5f5f5', 'white'), 
            ('#92c720', 'green'), 
            ('#e00f00', 'red'),
            ('#05dbdb', 'cyan'),
            ('#d601d2', 'magenta'),
            ('#f8ff6e', 'yellow'),
            ('#4f84bd', 'blue')
        ]
    )

    line_width = SelectField('Line width: ', choices=[(val, val) for val in range(1, 11)])

    line_style = SelectField('Style: ', choices=[
            ('solid',  'solid'), 
            ('dashed', 'dashed')
        ]
    )

    marker = SelectField('Marker: ', choices=[
            ('.', 'dot'), 
            ('+', 'plus'),
            ('*', 'star'),
            ('x', 'cross'),
            ('s', 'square'),
            ('o', 'circle'), 
            ('d', 'diamond'),
            ('^', 'triangle'),
            ('_', 'underscore')
        ]
    )

    flag_scatter_plot = BooleanField("Scatter:")
    flag_show_grid = BooleanField("Grid:")
    flag_logscale_x = BooleanField("Log scale X:")
    flag_logscale_y = BooleanField("Log scale Y:")
    
    submit = SubmitField('Add data')


class BokehOptionsForm(FlaskForm):
    color = SelectField('Line color: ', choices=[
            ('#292928', 'black'),
            ('#f5f5f5', 'white'), 
            ('#92c720', 'green'), 
            ('#e00f00', 'red'),
            ('#05dbdb', 'cyan'),
            ('#d601d2', 'magenta'),
            ('#f8ff6e', 'yellow'),
            ('#4f84bd', 'blue')
        ]
    )

    bg_color = SelectField('Background color: ', choices=[
            ('#292928', 'black'),
            ('#f5f5f5', 'white'), 
            ('#92c720', 'green'), 
            ('#e00f00', 'red'),
            ('#05dbdb', 'cyan'),
            ('#d601d2', 'magenta'),
            ('#f8ff6e', 'yellow'),
            ('#4f84bd', 'blue')
        ]
    )

    line_width = SelectField('Line width: ', choices=[(val, val) for val in range(1, 11)])

    line_style = SelectField('Style: ', choices=[
            ('solid',  'solid'), 
            ('dashed', 'dashed'), 
            ('dotted',  'dotted'),
            ('dashdot', 'dashed-dotted')
        ]
    )
    
    marker = SelectField('Marker: ', choices=[
            ('.', 'dot'), 
            ('+', 'plus'),
            ('*', 'star'),
            ('x', 'cross'),
            ('s', 'square'),
            ('o', 'circle'), 
            ('d', 'diamond'),
            ('^', 'triangle'),
            ('_', 'underscore')
        ]
    )

    flag_scatter_plot = BooleanField("Scatter:")
    flag_show_grid = BooleanField("Grid:")
    flag_logscale_x = BooleanField("Log scale X:")
    flag_logscale_y = BooleanField("Log scale Y:")
    
    submit = SubmitField('Add data')


class PlotlyOptionsForm (FlaskForm):
    color = SelectField('Line color: ', choices=[
            ('#292928', 'black'),
            ('#f5f5f5', 'white'), 
            ('#92c720', 'green'), 
            ('#e00f00', 'red'),
            ('#05dbdb', 'cyan'),
            ('#d601d2', 'magenta'),
            ('#f8ff6e', 'yellow'),
            ('#4f84bd', 'blue')
        ]
    )

    bg_color = SelectField('Background color: ', choices=[
            ('#292928', 'black'),
            ('#f5f5f5', 'white'), 
            ('#92c720', 'green'), 
            ('#e00f00', 'red'),
            ('#05dbdb', 'cyan'),
            ('#d601d2', 'magenta'),
            ('#f8ff6e', 'yellow'),
            ('#4f84bd', 'blue')
        ]
    )
    

    line_width = SelectField('Line width: ', choices=[(val, val) for val in range(1, 11)])

    line_style = SelectField('Style: ', choices=[
            ('solid',  'solid'), 
            ('dash', 'dashed'), 
            ('dot',  'dotted'),
            ('dashdot', 'dashed-dotted')
        ]
    )

    marker = SelectField('Marker: ', choices=[
            ('asterisk', 'asterisk'),
            ('star', 'star'),
            ('cross', 'cross'),
            ('square', 'square'),
            ('circle', 'circle'), 
            ('diamond', 'diamond'),
            ('triangle-up', 'triangle'),
        ]
    )

    flag_scatter_plot = BooleanField("Scatter:")
    flag_show_grid = BooleanField("Grid:")
    flag_logscale_x = BooleanField("Log scale X:")
    flag_logscale_y = BooleanField("Log scale Y:")
    
    submit = SubmitField('Add data')


class PygalOptionsForm (FlaskForm):
    color = SelectField('Line color: ', choices=[
            ('#292928', 'black'),
            ('#f5f5f5', 'white'), 
            ('#92c720', 'green'), 
            ('#e00f00', 'red'),
            ('#05dbdb', 'cyan'),
            ('#d601d2', 'magenta'),
            ('#f8ff6e', 'yellow'),
            ('#4f84bd', 'blue')
        ]
    )

    bg_color = SelectField('Background color: ', choices=[
            ('#292928', 'black'),
            ('#f5f5f5', 'white'), 
            ('#92c720', 'green'), 
            ('#e00f00', 'red'),
            ('#05dbdb', 'cyan'),
            ('#d601d2', 'magenta'),
            ('#f8ff6e', 'yellow'),
            ('#4f84bd', 'blue')
        ]
    )
    

    line_width = SelectField('Line width: ', choices=[(val, val) for val in range(1, 11)])

    line_style = SelectField('Style: ', choices=[
            ('solid',  'solid'), 
            ('dash', 'dashed'), 
            ('dot',  'dotted'),
            ('dashdot', 'dashed-dotted')
        ]
    )

    marker = SelectField('Marker: ', choices=[
            ('asterisk', 'asterisk'),
            ('star', 'star'),
            ('cross', 'cross'),
            ('square', 'square'),
            ('circle', 'circle'), 
            ('diamond', 'diamond'),
            ('triangle-up', 'triangle'),
        ]
    )

    flag_scatter_plot = BooleanField("Scatter:")
    flag_show_grid = BooleanField("Grid:")
    flag_logscale_y = BooleanField("Log scale Y:")
    
    submit = SubmitField('Add data')
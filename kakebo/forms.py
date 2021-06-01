import imp
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class MovimientosForm(FlaskForm):
    fecha = DateField('Fecha', validators=[DataRequired()])
    concepto = StringField('Concepto', validators=[DataRequired(), Length(min=10)])
    categoria = SelectField('Categoria', choices=[('SU', 'Supervivencia'), ('OV', 'Ocio/Vicio'), ('CU', 'Cultura'), ('EX', ' Extras')])
    submit = SubmitField('Aceptar')
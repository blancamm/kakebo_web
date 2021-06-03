from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SelectField, SubmitField, FloatField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date

def fecha_por_debajo_de_hoy(formulario, campo):
    if campo.data ==None:
        return  
    hoy = date.today()
    if campo.data > hoy: #RECUERDA QUE LA FECHA PARA COMPARAR TIENE QUE SER AÑO/MES/DIA
        raise ValidationError('La fecha debe ser menor que hoy')



class MovimientosForm(FlaskForm):
    id = HiddenField()
    fecha = DateField('Fecha', validators=[DataRequired(message="Debe informar de la fecha"), fecha_por_debajo_de_hoy])
    concepto = StringField('Concepto', validators=[DataRequired(), Length(min=5)])
    categoria = SelectField('Categoria', choices=[('00',''), ('SU', 'Supervivencia'), ('OV', 'Ocio/Vicio'), ('CU', 'Cultura'), ('EX', ' Extras')])
    cantidad = FloatField('Cantidad', validators=[DataRequired()])
    esGasto = BooleanField('Es gasto')
    submit = SubmitField('Aceptar')

class FiltarMovimientos(FlaskForm):
    fechaDesde = DateField("Desde", validators=[fecha_por_debajo_de_hoy], default=date(2021,1,1)) #aqui no se esta ejecutando la funcion, es decir, se ejecuta cuando hago el validate del formulario, 
                                                                        #por eso no lleva () (fecha_por_debajo_de_hoy) porque en el momento de definirlo no se tiene que ejecutar, solo cuando lo valido la fecha
    fechaHasta = DateField("Hasta", validators=[fecha_por_debajo_de_hoy], default= date.today())
    texto = StringField("Concepto")
    submit=SubmitField("Filtrar")

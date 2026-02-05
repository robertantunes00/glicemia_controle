from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired

class GlicemiaForm(FlaskForm):
    valor = IntegerField('Valor (mg/dL)', validators=[DataRequired()])
    periodo = SelectField('Selecione o período', choices=[
        ('jejum', 'Jejum'),
        ('2_horas_apos_cafe', '2h após café'),
        ('antes_do_almoco', 'Antes do almoço'),
        ('2_horas_apos_almoco', '2h após almoço'),
        ('antes_do_jantar', 'Antes do jantar'),
        ('2_horas_apos_jantar', '2h após jantar'),
        ('antes_de_dormir', 'Antes de dormir'),
        ('3_horas', '3h da madrugada')
    ])
    submit = SubmitField('Enviar')
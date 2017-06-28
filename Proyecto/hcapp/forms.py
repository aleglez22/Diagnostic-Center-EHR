from . import models as m
from django.db import models
from django import forms

class TipoEstudioForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=m.Categoria.objects.all())
    subcategoria = forms.ModelChoiceField(queryset=m.Subcategoria.objects.none()) # Need to populate this using jquery
    estudio = forms.ModelChoiceField(queryset=m.TipoEstudio.objects.none()) # Need to populate this using jquery

    class Meta:
        model = m.TipoEstudio
        fields = ('categoria', 'subcategoria', 'estudio')

class PedidoForm(forms.Form):

	
    class Meta:
        model = m.Pedido
        fields = ('Paciente', 'Medico', 'Diagnostico_presuntivo', 'Fecha_pedido')
       
class PacienteForm(forms.ModelForm):
    

    class Meta:
        model = m.Paciente
        fields = '__all__'

    
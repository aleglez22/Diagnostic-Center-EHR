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



from django.core.exceptions import ValidationError

def validar_cliente_existe(value):
    cliente = m.Paciente.objects.filter(Cedula=value)
    if not cliente: # check if any object exists
        raise ValidationError('paciente no existe, por favor registrelo') 

def validar_estudio_existe(value):
    estudio = m.TipoEstudio.objects.filter(Nombre=value)
    if not estudio: # check if any object exists
        raise ValidationError('estudio no existe') 


class PedidoForm(forms.Form):
    Paciente = forms.CharField(validators=[validar_cliente_existe], widget=forms.TextInput(attrs={'class': 'form-control'}))
    Medico= forms.CharField(label='Médico solicitante',required=False)
    Fecha= forms.DateField(label='Fecha Pedido',required=False)
    Estudio=forms.CharField(label='Tipo de estudio',validators=[validar_estudio_existe])
    Diagnostico=forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)
        for x, y in self.fields.items():
            self.fields[x].widget.attrs.update({'class': 'form-control'})

class NombreEstudioForm(forms.Form):
    Estudio=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Tipo de estudio',validators=[validar_estudio_existe],required=False)

       
class EstudioForm(forms.Form):
    Campo = forms.CharField(label ='Historia', widget=forms.Textarea,required=False)
    Conclusion=forms.CharField(label='Conclusión',required=False)


class PacienteForm(forms.ModelForm):
    
    class Meta:
        model = m.Paciente
        fields = '__all__'

    #se le añade  linea al constructor para modificar campo
    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)
        self.fields['Apellido'].widget.attrs['value'] = 'gonza'
    
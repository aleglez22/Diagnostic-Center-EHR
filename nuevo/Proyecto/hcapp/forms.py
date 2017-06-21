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

class EstudioForm(forms.Form):
    Campo = models.TextField()
    Conclusion = models.TextField()  # charfield
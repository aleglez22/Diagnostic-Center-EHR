from django.shortcuts import render, redirect , get_object_or_404
from .models import Paciente, Categoria, Estudio, MedicoSolicitante, Pedido, Radiologo, Subcategoria
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponse


#ejemplo de funcion que retorna varios pacientes
def Inicio(request):
    pacientes=Paciente.objects.all()
    return render(request,"inicio.html",{ 'pacientes': pacientes})


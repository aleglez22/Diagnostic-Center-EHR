from django.shortcuts import render, redirect , get_object_or_404
from .models import Paciente, Secretario, Medico, Categoria, TipoEstudio, MedicoSolicitante, Pedido, Radiologo, Subcategoria
from django.views import generic
from django.apps import apps
from . import models as m
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponse


#ejemplo de funcion que retorna varios pacientes
def Inicio(request):
    pacientes=Paciente.objects.all()
    return render(request,"inicio.html",{ 'pacientes': pacientes})

##CONTROLADORES DE PACIENTES##

#vista para Home_pacientes

class CrearPaciente(generic.CreateView):
    model = Paciente
    fields = ['Cedula','Nombre','Apellido','Telefono','Edad','Fecha_nacimiento']


class ListaPaciente(generic.ListView):
    template_name = 'hcapp/pacientes.html'
    context_object_name='pacientes'

    # @Override devuelve los objetos que serán renderizados
    def get_queryset(self):
        return Paciente.objects.all().order_by('-Fecha_ingreso')

class EliminarPaciente(generic.DeleteView):
    model= Paciente
    success_url= reverse_lazy("hcapp:Home-pacientes")

class EditarPaciente (generic.UpdateView):
    model= Paciente
    fields = ['Telefono', 'Edad', 'Fecha_nacimiento']


##CONTROLADORES DE HISTORIAS##

class CrearPedido(generic.CreateView):
    model = Pedido
    fields = ['Paciente','Medico','Diagnostico_presuntivo']

class DetallePedido(generic.DetailView):
    model=Pedido
    template_name = 'hcapp/detalle_pedido.html'

class ListaPedidos(generic.ListView):
    template_name = 'hcapp/pedidos.html'
    context_object_name='pedidos'

    # @Override devuelve los objetos que serán renderizados
    def get_queryset(self):
        return Pedido.objects.all().order_by('-Fecha')


class FactoryHistoria():
    def getTipo(self,nombreEstudio):
        return apps.get_model(app_label="hcapp",model_name=nombreEstudio)



class ListaHistoria(generic.ListView):
    template_name = 'hcapp/historias.html'
    context_object_name='historias'

    # @Override devuelve los objetos que serán renderizados
    def get_queryset(self):
        return m.Estudio.objects.all().order_by('-Fecha_ingreso')



#pasarle como parametro el nombre de la tabla a modificar utilizando factory

# class CrearEstudio(generic.CreateView):
#     model = #tabla
#     pass
#
# class DetalleEstudio(generic.DetailView):
#     model= #tabla
#     template_name = 'hcapp/detalle_estudio.html'

class ListaEstudio(generic.ListView):
    template_name = 'hcapp/estudios.html'
    context_object_name='estudios'

class EditarEstudio (generic.UpdateView):
    #model= tabla
    #fields = todos
    pass

class EliminarEstudio(generic.DeleteView):
    # model= tabla
    success_url= reverse_lazy("hcapp:Home-estudios")




##CONTROLADORES DE MEDICO##

class CrearMedico(generic.CreateView):
    model = Medico
    fields = ['Nombre','Apellido','Telefono']


class DetalleMedico(generic.DetailView):
    model=Medico
    template_name = 'hcapp/detalle_medico.html'

class ListaMedico(generic.ListView):
    template_name = 'hcapp/medicos.html'
    context_object_name='medicos'


class EliminarMedico(generic.DeleteView):
    model= Medico
    success_url= reverse_lazy("hcapp:Home-pacientes")

class EditarMedico (generic.UpdateView):
    model= Medico
    fields = ['Nombre','Apellido','Telefono']



##CONTROLADORES DE SECRETARIOS##

class CrearSecretario(generic.CreateView):
    model = Secretario
    fields = ['Nombre','Apellido','Telefono']


class DetalleSecretario(generic.DetailView):
    model=Secretario
    template_name = 'hcapp/detalle_secretario.html'

class ListaSecretario(generic.ListView):
    template_name = 'hcapp/secretarios.html'
    context_object_name='secretarios'


class EliminarSecretario(generic.DeleteView):
    model= Secretario
    success_url= reverse_lazy("hcapp:Home-secretario")

class EditarSecretario (generic.UpdateView):
    model= Secretario
    fields = ['Nombre','Apellido','Telefono']
from django.shortcuts import render, redirect , get_object_or_404
from .models import Paciente, Secretario, Medico, Categoria, TipoEstudio, MedicoSolicitante, Pedido, Radiologo, Subcategoria
from django.views import generic
from django.apps import apps
from . import models as m
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponse
from .forms import  TipoEstudioForm
import json
from docx import Document
from . import filler  

#ejemplo de funcion que retorna varios pacientes
def Inicio(request):
    pacientes=Paciente.objects.all()
    return render(request,"hcapp/home.html",{})

def Pruebaselect(request):
    form=TipoEstudioForm()
    return render(request,"hcapp/prueba_select.html",{ 'form': form})



def DescargarDoc(request,historia_id, nombre_estudio):
    historia= m.Historia.objects.get(pk=historia_id)
    campo_nuevo=str(historia.Campo)
    plantilla = m.Plantilla.objects.get(TipoEstudio=nombre_estudio)
    nombre_doc=str(plantilla.NombreDoc)
    campo_viejo=str(plantilla.Campo)
    print (campo_viejo)

    pedido=Pedido.objects.get(Historia=historia)
    nombre_paciente=str(pedido.Paciente.Nombre) +' '+ str(pedido.Paciente.Apellido)
    medico_solicitante= str(pedido.Medico.Nombre) +' '+ str(pedido.Medico.Apellido)
    fecha=historia.Fecha_creacion
    edad_paciente=pedido.Paciente.Edad

    document=filler.reemplaza('realizan',campo_nuevo,nombre_paciente,edad_paciente,medico_solicitante,
        fecha,nombre_doc )

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=download.docx'
    document.save(response)
    return response



##CONTROLADORES DE PACIENTES##

#vista para Home_pacientes
def PacienteHome(request):
    ultimos=Paciente.objects.all().order_by('-Fecha_ingreso')[:10]
    context={'ultimos_pacientes':ultimos}
    return  render(request, "pacientes.html", context )

class CrearPaciente(generic.CreateView):
    model = Paciente
    fields = ['Cedula','Nombre','Apellido','Telefono','Edad','Fecha_nacimiento']
    #needs paciente_form.html

    def get_context_data(self, **kwargs):
        ctx = super(CrearPaciente, self).get_context_data(**kwargs)
        ultimos=Paciente.objects.all().order_by('-Fecha_ingreso')[:10]
        ctx['ultimos'] = ultimos
        return ctx

class ListaPaciente(generic.ListView):
    template_name = 'hcapp/lista_pacientes.html'
    context_object_name='pacientes'

    # @Override devuelve los objetos que serán renderizados
    def get_queryset(self):
        return Paciente.objects.all().order_by('-Fecha_ingreso')

class EliminarPaciente(generic.DeleteView):
    model= Paciente
    success_url= reverse_lazy("hcapp:Home-Pacientes")

class EditarPaciente (generic.UpdateView):
    model= Paciente
    fields = ['Telefono', 'Edad', 'Fecha_nacimiento']
    #needs paciente_form.html


##CONTROLADORES DE HISTORIAS##

def PedidosHome(request):
    return render(request, "pedidos_home.html")


def CrearPedido(request):

    if request.method== "POST":
        if request.POST.get('f_estudio'):
            estudio=request.POST.get('f_estudio')
        elif request.POST.get('f_estudio_auto'):
            estudio = request.POST.get('f_estudio_auto')
        else:
            print("error")
        if TipoEstudio.objects.get(pk =estudio) ==False:#######ojoooo
            print("error")

        if request.POST.get('f_medico'):
            if MedicoSolicitante.objects.get(pk=request.POST.get('f_medico')):
                request.session['medico'] =request.POST.get('f_medico')
            else:
                print("error")
        else:
            print("error")
        if request.POST.get('f_paciente'):
            if MedicoSolicitante.objects.get(pk=request.POST.get('f_paciente')):
                request.session['paciente'] = request.POST.get('f_paciente')
            else:
                print("error")
        else:
            print("error")
        request.session ['diagnostico']=request.POST.get('f_diagnostico')
        plantilla=m.Plantilla.objects.get(TipoEstudio=estudio)
        campo=plantilla.Campo
        conclusion=plantilla.Conclusion
        form = EstudioForm()
        form.Campo = campo
        form.Conclusion = conclusion

        datos={ 'estudio': estudio,
                'campo':campo, 'conclusion':conclusion, 'form':form}

    return render(request, "crear_historia.html", datos)

##como obtener el contexto de otra vista

def GuardarHistoria(request,estudio):
    if request.method == "POST":
        form = EstudioForm(request.POST)
        if form.is_valid():
            campos = form.save(commit=False)
            historia= m.Historia(TipoEstudio=estudio, Campo=campos.Campo, Conclusion=campos.Conclusion)
            pedido = Pedido(Paciente= request.session['paciente'], Medico= request.session['medico'],
            Diagnostico_presuntivo= request.session['diagnostico'], Historia=historia)

            if request.POST.get("boton_guardarysalir"):
                pedido.save()
                return redirect("PedidosHome")
            elif request.POST.get("boton_guardar2"):
                pedido.save()
                request.session['pedido']=pedido
                if request.POST.get('f_estudio'):
                    estudio = request.POST.get('f_estudio')
                elif request.POST.get('f_estudio_auto'):
                    estudio = request.POST.get('f_estudio_auto')
                else:
                    print("error")
                if TipoEstudio.objects.get(pk=estudio) == False:
                    print("error")

                plantilla = m.Plantilla.objects.get(TipoEstudio=estudio)
                campo = plantilla.Campo
                conclusion = plantilla.Conclusion
                form = EstudioForm()
                form.Campo=campo
                form.Conclusion=conclusion
                datos={'pedido':pedido,'campo':campo, 'conclusion':conclusion, 'form':form}

                return render(request, "crear_otra_historia.html", datos)
    else:
        form = EstudioForm()
    return render(request, 'crear_historia.html', {'form': form})



def GuardarOtraHistoria(request,estudio):
    if request.method == "POST":
        form = EstudioForm(request.POST)
        if form.is_valid():
            campos = form.save(commit=False)
            historia= m.Historia(TipoEstudio=estudio, Campo=campos.Campo, Conclusion=campos.Conclusion)
            pedido = request.session['pedido']
            pedido.historia=historia

            if request.POST.get("boton_guardarysalir"):
                pedido.save()
                return redirect("PedidosHome")
            elif request.POST.get("boton_guardar2"):
                pedido.save()
                request.session['pedido']=pedido
                if request.POST.get('f_estudio'):
                    estudio = request.POST.get('f_estudio')
                elif request.POST.get('f_estudio_auto'):
                    estudio = request.POST.get('f_estudio_auto')
                else:
                    print("error")
                if TipoEstudio.objects.get(pk=estudio) == False:
                    print("error")

                plantilla = m.Plantilla.objects.get(TipoEstudio=estudio)
                campo = plantilla.Campo
                conclusion = plantilla.Conclusion
                form = EstudioForm()
                form.Campo=campo
                form.Conclusion=conclusion

                datos={'pedido':pedido,'campo':campo, 'conclusion':conclusion, 'form':form}
                return render(request, "crear_otra_historia.html", datos)
    else:
        form = EstudioForm()
    return render(request, 'crear_historia', {'form': form})


class DetallePedido(generic.DetailView):
    model=Pedido
    template_name = 'hcapp/detalle_pedido.html'

class ListaPedidos(generic.ListView):
    template_name = 'hcapp/pedidos.html'
    context_object_name='pedidos'

    # @Override devuelve los objetos que serán renderizados
    def get_queryset(self):
        return Pedido.objects.all().order_by('-Fecha')

class ListaHistorias(generic.ListView):
    template_name = 'hcapp/historias.html'
    context_object_name='historias'

    # @Override devuelve los objetos que serán renderizados
    def get_queryset(self):
        return Pedido.objects.all().order_by('-Fecha')

class FactoryHistoria():
    def getTipo(self,nombreEstudio):
        return apps.get_model(app_label="hcapp",model_name=nombreEstudio)

'''
class EditarHistoria(generic.UpdateView):
    model = m.Historia.CerebroSimple
    fields = '__all__'
    #jodido buscar solucu¿ion
'''


def AutocompletarPaciente(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        lista = Paciente.objects.filter(Apellido = q )[:20]
        results = []
        for fila in lista:
            fila_json = {}
            fila_json['id'] = fila.pk
            fila_json['label'] = str(fila.Apellido) +" "+ str(fila.Nombre)
            fila_json['value'] = fila.Cedula
            results.append(fila_json)
        print (results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

    ###MEDICOSOLICITANTE###

def AutocompletarMedicoSolicitante(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        lista = MedicoSolicitante.objects.filter(Apellido = q )[:20]
        results = []
        for fila in lista:
            fila_json = {}
            fila_json['id'] = fila.pk
            fila_json['label'] = str(fila.Apellido) +" "+ str(fila.Nombre)
            fila_json['value'] = fila.Apellido
            results.append(fila_json)
        print (results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


    ###ESTUDIOS###

def AutocompletarTipoEstudio(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        lista = TipoEstudio.objects.filter(Nombre = q )[:20]
        results = []
        for fila in lista:
            fila_json = {}
            fila_json['id'] = fila.pk
            fila_json['label'] = str(fila.Nombre)
            fila_json['value'] = fila.pk
            results.append(fila_json)
        print (results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)



def GetSubcategoria(request, categoria_id):
    categoria = Categoria.objects.get(pk=categoria_id)
    subcategorias = Subcategoria.objects.filter(Categoria=categoria)
    contexto = {}
    for subcategoria in subcategorias:
        contexto[subcategoria.id] = subcategoria.Nombre
    return HttpResponse(json.dumps(contexto), content_type="application/json")

def GetEstudio(request, subcategoria_id):
    subcategoria = Subcategoria.objects.get(pk=subcategoria_id)
    estudios = TipoEstudio.objects.filter(Subcategoria=subcategoria)
    contexto = {}
    for estudio in estudios:
        contexto[estudio.id] = estudio.Nombre
    return HttpResponse(json.dumps(contexto), content_type="application/json")



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
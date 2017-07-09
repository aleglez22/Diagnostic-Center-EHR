from django.shortcuts import render, redirect , get_object_or_404
from .models import Paciente, Secretario, Medico, Categoria, TipoEstudio, MedicoSolicitante, Pedido, Radiologo, Subcategoria
from django.views import generic
from django.apps import apps
from . import models as m
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponse
from .forms import  TipoEstudioForm, PacienteForm, PedidoForm, NombreEstudioForm, EstudioForm
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

def PruebaTabla(request):
    return render(request,"hcapp/prueba_table.html",{})

def Tabla(request):
    
    historias= m.Historia.objects.all()
    lista=[]
    listaDatos=[]
    print (historias)

    for historia in historias:
        pk=historia.pk
        pedido= historia.Pedido
        p=pedido.pk
        medico= pedido.Medico.Nombre
        paciente=pedido.Paciente.Cedula
        tipo_estudio=historia.TipoEstudio
        fecha_historia= historia.Fecha_creacion
        fecha_pedido= pedido.Fecha_pedido

        lista=[str(pk),str(p),str(medico),str(paciente),str(tipo_estudio),str(fecha_historia),
        str(fecha_pedido)]
        listaDatos.append(lista)
    
    dic={"data":listaDatos}

    
    mimetype = 'application/json'
    return HttpResponse(json.dumps(dic), mimetype)



def DescargarDoc(request,historia_id):
    historia= m.Historia.objects.get(pk=historia_id)
    campo_nuevo=str(historia.Campo)
    plantilla = m.Plantilla.objects.get(TipoEstudio=historia.TipoEstudio)
    nombre_doc=str(plantilla.NombreDoc)
    campo_viejo=str(plantilla.Campo)
    print (campo_viejo)

    pedido=historia.Pedido #---cambio
    nombre_paciente=str(pedido.Paciente.Nombre) +' '+ str(pedido.Paciente.Apellido)
    medico_solicitante= str(pedido.Medico.Nombre) +' '+ str(pedido.Medico.Apellido)
    fecha=historia.Fecha_creacion
    edad_paciente=pedido.Paciente.Edad

    document=filler.reemplaza('##campo##',campo_nuevo,nombre_paciente,edad_paciente,medico_solicitante,
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
    return  render(request, "hcapp/paciente_form.html", context )



class CrearPaciente(generic.CreateView):
    model = Paciente
    fields = ['Cedula','Nombre','Apellido','Telefono','Fecha_nacimiento']
    template_name_suffix ='_form'
    #form_class= PacienteForm
    success_url =reverse_lazy('hcapp:Crear-Paciente')


    ##se puede utilizar el form_class o el metodo get_form para modificar el formulario
    def get_form(self, form_class=None ):
        form = super(CrearPaciente, self).get_form(form_class)
        #form.fields['Apellido'].label= "Apellido" #edita los atributos del form >>ref/forms/fields/
        #form.fields['Apellido'].widget.attrs.update({'value': 'pppppp'}) #actualiza los valores del html
        #form.fields['Nombre'].widget.attrs['value']='form-control' #otra forma
        #form.fields['Apellido'].widget.attrs.update({'placeholder': 'Apellido','size': 10})
        #form.fields['Apellido'].widget.attrs.update({'id': 'juan'})
        
        for x, y in form.fields.items():
            form.fields[x].widget.attrs.update({'class': 'form-control'})
    
        return form

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
    nform=NombreEstudioForm()
    form=PedidoForm()
    drop=TipoEstudioForm()
    ultimos_pedidos= Pedido.objects.order_by('-Fecha')[:10]
    context={'form':form, 'nombre_estudio_form':nform,
    'drop_form':drop, 'ultimos_pedidos':ultimos_pedidos}
    return render(request, "hcapp/pedidos_home.html",context )


def CrearPedido1(request):
    form=PedidoForm()  
    nform=NombreEstudioForm()
    drop=TipoEstudioForm()

    if request.method=="POST":
        form=PedidoForm(request.POST)
        if form.is_valid():
            estudio=form.cleaned_data['Estudio']
            request.session['paciente']=form.cleaned_data['Paciente']
            request.session['diagnostico']=form.cleaned_data['Diagnostico']
            import datetime
            if form.cleaned_data['Fecha']=='':
                request.session['fecha']=datetime.datetime.now().date()
            else:
                request.session['fecha']=form.cleaned_data['Fecha']


             #es el pk porq no puedo verificar el nombre y apell
            if MedicoSolicitante.objects.get(pk=form.cleaned_data['Medico']): 
                request.session['medico']=form.cleaned_data['Medico']
            else:
                request.session['medico']=MedicoSolicitante.objects.get(pk=1)

            plantilla=m.Plantilla.objects.get(TipoEstudio=estudio)
            campo=plantilla.Campo
            conclusion=plantilla.Conclusion
            data={'Campo':campo, 'Conclusion':conclusion}
            form_historia = EstudioForm(data)
            nform=NombreEstudioForm()
            request.session['estudio']=estudio

            datos={'campo':campo, 'conclusion':conclusion, 'form':form_historia, 'nombre_estudio_form':nform, 'drop_form':drop}
            return render(request, "hcapp/crear_historia.html", datos)

 
    else:        
        return render(request, 'hcapp/pedidos_home.html', {'form': form,'nombre_estudio_form':nform, 'drop_form':drop})
    return render(request, 'hcapp/pedidos_home.html', {'form': form,'nombre_estudio_form':nform, 'drop_form':drop})


def GuardarHistoria(request):
    drop=TipoEstudioForm()
    form = EstudioForm()
    nform=NombreEstudioForm()
    if request.method == "POST":
        form = EstudioForm(request.POST)
        if form.is_valid():
            
            
            pedido = Pedido(Paciente= Paciente.objects.get(Cedula=request.session['paciente']), Medico= MedicoSolicitante.objects.get(pk=request.session['medico']),
            Diagnostico_presuntivo= request.session['diagnostico'], Fecha_pedido=request.session['fecha'])
            pedido.save()
            historia= m.Historia(TipoEstudio=request.session['estudio'], Campo=form.cleaned_data['Campo'], Conclusion=form.cleaned_data['Conclusion'],Pedido=pedido)
            

            if request.POST.get("boton_guardarysalir"):
                historia.save()
                
                return redirect (reverse_lazy("hcapp:Home-Pedidos"))
            elif request.POST.get("boton_guardar2"):
                
                historia.save()
                request.session['pedido']=pedido.pk
                nform= NombreEstudioForm(request.POST)
                estudio=request.POST.get('Estudio')
                
                if nform.is_valid() and m.Plantilla.objects.filter(TipoEstudio=estudio).exists():
                    plantilla = m.Plantilla.objects.get(TipoEstudio=estudio)
                    campo = plantilla.Campo
                    conclusion = plantilla.Conclusion
                    data={'Campo':campo, 'Conclusion':conclusion}
                    form = EstudioForm(data)
                    nform=NombreEstudioForm()
                    datos={'campo':campo, 'conclusion':conclusion, 'form':form, 'nombre_estudio_form':nform, 'drop_form':drop}
                    return render(request, "hcapp/crear_otra_historia.html", datos)
                else:
                    nform=NombreEstudioForm()
                    return render(request, "hcapp/error_estudio.html", {'nombre_estudio_form':nform, 'drop_form':drop})
    return render(request, 'hcapp/crear_historia.html', {'form': form,'nombre_estudio_form':nform ,'drop_form':drop })


def GuardarOtraHistoria(request):
    form = EstudioForm()
    nform=NombreEstudioForm()
    drop=TipoEstudioForm()
    
    if request.method == "POST":
        form = EstudioForm(request.POST)
        if form.is_valid():
            pedido= Pedido.objects.get(pk=request.session['pedido'])
            historia= m.Historia(TipoEstudio=request.session['estudio'], Campo=form.cleaned_data['Campo'], Conclusion=form.cleaned_data['Conclusion'],Pedido=pedido)       
            
            if request.POST.get("boton_guardarysalir"):
                historia.save()
                del request.session['pedido']
                return redirect (reverse_lazy("hcapp:Home-Pedidos"))
            elif request.POST.get("boton_guardar2"):
                historia.save()
                request.session['pedido']=pedido.pk
                nform= NombreEstudioForm(request.POST)            
                estudio=request.POST.get('Estudio')
                
                if nform.is_valid() and m.Plantilla.objects.filter(TipoEstudio=estudio).exists():
                    plantilla = m.Plantilla.objects.get(TipoEstudio=estudio)
                    campo = plantilla.Campo
                    conclusion = plantilla.Conclusion
                    data={'Campo':campo, 'Conclusion':conclusion}
                    form = EstudioForm(data)
                    nform=NombreEstudioForm()
                    datos={'campo':campo, 'conclusion':conclusion, 'form':form, 'nombre_estudio_form':nform, 'drop_form':drop}
                    return render(request, "hcapp/crear_otra_historia.html", datos)
                else:
                    nform=NombreEstudioForm()
                    return render(request, "hcapp/error_estudio.html", {'nombre_estudio_form':nform, 'drop_form':drop})

    return render(request, 'hcapp/crear_historia.html', {'form': form,'nombre_estudio_form':nform, 'drop_form':drop })


def CasoErrorNestudio(request):
    nform=NombreEstudioForm(request.POST)
    estudio=request.POST.get('Estudio')
    if nform.is_valid() and m.Plantilla.objects.filter(TipoEstudio=estudio).exists():
        plantilla = m.Plantilla.objects.get(TipoEstudio=estudio)
        campo = plantilla.Campo
        conclusion = plantilla.Conclusion
        data={'Campo':campo, 'Conclusion':conclusion}
        form = EstudioForm(data)
        nform=NombreEstudioForm()
        datos={'campo':campo, 'conclusion':conclusion, 'form':form, 'nombre_estudio_form':nform}
        return render(request, "hcapp/crear_otra_historia.html", datos)
    
    return render(request, "hcapp/error_estudio.html", {'nombre_estudio_form':nform})






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


import unicodedata
def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def AutocompletarPaciente(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        lista = Paciente.objects.filter(Apellido__startswith = q ).order_by('Apellido')[:20]
        results = []
        for fila in lista:
            fila_json = {}
            fila_json['id'] = fila.pk
            fila_json['label'] = elimina_tildes(str(fila.Apellido)) +" "+ elimina_tildes(str(fila.Nombre))
            fila_json['value'] = fila.Cedula
            results.append(fila_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

    ###MEDICOSOLICITANTE###

def AutocompletarMedicoSolicitante(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        lista = MedicoSolicitante.objects.filter(Apellido__startswith = q ).order_by('Apellido')[:20]
        results = []
        for fila in lista:
            fila_json = {}
            fila_json['id'] = fila.pk
            fila_json['label'] = elimina_tildes(str(fila.Apellido)) +" "+ elimina_tildes(str(fila.Nombre))
            fila_json['value'] = fila.pk
            results.append(fila_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


    ###ESTUDIOS###

def AutocompletarTipoEstudio(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        lista = TipoEstudio.objects.filter(Nombre__startswith = q ).order_by('Nombre')[:20]
        results = []
        for fila in lista:
            fila_json = {}
            fila_json['id'] = fila.pk
            fila_json['label'] = elimina_tildes(str(fila.Nombre))
            fila_json['value'] = str(fila.Nombre)
            results.append(fila_json)
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
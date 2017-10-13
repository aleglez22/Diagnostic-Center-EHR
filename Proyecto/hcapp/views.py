from django.shortcuts import render, redirect , get_object_or_404
from .models import Paciente, Historia, Categoria, TipoEstudio, MedicoSolicitante, Pedido, Subcategoria
from django.views import generic, View
from django.apps import apps
from . import models as m
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from .forms import  TipoEstudioForm, PacienteForm, PedidoForm, NombreEstudioForm, EstudioForm, RangoFechasForm
import json
from docx import Document
from . import filler
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from datetime import date
from django.db.models import Count
from .cedula import verificar
from django.core.exceptions import ValidationError
import os


def superuser_or_medico(user):
    return user.is_superuser or user.groups.filter(name='medicos').exists()

def superuser(user):
    return user.is_superuser

def superuser_or_secretario(user):
    return user.is_superuser or user.groups.filter(name='secretarios').exists()

def get_edad(born):
    today = date.today()
    if born is None:
        return 'error edad'
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

class MyFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if os.path.exists(self.path(name)):
            os.remove(self.path(name))
        return name

def UploadPlantilla(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = MyFileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'hcapp/subir_plantilla.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'hcapp/subir_plantilla.html')
    

#ejemplo de funcion que retorna varios pacientes
def Inicio(request):
    pacientes=Paciente.objects.all()
    return render(request,"hcapp/home.html",{})


def Historias(request):
    return render(request,"hcapp/prueba_table.html",{})



def TablaPacientes(request):
    
    pacientes= Paciente.objects.all()
    lista=[]
    listaDatos=[]

    for p in pacientes:

        address="'/editar/paciente/{0}'".format(p.pk)
        btn_editar='<button class="btn btn-primary btn-block" type="button" id="modificar_paciente"  onclick="window.location.href={0}">  <span class="glyphicon glyphicon-pencil"></span></button>'.format(address)

        lista=[str(p.Cedula),str(p.Nombre)+' '+str(p.Apellido),str(p.Telefono),str(get_edad(p.Fecha_nacimiento)),str(p.Fecha_nacimiento),
        str(p.Fecha_ingreso), str(btn_editar)]
        listaDatos.append(lista)
    
    dic={"data":listaDatos}
    mimetype = 'application/json'
    return HttpResponse(json.dumps(dic), mimetype)


def TablaHistorias(request):
    
    historias= m.Historia.objects.all()
    lista=[]
    listaDatos=[]
    print (historias)

    for historia in historias:
        address="'/editar/historia/{0}'".format(historia.pk)
        btn_editar='<button class="btn btn-primary btn-block" type="button" id="modificar_paciente"  onclick="window.location.href={0}">  <span class="glyphicon glyphicon-pencil"></span></button>'.format(address)
       
        pk=historia.pk
        pk="<a href='/historia/{0}'> h{1} </a>".format(pk, pk)
        pedido= historia.Pedido
        p=pedido.pk

        medico= pedido.Medico.Nombre
        paciente=pedido.Paciente.Cedula
        tipo_estudio=historia.TipoEstudio
        fecha_historia= historia.Fecha_creacion
        fecha_pedido= pedido.Fecha_pedido
        nombre_paciente=str(pedido.Paciente.Nombre) +" "+ str(pedido.Paciente.Apellido)

        lista=[str(pk),'p'+str(p),str(medico),str(paciente),str(nombre_paciente),str(tipo_estudio),str(fecha_historia),
        str(fecha_pedido), str(btn_editar)]
        listaDatos.append(lista)
    
    dic={"data":listaDatos}

    
    mimetype = 'application/json'
    return HttpResponse(json.dumps(dic), mimetype)



class DetalleHistoria(generic.DetailView):
    model=m.Historia
    template_name = 'hcapp/detalle_historia.html'

    def get_context_data(self, **kwargs):
        contexto=super(DetalleHistoria, self).get_context_data(**kwargs)

        historia_actual= Historia.objects.get(pk=self.kwargs['pk'])
        print('historia_actual '+str(historia_actual.pk))
        estudio_actual= historia_actual.TipoEstudio
        print('estudio_actual '+str(estudio_actual))

        pedido_actual= Pedido.objects.get(pk=historia_actual.Pedido.pk)
        print('pedido actual '+str(pedido_actual.pk))

        pedidos=Pedido.objects.filter(Paciente= pedido_actual.Paciente)
        print('pedidos '+str(pedidos)) #pedidos en los que esta el paciente actual

        historias= Historia.objects.filter(Pedido=pedidos, TipoEstudio=estudio_actual)
        print('historias  '+str(historias)) #pedidos en los que esta el paciente actual
        contexto['historias_paciente']= historias
        return contexto

class EditarHistoria(generic.UpdateView):
    model=Historia
    fields = ['Campo', 'Conclusion']
    template_name_suffix ='_editform'
    success_url =reverse_lazy('hcapp:Tabla-Historias')



def DescargarDoc(request,historia_id):
    historia= m.Historia.objects.get(pk=historia_id)
    campo_nuevo=str(historia.Campo)
    plantilla = m.Plantilla.objects.get(TipoEstudio=historia.TipoEstudio)
    nombre_doc=str(plantilla.NombreDoc)
    campo_viejo=str(plantilla.Campo)
    print (campo_viejo)

    pedido=historia.Pedido 
    nombre_paciente=str(pedido.Paciente.Nombre) +' '+ str(pedido.Paciente.Apellido)
    medico_solicitante= str(pedido.Medico.Nombre) +' '+ str(pedido.Medico.Apellido)
    fecha=historia.Fecha_creacion
    edad_paciente=get_edad(pedido.Paciente.Fecha_nacimiento)
    tipo_estudio=historia.TipoEstudio

    document=filler.reemplaza(campo_viejo,campo_nuevo,nombre_paciente,edad_paciente,medico_solicitante,
        fecha,nombre_doc )
    nombre_fichero=str(nombre_paciente) + ' '+ str(tipo_estudio)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename={0}.docx'.format(nombre_fichero)
    document.save(response)
    return response



##CONTROLADORES DE PACIENTES##

#vista para Home_pacientes

def validar_cedula(value):
    cedula = verificar(str(value))
    print("valor")
    print(value)
    if not cedula: 
        raise ValidationError('Cédula incorrecta') 

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
        form.fields['Cedula'].validators=[validar_cedula]
        
        for x, y in form.fields.items():
            form.fields[x].widget.attrs.update({'class': 'form-control'})
    
        return form

    def get_context_data(self, **kwargs):
        ctx = super(CrearPaciente, self).get_context_data(**kwargs)
        ultimos=Paciente.objects.all().order_by('-Fecha_ingreso')[:10]
        ctx['ultimos'] = ultimos
        return ctx



class EliminarPaciente(generic.DeleteView):
    model= Paciente
    success_url= reverse_lazy("hcapp:Crear-Paciente")

class EditarPaciente (generic.UpdateView):
    model= Paciente
    fields = ['Telefono', 'Nombre', 'Apellido','Fecha_nacimiento']
    template_name_suffix ='_editform'
    #needs paciente_form.html


##CONTROLADORES DE HISTORIAS##


#@user_passes_test(superuser_or_medico)
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
            request.session['cortecia']=form.cleaned_data['Cortecia']
            request.session['fecha']=str(form.cleaned_data['Fecha'])


             #es el pk porq no puedo verificar el nombre y apell
            if MedicoSolicitante.objects.get(pk=form.cleaned_data['Medico']): 
                request.session['medico']=form.cleaned_data['Medico']
            else:
                request.session['medico']=MedicoSolicitante.objects.get(pk=1)
            estudio_obj= TipoEstudio.objects.get(Nombre=estudio)
            plantilla=m.Plantilla.objects.get(TipoEstudio=estudio_obj)
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
            Diagnostico_presuntivo= request.session['diagnostico'], Fecha_pedido=request.session['fecha'], Cortecia=request.session['cortecia'])
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
                
                if nform.is_valid() and m.Plantilla.objects.filter(TipoEstudio= TipoEstudio.objects.filter(Nombre=estudio)).exists():
                    plantilla = m.Plantilla.objects.get(TipoEstudio=TipoEstudio.objects.get(Nombre=estudio))
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
                
                if nform.is_valid() and m.Plantilla.objects.filter(TipoEstudio= TipoEstudio.objects.filter(Nombre=estudio)).exists():
                    plantilla = m.Plantilla.objects.get(TipoEstudio=TipoEstudio.objects.get(Nombre=estudio))
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
    if nform.is_valid() and m.Plantilla.objects.filter(TipoEstudio= TipoEstudio.objects.filter(Nombre=estudio)).exists():
        plantilla = m.Plantilla.objects.get(TipoEstudio=TipoEstudio.objects.get(Nombre=estudio))
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


class FactoryHistoria():
    def getTipo(self,nombreEstudio):
        return apps.get_model(app_label="hcapp",model_name=nombreEstudio)


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



######  REPORTES   ########
#@login_required
def ReportesHome(request):
    form=RangoFechasForm()
    return render(request,"hcapp/reportes_home.html",{'form':form})

from django.contrib.messages.views import SuccessMessageMixin

class RegistrarPlaca(SuccessMessageMixin, generic.CreateView):
    model = m.Placa
    fields = '__all__'
    template_name_suffix ='_form'
    success_url =reverse_lazy('hcapp:Registrar-Placa')
    success_message = 'Se ha registrado una placa dañada'
    
    


    



def ReporteCortecias(request):
    today = date.today()
    form=RangoFechasForm(request.POST)
    if request.POST:    
        if form.is_valid():
            f_ini=form.cleaned_data['Fecha_inicial']
            f_fin=form.cleaned_data['Fecha_final']
            print(form.cleaned_data)

            if (f_ini != None) and (f_fin != None):
                a = Pedido.objects.filter(Fecha__range=(f_ini, f_fin), Cortecia=True)
                print("ambas")
            elif (f_ini != None):
                a = Pedido.objects.filter(Fecha__range=(f_ini, today), Cortecia=True)
                f_fin=today
                print("inicial")
            else:
                a = Pedido.objects.filter(Cortecia=True)
                print("ninguna")
                
            return render(request,'hcapp/reportes.html', {'pedidos':a,'fechainicial':f_ini, 'fechafinal': f_fin})
    return redirect (reverse_lazy("hcapp:Home-Reportes"))



class Reporte(View):
    today = date.today()
    model=Pedido
    template='hcapp/reportes.html'
    date_field_name = 'Fecha__range'
    context_name='pedidos'

    
    def post(self, request, *args, **kwargs): 
        form=RangoFechasForm(request.POST) 
        if form.is_valid():
            f_ini=form.cleaned_data['Fecha_inicial']
            f_fin=form.cleaned_data['Fecha_final']
            print(form.cleaned_data)

            if (f_ini != None) and (f_fin != None):
                
                context =self.model.objects.filter(**{self.date_field_name: (f_ini,f_fin)}) 
                print("ambas")
            elif (f_ini != None):
                context = self.model.objects.filter(**{self.date_field_name: (f_ini,self.today)}) 
                print("inicial")
                f_fin=today
            else:
                context = self.model.objects.all()
                print("ninguna")
                
            return render(request,self.template, {self.context_name:context, 'fechainicial':f_ini, 'fechafinal': f_fin})
        return redirect (reverse_lazy("hcapp:Home-Reportes"))


class ReportePacientes(View):
    today = date.today()
    context_name='pacientes'
    template='hcapp/reportes.html'
    
    
    def post(self, request, *args, **kwargs): 
        form=RangoFechasForm(request.POST) 
        if form.is_valid():
            f_ini=form.cleaned_data['Fecha_inicial']
            f_fin=form.cleaned_data['Fecha_final']
            print(form.cleaned_data)

            if (f_ini != None) and (f_fin != None):
                
                pedidos =Pedido.objects.filter(Fecha__range=(f_ini,f_fin)) 
                print("ambas")
            elif (f_ini != None):
                pedidos = Pedido.objects.filter(Fecha__range=(f_ini,self.today)) 
                print("inicial")
                f_fin=today
            else:
                pedidos = Pedido.objects.all()
                print("ninguna")

            # ####a= pedidos.annotate(edad=get_edad(pedidos.values('Paciente__Fecha_nacimiento')))<<<<<

            lista=[]
            contexto={}

            for x in pedidos:

                if get_edad(x.Paciente.Fecha_nacimiento) in contexto :
                    contexto[get_edad(x.Paciente.Fecha_nacimiento)]+=1
                else:
                    contexto[get_edad(x.Paciente.Fecha_nacimiento)]=1
            print(contexto)


            for x, y in contexto.items():
                lista.append({'edad':x, 'cantidad':y})
                
            return render(request,self.template, {self.context_name:lista, 'fechainicial':f_ini, 'fechafinal': f_fin})
        return redirect (reverse_lazy("hcapp:Home-Reportes"))


class ReportePlacas(View):
    today = date.today()
    context_name='placas'
    template='hcapp/reportes.html'

    
    def post(self, request, *args, **kwargs): 
        form=RangoFechasForm(request.POST) 
        if form.is_valid():
            f_ini=form.cleaned_data['Fecha_inicial']
            f_fin=form.cleaned_data['Fecha_final']
            print(form.cleaned_data)

            if (f_ini != None) and (f_fin != None):
                
                placas =m.Placa.objects.filter(Fecha__range=(f_ini,f_fin)) 
                print("ambas")
            elif (f_ini != None):
                placas = m.Placa.objects.filter(Fecha__range=(f_ini,self.today)) 
                print("inicial")
                f_fin=today
            else:
                placas = m.Placa.objects.all()
                print("ninguna")

            
            contexto= placas.values('Tipo').annotate(cantidad=Count('Tipo'))
            print( 'cantidad:'+str(contexto) )

            return render(request,self.template, {self.context_name:contexto,'fechainicial':f_ini, 'fechafinal': f_fin})
        return redirect (reverse_lazy("hcapp:Home-Reportes"))




class ReporteEstudios(View):
    today = date.today()
    context_name='historias'
    template='hcapp/reportes.html'

    def post(self, request, *args, **kwargs): 
        form=RangoFechasForm(request.POST) 
        if form.is_valid():
            f_ini=form.cleaned_data['Fecha_inicial']
            f_fin=form.cleaned_data['Fecha_final']
            print(form.cleaned_data)

            if (f_ini != None) and (f_fin != None):
                
                historias =Historia.objects.filter(Fecha__range=(f_ini,f_fin)) 
                print("ambas")
            elif (f_ini != None):
                historias = Historia.objects.filter(Fecha__range=(f_ini,self.today)) 
                print("inicial")
                f_fin=today
            else:
                historias = Historia.objects.all()
                print("ninguna")

            contexto= historias.values('TipoEstudio').annotate(cantidad=Count('TipoEstudio'))

            return render(request,self.template, {self.context_name:contexto,'fechainicial':f_ini, 'fechafinal': f_fin})
        return redirect (reverse_lazy("hcapp:Home-Reportes"))


class ReporteMedicos(View):
    today = date.today()
    context_name='medicos'
    template='hcapp/reportes.html'

    def post(self, request, *args, **kwargs): 
        form=RangoFechasForm(request.POST) 
        if form.is_valid():
            f_ini=form.cleaned_data['Fecha_inicial']
            f_fin=form.cleaned_data['Fecha_final']
            print(form.cleaned_data)

            if (f_ini != None) and (f_fin != None):
                
                pedidos =Pedido.objects.filter(Fecha__range=(f_ini,f_fin)) 
                print("ambas")
            elif (f_ini != None):
                pedidos = Pedido.objects.filter(Fecha__range=(f_ini,self.today)) 
                print("inicial")
                f_fin=today
            else:
                pedidos = Pedido.objects.all()
                print("ninguna")

            contexto= pedidos.values('Medico__Nombre','Medico__Apellido').annotate(cantidad=Count('Medico'))
            #print( 'cantidad:'+str(contexto) )



            return render(request,self.template, {self.context_name:contexto,'fechainicial':f_ini, 'fechafinal': f_fin})
        return redirect (reverse_lazy("hcapp:Home-Reportes"))




##CONTROLADORES DE MEDICOSOLICITANTE##

class CrearMedico(generic.CreateView):
    model = MedicoSolicitante
    fields = ['Nombre','Apellido','Telefono']
    success_url=reverse_lazy("hcapp:Home-Pedidos")

    def get_context_data(self, **kwargs):
        ctx = super(CrearMedico, self).get_context_data(**kwargs)
        medicos=MedicoSolicitante.objects.all().order_by('-Fecha')
        ctx['medicos'] = medicos
        return ctx


class DetalleMedico(generic.DetailView):
    model=MedicoSolicitante
    template_name = 'hcapp/detalle_medico.html'


class ListaMedico(generic.ListView):
    template_name = 'hcapp/medicos.html'
    context_object_name='medicos'

    
    def get_queryset(self):
        return MedicoSolicitante.objects.all().order_by('-Fecha')


class EliminarMedico(generic.DeleteView):
    model= MedicoSolicitante
    success_url= reverse_lazy("hcapp:Crear-Paciente")

class EditarMedico (generic.UpdateView):
    model= MedicoSolicitante
    fields = ['Nombre','Apellido','Telefono']
    success_url=reverse_lazy("hcapp:Crear-Medico")

    def get_context_data(self, **kwargs):
        ctx = super(EditarMedico, self).get_context_data(**kwargs)
        medicos=MedicoSolicitante.objects.all().order_by('-Fecha')
        ctx['medicos'] = medicos
        return ctx


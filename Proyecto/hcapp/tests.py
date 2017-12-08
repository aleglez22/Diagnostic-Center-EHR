from django.test import TestCase
#from .models import Paciente
#from . import models
#from .views import FactoryHistoria
from . import  views

# Create your tests here.

#
class FactoryHistoriaTest(TestCase):
    def test_return_requested_model(self):
        print("nombre: "+ str(Paciente.__name__))
        nombre_modelo=Paciente.__name__
        objeto=FactoryHistoria.getTipo(self, str(nombre_modelo))
        print ("modelo devuelto: "+ str(objeto.__name__))

        self.assertEqual(Paciente, FactoryHistoria.getTipo(self, Paciente.__name__))

def DescargarDoc(request,historia_id):
    historia= m.Historia.objects.get(pk=historia_id)
    campo_nuevo=str(historia.Campo)
    conclusion=str(historia.Conclusion)
    #print ("conclusion:"+ str(conclusion))
    plantilla = TipoEstudio.objects.get(Nombre=historia.TipoEstudio).Plantilla
    nombre_doc=str(plantilla.NombreDoc)
    campo_viejo=str(plantilla.Campo)

    pedido=historia.Pedido 
    nombre_paciente=str(pedido.Paciente.Nombre) +' '+ str(pedido.Paciente.Apellido)
    medico_solicitante= str(pedido.Medico.Nombre) +' '+ str(pedido.Medico.Apellido)
    fecha=historia.Fecha_creacion
    edad_paciente=get_edad(pedido.Paciente.Fecha_nacimiento)
    tipo_estudio=historia.TipoEstudio

    document=filler.reemplaza(campo_viejo,campo_nuevo,conclusion,nombre_paciente,edad_paciente,medico_solicitante,
        fecha,nombre_doc )
    nombre_fichero=str(nombre_paciente) + ' '+ str(tipo_estudio)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename={0}.docx'.format(nombre_fichero)
    document.save(response)
    return response


from . import filler
class DescargaTest(TestCase):

    def test_filler(self):
     
        paciente1= Paciente.Create(Cedula='1709262933',Nombre='Franklin',Apellido='Sanchez',Telefono=0987273842,
        	Fecha_nacimiento='02-02-1992')
        medico1= (Nombre='Marcos',Apellido='Arebalos',Telefono=094234218)
        plantilla1= Plantilla.Create(Campo='campo de plantilla',Conclusion='Conclusion plantilla', NombreDoc='test.docx')
        categoria1=Categoria.Create('Ultrasonidos')
        subcategoria1= Subcategoria.Create(categoria1,'Abdominal')
    	tipo_estudio1=TipoEstudio.Create(plantilla1,'Abdomen inferior simple',subcategoria1)
    	pedido1=Pedido.Create(paciente1,medico1,'diagnostico','28-08-2017','28-08-2017',False)
        historia1 = Historia.Create(pedido1,tipo_estudio1,'28-08-2017','campo nuevo','conclusion nueva')

        filler.reemplaza()
    
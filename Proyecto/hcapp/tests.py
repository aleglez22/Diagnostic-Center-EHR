from django.test import TestCase
from hcapp.models import  Paciente, Historia, Categoria, TipoEstudio, MedicoSolicitante, Pedido, Subcategoria, Plantilla
#from .models import Paciente
#from . import models
#from .views import FactoryHistoria
#from . import filler



class DescargaTest(TestCase):

    def test_filler(self):
     
        paciente1= Paciente.objects.create(Cedula='1709262933',Nombre='Franklin',Apellido='Sanchez',Telefono='0987273842',
        	Fecha_nacimiento='1992-02-02')
        medico1= MedicoSolicitante.objects.create(Nombre='Marcos',Apellido='Arebalos',Telefono='094234218')
        plantilla1= Plantilla.objects.create(Campo='campo de plantilla',Conclusion='Conclusion plantilla', NombreDoc='test.docx')
        categoria1=Categoria.objects.create(Nombre='Ultrasonidos')
        subcategoria1= Subcategoria.objects.create(Categoria=categoria1,Nombre='Abdominal')
        tipo_estudio1=TipoEstudio.objects.create(plantilla1,'Abdomen inferior simple',subcategoria1)
        pedido1=Pedido.objects.create(paciente1,medico1,'diagnostico','2017-08-28','2017-08-28',False)
        historia1 = Historia.objects.create(pedido1,tipo_estudio1,'2017-08-28','campo nuevo','conclusion nueva')
        
        documento= filler.reemplaza(historia1.Campo,historia1.Campo,historia1.Conclusion,pedido1.Paciente.Nombre,
            pedido1.Paciente.Fecha_nacimiento,pedido1.Medico.Nombre,historia1.Fecha_creacion,plantilla1.NombreDoc )
        documento.save('prueba.docx')

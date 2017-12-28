from django.test import TestCase
from hcapp.models import  Paciente, Historia, Categoria, TipoEstudio, MedicoSolicitante, Pedido, Subcategoria, Plantilla
#from .models import Paciente
#from . import models
#from .views import FactoryHistoria
from hcapp import filler



class DescargaTest(TestCase):

    def test_filler(self):
     
        paciente1= Paciente.objects.create(Cedula='1709262933',Nombre='Franklin',Apellido='Sanchez',Telefono='0987273842',
        	Fecha_nacimiento='1992-02-02')
        medico1= MedicoSolicitante.objects.create(Nombre='Marcos',Apellido='Arebalos',Telefono='094234218')
        plantilla1= Plantilla.objects.create(Campo='campo de plantilla',Conclusion='Conclusion plantilla', NombreDoc='test.docx')
        categoria1=Categoria.objects.create(Nombre='Ultrasonidos')
        subcategoria1= Subcategoria.objects.create(Categoria=categoria1,Nombre='Abdominal')
        tipo_estudio1=TipoEstudio.objects.create(Plantilla=plantilla1,Nombre='Abdomen inferior simple',Subcategoria=subcategoria1)
        pedido1=Pedido.objects.create(Paciente=paciente1,Medico=medico1,Diagnostico_presuntivo='diagnostico',Fecha_pedido='2017-08-28',Fecha='2017-08-28',Cortecia=False)
        historia1 = Historia.objects.create(Pedido=pedido1,TipoEstudio=tipo_estudio1,Fecha_creacion='2017-08-28',Campo='campo nuevo',Conclusion='conclusion nueva')
        documento= filler.reemplaza(historia1.Campo,historia1.Campo,historia1.Conclusion,pedido1.Paciente.Nombre,
            pedido1.Paciente.Fecha_nacimiento,pedido1.Medico.Nombre,historia1.Fecha_creacion,plantilla1.NombreDoc )
        documento.save('prueba.docx')

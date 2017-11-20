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

class DescargaTest(TestCase):
    def test_descarga(self):
        response = v.DescargarDoc(request, 1)
        self.assertEqual(response.status_code, 200) 
    
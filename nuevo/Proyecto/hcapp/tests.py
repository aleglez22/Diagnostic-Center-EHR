from django.test import TestCase
from .models import Paciente
from . import models
from .views import FactoryHistoria

# Create your tests here.

#
class FactoryHistoriaTest(TestCase):
    def test_return_requested_model(self):
        print("nombre: "+ str(Paciente.__name__))
        nombre_modelo=Paciente.__name__
        objeto=FactoryHistoria.getTipo(self, str(nombre_modelo))
        print ("modelo devuelto: "+ str(objeto.__name__))

        self.assertEqual(Paciente, FactoryHistoria.getTipo(self, Paciente.__name__))

class ModelsTest(TestCase):
    def OnetoOneTest(self):
        estudio1= models.Estudio.objects.create()
        cerebro1=models.CerebroSimple.objects.create(Estudio=estudio1,Campo= "Estructuras del cerebelo, tallo ",Conclusion=" todo esta bien")
        print (estudio1.Cerebrosimple.objects.all())
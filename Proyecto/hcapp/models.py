from django.db import models

# Create your models here.
class Paciente (models.Model):
    Cedula = models.IntegerField(null=False, blank=False, unique=True) # es necesaria?
    Nombre = models.CharField(max_length=128, null=False, blank=False)
    Apellido = models.CharField(max_length=128, null=False, blank=False)
    Telefono = models.IntegerField(max_length=10, null=True, blank=True)
    Edad= models.IntegerField(max_length=3, null=True, blank=True)
    Fecha_nacimiento= models.DateField(null= True, blank=True)
    Fecha_ingreso= models.DateField(auto_now=True, auto_now_add=False)


class MedicoSolicitante (models.Model):
    Nombre = models.CharField(max_length=128, null=False, blank=False)
    Apellido = models.CharField(max_length=128, null=False, blank=False)
    Telefono = models.IntegerField(max_length=10, null=True, blank=True)

class Radiologo (models.Model):
    Nombre = models.CharField(max_length=128, null=False, blank=False)
    Apellido = models.CharField(max_length=128, null=False, blank=False)
    Telefono = models.IntegerField(max_length=10, null=True, blank=True)

class Pedido(models.Model):
    Paciente= models.ForeignKey(Paciente, on_delete=models.DO_NOTHING)
    Medico= models.ForeignKey(MedicoSolicitante, on_delete=models.DO_NOTHING)
    Diagnostico_presuntivo= models.CharField(max_length=255, null=True, blank=True)
    Fecha = models.DateField(auto_now=True) # auto_add será valido ???

class Categoria(models.Model):
    Nombre = models.CharField(max_length=255, null=True, blank=True)
#   Descripcion

class Subcategoria(models.Model):
    Categoria= models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    Nombre = models.CharField(max_length=255, null=True, blank=True)
#   Descripcion

class Estudio(models.Model):
    Subcategoria= models.CharField(max_length=255, null=True, blank=True)
    Fecha = models.DateField(auto_now=True)



class CerebroSimple(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class CerebroSimpleContrastado(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class CerebroSimpleVentanaOsea(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class Hipofisis(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class HipofisisContrastada(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class MacizoFacialHuesosNasales(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class MacizoFacialReconstruido3d(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class MaxilarSuperiorInferior(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class MaxilarSupInfReconstruido(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class Oido(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class OidoConstrastado(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class OidoReconstruido3d(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class OrbitasSimple(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class OrbitasContrastado(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class SenosParanasalesSimple(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class SenosParanasalesReconstruido3d(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class GlandulasSalivales(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)

class CerebroSimple(models.Model):
    Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)






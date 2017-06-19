from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class Paciente (models.Model):
    Cedula = models.IntegerField(null=False, blank=False, unique=True) # es necesaria?
    Nombre = models.CharField(max_length=128, null=False, blank=False)
    Apellido = models.CharField(max_length=128, null=False, blank=False)
    Telefono = models.IntegerField(validators=[MaxValueValidator(9999999999)], null=True, blank=True)
    Edad= models.IntegerField(validators=[MaxValueValidator(200)], null=True, blank=True)
    Fecha_nacimiento= models.DateField(null= True, blank=True)
    Fecha_ingreso= models.DateField(auto_now=True, auto_now_add=False)


class MedicoSolicitante (models.Model):
    Nombre = models.CharField(max_length=128, null=False, blank=False)
    Apellido = models.CharField(max_length=128, null=False, blank=False)
    Telefono = models.IntegerField(validators=[MaxValueValidator(9999999999)], null=True, blank=True)

class Radiologo (models.Model):
    Nombre = models.CharField(max_length=128, null=False, blank=False)
    Apellido = models.CharField(max_length=128, null=False, blank=False)
    Telefono = models.IntegerField( validators=[MaxValueValidator(9999999999)],null=True, blank=True)

class Medico (models.Model):
    Nombre = models.CharField(max_length=128, null=False, blank=False)
    Apellido = models.CharField(max_length=128, null=False, blank=False)
    Telefono = models.IntegerField( validators=[MaxValueValidator(9999999999)],null=True, blank=True)
    Fecha_creacion = models.DateField(auto_now=True)

class Secretario (models.Model):
    Nombre = models.CharField(max_length=128, null=False, blank=False)
    Apellido = models.CharField(max_length=128, null=False, blank=False)
    Telefono = models.IntegerField( validators=[MaxValueValidator(9999999999)],null=True, blank=True)
    Fecha_creacion = models.DateField(auto_now=True)


class Historia(models.Model):
    TipoEstudio= models.CharField(max_length=200)
    Fecha_creacion = models.DateField(auto_now=True)
    Campo = models.TextField()
    Conclusion = models.TextField()  # charfield

class Plantilla(models.Model):
    TipoEstudio = models.CharField(max_length=200)
    Fecha_creacion = models.DateField(auto_now=True)
    Campo = models.TextField()
    Conclusion = models.TextField()

class Pedido(models.Model):
    Paciente= models.ForeignKey(Paciente, on_delete=models.DO_NOTHING)
    Medico= models.ForeignKey(MedicoSolicitante, on_delete=models.DO_NOTHING)
    Diagnostico_presuntivo= models.CharField(max_length=255, null=True, blank=True)
    Fecha_pedido = models.DateField(auto_now=True) # auto_add será valido ???
    Historia=models.ForeignKey(Historia, on_delete=models.DO_NOTHING)
    Fecha = models.DateField(auto_now=True)


class Categoria(models.Model):
    Nombre = models.CharField(max_length=255, null=True, blank=True)
#   Descripcion

class Subcategoria(models.Model):
    Categoria= models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    Nombre = models.CharField(max_length=255, null=True, blank=True)
#   Descripcion

class Subcategoria(models.Model):
    Categoria= models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    Nombre = models.CharField(max_length=255, null=True, blank=True)

class TipoEstudio(models.Model):
    Nombre = models.CharField(max_length=255, null=True, blank=True)
    Subcategoria= models.CharField(max_length=255, null=True, blank=True)
    Fecha_creacion = models.DateField(auto_now=True)




##### CABEZA ######

#

#
# class CerebroSimpleContrastado(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class CerebroSimpleVentanaOsea(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class Hipofisis(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class HipofisisContrastada(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class MacizoFacialHuesosNasales(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class MacizoFacialReconstruido3d(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class MaxilarSuperiorInferior(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class MaxilarSupInfReconstruido(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class Oido(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class OidoConstrastado(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class OidoReconstruido3d(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class OrbitasSimple(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class OrbitasContrastado(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class SenosParanasalesSimple(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class SenosParanasalesReconstruido3d(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class GlandulasSalivales(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class CerebroSimple(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
#
# ##### ABDOMEN ######
#
#
# class AbdomenSupInfSimple(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class AbdomenSupInfContrastado(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class AbdomenTotalSimple(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class AbdomenTotalSimpleContrastado(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class Pelvis(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
#
# ##### ESPECIALES ######
#
#
# class Urotac(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
#
# class Pielotac(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
#
# ##### Extremidades ######
#
#
# class Articulaciones(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
#
# class ArticulacionesReconstruccion3d(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
#
# class Escanograma(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
#
# ##### CUELLO ######
#
#
# class CuelloSimple(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
#
# class CuelloContrastado(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
#
# ##### TORAX ######
#
#
# class ToraxSimple(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
#
# class ToraxContrastado(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class ToraxAltaResolucion(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
#
# ##### COLUMNA ######
#
#
# class ColumnaCervical(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class ColumnaCervicalReconstruida3d(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class ColumnaDorsal(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class ColumnaDorsalReconstruida3d(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class ColumnaLumbo(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class ColumnaLumboReconstruida3d(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class ColumnaTotal(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)
#
# class ColumnaTotalReconstruida3d(models.Model):
#     Estudio = models.OneToOneField(Estudio, on_delete=models.DO_NOTHING)


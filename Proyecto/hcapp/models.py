from django.db import models
from django.core.validators import MaxValueValidator
from django.core.urlresolvers import reverse

## Cuando se elimina un campo con relaciones 
## poner default=1 

# Create your models here.
from datetime import date

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class Paciente (models.Model):
    Cedula = models.IntegerField(null=False, blank=False, unique=True) # es necesaria?
    Nombre = models.CharField(max_length=128, null=False, blank=False)
    Apellido = models.CharField(max_length=128, null=False, blank=False)
    Telefono = models.IntegerField(validators=[MaxValueValidator(9999999999)], null=True, blank=True)
    Fecha_nacimiento= models.DateField(null= True, blank=True)
    Fecha_ingreso= models.DateField(auto_now=True, auto_now_add=False)
    #Edad= models.IntegerField(null=True, blank=True) #>>>>automatizar calculo

    '''def save(self, *args, **kwargs):
        if not self.Edad:
            self.Edad = calculate_age(self.Fecha_nacimiento)
        super(Paciente, self).save(*args, **kwargs)'''

    def get_absolute_url(self):
        return reverse('hcapp:Crear-Paciente')

    def __str__(self):
        return ("pcte: "+str(self.Cedula)+" "+str(self.Nombre)+" "+str(self.Apellido))


class MedicoSolicitante (models.Model):
    Nombre = models.CharField(max_length=128, null=False, blank=False)
    Apellido = models.CharField(max_length=128, null=False, blank=False)
    Telefono = models.IntegerField(validators=[MaxValueValidator(9999999999)], null=True, blank=True)
    def __str__(self):
        return ("med_sol: "+str(self.Nombre)+" "+str(self.Apellido))


class Radiologo (models.Model):
    Nombre = models.CharField(max_length=128, null=False, blank=False)
    Apellido = models.CharField(max_length=128, null=False, blank=False)
    Telefono = models.IntegerField( validators=[MaxValueValidator(9999999999)],null=True, blank=True)
    def __str__(self):
            return ("radiol: "+str(self.Nombre)+" "+str(self.Apellido))

class Medico (models.Model):
    Nombre = models.CharField(max_length=128, null=False, blank=False)
    Apellido = models.CharField(max_length=128, null=False, blank=False)
    Telefono = models.IntegerField( validators=[MaxValueValidator(9999999999)],null=True, blank=True)
    Fecha_creacion = models.DateField(auto_now=True)

    def __str__(self):
        return ("medic: "+str(self.Nombre)+" "+str(self.Apellido))

class Secretario (models.Model):
    Nombre = models.CharField(max_length=128, null=False, blank=False)
    Apellido = models.CharField(max_length=128, null=False, blank=False)
    Telefono = models.IntegerField( validators=[MaxValueValidator(9999999999)],null=True, blank=True)
    Fecha_creacion = models.DateField(auto_now=True)

    def __str__(self):
        return ("secret: "+str(self.Nombre)+" "+str(self.Apellido))



class Plantilla(models.Model):
    TipoEstudio = models.CharField(max_length=200) #>>>>unique
    Fecha_creacion = models.DateField(auto_now=True)
    Campo = models.TextField()
    Conclusion = models.TextField()
    NombreDoc= models.CharField(max_length=200)

    def __str__(self):
        return ("Plantilla: "+str(self.TipoEstudio))


class Pedido(models.Model):
    TRUE_FALSE_CHOICE = ((True, "Yes"),(False, "No"))
    Paciente= models.ForeignKey(Paciente, on_delete=models.PROTECT)
    Medico= models.ForeignKey(MedicoSolicitante, on_delete=models.PROTECT)
    Diagnostico_presuntivo= models.CharField(max_length=255, null=True, blank=True)
    Fecha_pedido = models.DateField(auto_now=True) # auto_add será valido ???
    Fecha = models.DateField(auto_now=True)
    Cortecia = models.BooleanField(choices=TRUE_FALSE_CHOICE)


    def __str__(self):
        return ("pedido: "+str(self.Paciente)+" "+str(self.Diagnostico_presuntivo))

class Historia(models.Model):
    p1=Pedido(Paciente=Paciente.objects.get(Cedula=111),Medico=MedicoSolicitante.objects.get(pk=1),Diagnostico_presuntivo="nada")
    Pedido=models.ForeignKey(Pedido, on_delete=models.PROTECT, default= 1)
    TipoEstudio= models.CharField(max_length=200)
    Fecha_creacion = models.DateField(auto_now=True)
    Campo = models.TextField()
    Conclusion = models.TextField()  # charfield

    def __str__(self):
        return ("hist: "+str(self.TipoEstudio))


class Categoria(models.Model):
    Nombre = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return ("cat: "+str(self.Nombre))


class Subcategoria(models.Model):
    Categoria= models.ForeignKey(Categoria, on_delete=models.PROTECT)
    Nombre = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return ("sub: "+str(self.Nombre))


class TipoEstudio(models.Model):
    Nombre = models.CharField(max_length=255, null=True, blank=True)
    Subcategoria= models.ForeignKey(Subcategoria, on_delete=models.PROTECT)
    Fecha_creacion = models.DateField(auto_now=True)

    def __str__(self):
        return ("est: "+str(self.Nombre))



class Placa(models.Model):
    tipos=(('AGFA','8 X 10'), ('AGFA','10 X 14'),('AGFA','14 X 17'), ('FUJI','8 X 10'),
    ('FUJI','10 X 14'),('FUJI','14 X 17'))
    Tipo = models.CharField(max_length=255, null=True, blank=True, choices=tipos)
    Fecha= models.DateField(auto_now=True)

    def __str__(self):
        return ("placa: "+str(self.Tipo))


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


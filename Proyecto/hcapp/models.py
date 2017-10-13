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
    Cedula = models.IntegerField(null=False, blank=False, unique=True, error_messages={'unique':"Ya existe un paciente con esta cédula en el sistema"}) # es necesaria?
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
    Fecha = models.DateField(auto_now=True)
    def __str__(self):
        return ("med_sol: "+str(self.Nombre)+" "+str(self.Apellido))



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
    Pedido=models.ForeignKey(Pedido, on_delete=models.PROTECT, default= 1)
    TipoEstudio= models.CharField(max_length=200)
    Fecha_creacion = models.DateField(auto_now=True)
    Campo = models.TextField()
    Conclusion = models.CharField(max_length=200)  # charfield

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

class Plantilla(models.Model):
    TipoEstudio = models.ForeignKey(TipoEstudio, on_delete=models.PROTECT)
    Fecha_creacion = models.DateField(auto_now=True)
    Campo = models.TextField()
    Conclusion = models.CharField(max_length=200)
    NombreDoc= models.CharField(max_length=200)

    def __str__(self):
        return ("Plantilla: "+str(self.TipoEstudio))

class Placa(models.Model):
    tipos=(('AGFA 8 X 10','AGFA 8 X 10'), ('AGFA 10 X 14','AGFA 10 X 14'),('AGFA 14 X 17','AGFA 14 X 17'), ('FUJI 8 X 10',' FUJI 8 X 10'),
    ('FUJI 10 X 14','FUJI 10 X 14'),('FUJI 14 X 17','FUJI 14 X 17'))
    Tipo = models.CharField(max_length=255, null=True, blank=True, choices=tipos)
    Fecha= models.DateField(auto_now=True)

    def __str__(self):
        return ("placa: "+str(self.Tipo))



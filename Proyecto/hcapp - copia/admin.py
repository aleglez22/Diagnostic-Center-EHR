from django.contrib import admin
from .models import Paciente, Categoria, TipoEstudio, MedicoSolicitante, Pedido, Radiologo, Subcategoria
from. import models

admin.site.register(Paciente)
admin.site.register(models.Pedido)
admin.site.register(models.Categoria)
admin.site.register(models.Subcategoria)
admin.site.register(models.TipoEstudio)

admin.site.register(models.Historia)
admin.site.register(models.Plantilla)
admin.site.register(models.MedicoSolicitante)


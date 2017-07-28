from django.contrib import admin
from .models import Paciente, Categoria, TipoEstudio, MedicoSolicitante, Pedido, Radiologo, Subcategoria
from. import models

admin.site.register(models.Categoria)
admin.site.register(models.Subcategoria)
admin.site.register(models.TipoEstudio)


admin.site.register(models.Plantilla)
admin.site.register(models.MedicoSolicitante)

class DeleteNotAllowedModelAdmin(admin.ModelAdmin):
    # Other stuff here
    #admin.site.register(models.Historia)

    def get_actions(self, request):
        #Disable delete
        actions = super(DeleteNotAllowedModelAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    #solo readonly los campos
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + self.campos_readonly
        return self.readonly_fields


class PedidoModelAdmin(DeleteNotAllowedModelAdmin):
	campos_readonly=('Paciente', 'Medico','Diagnostico_presuntivo' )

class HistoriaModelAdmin(DeleteNotAllowedModelAdmin):
	campos_readonly=('Pedido','TipoEstudio','Fecha_creacion')

class PacienteModelAdmin(DeleteNotAllowedModelAdmin):
	campos_readonly=('Cedula','Nombre','Apellido','Fecha_nacimiento','Fecha_ingreso')



admin.site.register(models.Historia, HistoriaModelAdmin)
admin.site.register(models.Paciente, PacienteModelAdmin)
admin.site.register(models.Pedido, PedidoModelAdmin)
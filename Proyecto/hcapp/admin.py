from django.contrib import admin
from .models import Paciente, Categoria, TipoEstudio, MedicoSolicitante, Pedido, Subcategoria
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
    list_display = ('id','Paciente', 'Medico', 'Diagnostico_presuntivo','Fecha','Cortecia',)#campos a mostrar
    list_filter = ('Fecha','Medico',)# filtros(tags)
    ordering = ('-Fecha',)
    search_fields = ('id',)

    #buscar por paciente 

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(PedidoModelAdmin, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            paciente=models.Paciente.objects.get(Cedula=search_term_as_int)
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(Paciente=paciente)
        return queryset, use_distinct

class PlacaModelAdmin(DeleteNotAllowedModelAdmin):
    campos_readonly=('Tipo','Fecha')
    def has_delete_permission(self, request, obj=None):
        return True
    

class HistoriaModelAdmin(DeleteNotAllowedModelAdmin):
    campos_readonly=('Pedido','TipoEstudio','Fecha_creacion')
    list_display = ('Pedido', 'TipoEstudio', 'Fecha_creacion')#campos a mostrar
    list_filter = ('TipoEstudio','Fecha_creacion',)# filtros(tags)
    ordering = ('-Fecha_creacion',)


class PacienteModelAdmin(DeleteNotAllowedModelAdmin):
    campos_readonly=('Cedula','Fecha_ingreso')
    list_display = ('Nombre', 'Apellido', 'Fecha_ingreso')#campos a mostrar
    list_filter = ('Fecha_ingreso',)# filtros(tags)
    ordering = ('-Fecha_ingreso',)
    search_fields = ('Cedula',)




admin.site.register(models.Historia, HistoriaModelAdmin)
admin.site.register(models.Paciente, PacienteModelAdmin)
admin.site.register(models.Pedido, PedidoModelAdmin)
admin.site.register(models.Placa, PlacaModelAdmin)
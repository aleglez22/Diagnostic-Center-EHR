from django.conf.urls import include, url
from django.contrib import admin
from . import  views

app_name ='hcapp'

urlpatterns = [
url(r'^home/$',views.Inicio ,name="Inicio"),

#url(r'^imprimir/(?P<historia_id>[0-9]+)/(?P<nombre_estudio>[\w\-]+)/$',views.DescargarDoc,name="Descargar"),
url(r'^imprimir/(?P<historia_id>[0-9]+)/$',views.DescargarDoc,name="Descargar"),


    ###PACIENTES###
url(r'^pacientes/$',views.PacienteHome,name="Home-Paciente"),
url(r'^prueba/$',views.Pruebaselect,name="prueba"),

url(r'^GetSubcategoria/(?P<categoria_id>[0-9]+)/$',views.GetSubcategoria,name="prueba"),
url(r'^GetEstudio/(?P<subcategoria_id>[0-9]+)/$',views.GetEstudio,name="estudio"),


url(r'^crear/paciente/$',views.CrearPaciente.as_view() ,name="Crear-Paciente"),
url(r'^pacientes/$',views.TablaPacientes ,name="Tabla-Pacientes"),
url(r'^editar/paciente/(?P<pk>[0-9]+)/$',views.EditarPaciente.as_view() ,name="Editar-Pacientes"),
url(r'^eliminar/paciente/(?P<pk>[0-9]+)$',views.EliminarPaciente.as_view() ,name="Eliminar-Pacientes"),


    ###HISTORIAS###
url(r'^crear/historia/$',views.GuardarHistoria ,name="Crear-Historia"),
url(r'^crear/otrahistoria/$',views.GuardarOtraHistoria ,name="Crear-Otra-Historia"),
url(r'^crear/selecciona-estudio/$',views.CasoErrorNestudio ,name="Selecciona-Estudio"),
url(r'^historia/(?P<pk>[0-9]+)/$',views.DetalleHistoria.as_view() ,name="Detalle-Historia"),
url(r'^historias/$', views.Historias, name= "Tabla-Historias"),

#url(r'^editar/historia/(?P<pk>[0-9]+)/$',views.EditarHistoria.as_view() ,name="Editar-Historia"),
#url(r'^eliminar/historia/(?P<pk>[0-9]+)$',views.EliminarHistoria.as_view() ,name="Eliminar-Pacientes"),
# pedido tiene varias historias, cada historia tiene su estudio

    ###PEDIDOS###
url(r'^pedidos/$',views.PedidosHome ,name="Home-Pedidos"),
url(r'^lista-pedidos/$',views.ListaPedidos.as_view() ,name="Lista-Pedidos"),
url(r'^pedido/(?P<pk>[0-9]+)/$',views.DetallePedido.as_view() ,name="Detalle-Pedido"),
url(r'^crear/pedido/$',views.CrearPedido1 ,name="Crear-Pedidos"),


	###REPORTES###
url(r'^registrar-placas/$',views.RegistrarPlaca ,name="Registrar-Placa"),
url(r'^reportes/$',views.ReportesHome ,name="Home-Reportes"),
url(r'^reportes/reporte-cortecias/$',views.ReporteCortecias ,name="Reporte-Cortecia"),
url(r'^reportes/reporte-pacientes/$',views.ReportePacientes ,name="Reporte-Paciente"),
url(r'^reportes/reporte-estudios/$',views.ReporteEstudios ,name="Reporte-Estudios"),
url(r'^reportes/reporte-medicos/$',views.ReporteMedicos ,name="Reporte-Medicos"),



    ### REST API JSON ###
url(r'^api/medico-solicitante/$', views.AutocompletarMedicoSolicitante, name= "Api-MedicoSolicitante"),
url(r'^api/tipo-estudio/$', views.AutocompletarTipoEstudio, name= "Api-Estudio"),
url(r'^api/paciente/$', views.AutocompletarPaciente, name= "Api-Paciente"),
url(r'^api/historias/$', views.TablaHistorias, name= "Api-Historias"),
url(r'^api/pacientes/$', views.TablaPacientes, name= "Api-Pacientes"),
#url(r'^reportes/$', views.PruebaTabla, name= "Reportes"),
]


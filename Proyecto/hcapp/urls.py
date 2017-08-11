from django.conf.urls import include, url
from django.contrib import admin
from . import  views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test



app_name ='hcapp'

urlpatterns = [
url(r'^$',views.Inicio ,name="Inicio"),

	###ACCESSO###
#url(r'^accounts/', include('django.contrib.auth.urls')),#incluye todas las urls de la aplicacion auth
url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='Login'),
url(r'^logout/$', auth_views.logout, {'next_page': 'hcapp:Inicio'}, name='Logout'),


	###INPUTS###
url(r'^subirplantilla/$',views.UploadPlantilla,name="Subir-Plantilla"),


	###OUTPUTS###
url(r'^imprimir/(?P<historia_id>[0-9]+)/$',views.DescargarDoc,name="Descargar"),


    ###PACIENTES###
url(r'^crear/paciente/$',login_required(views.CrearPaciente.as_view()) ,name="Crear-Paciente"),
url(r'^pacientes/$', TemplateView.as_view(template_name="hcapp/pacientes.html") ,name="Tabla-Pacientes"),
url(r'^editar/paciente/(?P<pk>[0-9]+)/$',views.EditarPaciente.as_view() ,name="Editar-Pacientes"),
url(r'^eliminar/paciente/(?P<pk>[0-9]+)$',views.EliminarPaciente.as_view() ,name="Eliminar-Pacientes"),


    ###HISTORIAS###
url(r'^crear/historia/$',views.GuardarHistoria ,name="Crear-Historia"),
url(r'^crear/otrahistoria/$',views.GuardarOtraHistoria ,name="Crear-Otra-Historia"),
url(r'^crear/selecciona-estudio/$',views.CasoErrorNestudio ,name="Selecciona-Estudio"),
url(r'^historia/(?P<pk>[0-9]+)/$',views.DetalleHistoria.as_view() ,name="Detalle-Historia"),
url(r'^historias/$', views.Historias, name= "Tabla-Historias"),
url(r'^editar/historia/(?P<pk>[0-9]+)/$',views.EditarHistoria.as_view() ,name="Editar-Historia"),
#url(r'^eliminar/historia/(?P<pk>[0-9]+)$',views.EliminarHistoria.as_view() ,name="Eliminar-Pacientes"),


    ###PEDIDOS###
url(r'^pedidos/$',user_passes_test(views.superuser_or_medico)(views.PedidosHome) ,name="Home-Pedidos"),
url(r'^lista-pedidos/$',views.ListaPedidos.as_view() ,name="Lista-Pedidos"),
url(r'^pedido/(?P<pk>[0-9]+)/$',views.DetallePedido.as_view() ,name="Detalle-Pedido"),
url(r'^crear/pedido/$',views.CrearPedido1 ,name="Crear-Pedidos"),


	###REPORTES###
url(r'^registrar-placas/$',views.RegistrarPlaca.as_view() ,name="Registrar-Placa"),
url(r'^reportes/$',views.ReportesHome ,name="Home-Reportes"),
url(r'^reportes/reporte-cortecias/$',views.ReporteCortecias ,name="Reporte-Cortecia"),
url(r'^reportes/reporte-pacientes/$',views.ReportePacientes.as_view() ,name="Reporte-Pacientes"),
url(r'^reportes/reporte-estudios/$',views.ReporteEstudios.as_view() ,name="Reporte-Estudios"),
url(r'^reportes/reporte-medicos/$',views.ReporteMedicos.as_view() ,name="Reporte-Medicos"),
url(r'^reportes/reporte-placas/$',views.ReportePlacas.as_view() ,name="Reporte-Placas"),


    ### REST API JSON ###
url(r'^GetSubcategoria/(?P<categoria_id>[0-9]+)/$',views.GetSubcategoria,name="prueba"),
url(r'^GetEstudio/(?P<subcategoria_id>[0-9]+)/$',views.GetEstudio,name="estudio"),
url(r'^api/medico-solicitante/$', views.AutocompletarMedicoSolicitante, name= "Api-MedicoSolicitante"),
url(r'^api/tipo-estudio/$', views.AutocompletarTipoEstudio, name= "Api-Estudio"),
url(r'^api/paciente/$', views.AutocompletarPaciente, name= "Api-Paciente"),
url(r'^api/historias/$', views.TablaHistorias, name= "Api-Historias"),
url(r'^api/pacientes/$', views.TablaPacientes, name= "Api-Pacientes"),
#url(r'^reportes/$', views.PruebaTabla, name= "Reportes"),


    ###MEDICOS SOLICITANTES###
url(r'^crear/medico/$',login_required(views.CrearMedico.as_view()) ,name="Crear-Medico"),
url(r'^editar/medico/(?P<pk>[0-9]+)/$',login_required(views.EditarMedico.as_view()) ,name="Editar-Medico"),
]


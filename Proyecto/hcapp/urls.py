from django.conf.urls import include, url
from django.contrib import admin
from . import  views

app_name ='hcapp'

urlpatterns = [
url(r'^$',views.Inicio ,name="Inicio"),

]


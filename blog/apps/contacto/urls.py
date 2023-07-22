from django.urls import path
from . import views

urlpatterns = [
    path('formulario_contacto', views.formulario_contacto, name='formulario_contacto'),
    path('exito/', views.exito, name='exito'),
]
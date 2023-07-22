from django.urls import path
from .views import user_login, user_logout
#desde el archivo views ubicado en usuario, importame las dos vistas
from . import views
#llama a la clase Registro que esta en vista.py

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('registro/', views.Registro.as_view(), name='registro')#forma de llamar a una clase
        
] 
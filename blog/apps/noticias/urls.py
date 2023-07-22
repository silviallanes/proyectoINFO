from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'noticias'

urlpatterns = [
       
    #urls aplicaciones
    path('',views.ListarNoticias,name='listar'),
    path('listarNoticia/', views.mostrarNoticia.as_view()), #linkear la url  con clase    
    path('detalle/<int:pk>', views.DetalleNoticias, name='detalle'),
    path('addNoticia', views.add_noticia, name='addnoticia'),
    path('noticias/<int:pk>/edit/', views.EditNoticia, name='edit_noticia'),
    #url comentarios
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('comment/add/<int:noticia_id>/', views.add_comment, name='add_comment'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
]
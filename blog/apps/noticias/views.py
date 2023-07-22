from django.shortcuts import render, redirect, get_object_or_404
from .models import Noticia, Categoria, Comment
from django.views.generic.list import ListView #para las vistas clases
from django.contrib.auth.decorators import login_required #decoradores para el login
from .forms import NoticiaForm, CommentForm
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.
# vista con funciones
def ListarNoticias(request):
    noticias = Noticia.objects.all()

    # Filtrar por categoría
    categoria = request.GET.get('categoria')
    if categoria:
        noticias = noticias.filter(categoria_noticia=categoria)

    # Filtrar por antigüedad ascendente
    antiguedad_asc = request.GET.get('antiguedad_asc')
    if antiguedad_asc:
        noticias = noticias.order_by('fecha_de_publicacion')

    # Filtrar por antigüedad descendente
    antiguedad_desc = request.GET.get('antiguedad_desc')
    if antiguedad_desc:
        noticias = noticias.order_by('-fecha_de_publicacion')

    # Filtrar por orden alfabético ascendente
    orden_asc = request.GET.get('orden_asc')
    if orden_asc:
        noticias = noticias.order_by('titulo')

    # Filtrar por orden alfabético descendente
    orden_desc = request.GET.get('orden_desc')
    if orden_desc:
        noticias = noticias.order_by('-titulo')

    context = {
        'noticias': noticias,
        'categorias': Categoria.objects.all(),  # Asegúrate de tener el modelo 'Categoria' importado y definido
    }
    return render(request, 'noticias/listar.html', context)


#vista con clases
class mostrarNoticia(ListView):
    model = Noticia
    template_name = 'noticias/listarNoticia.html'

def DetalleNoticias(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    comments = noticia.comments.all()

    #BORRAR NOTICIA
    if request.method == 'POST' and 'delete_noticia' in request.POST:
        noticia.delete()
        return redirect('noticias:listar')

    # COMENTARIO
    if request.method == 'POST' and 'add_comment' in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.noticia = noticia
            comment.author = request.user
            comment.save()
            return redirect('noticias:detalle', pk=pk)
    else:
        form = CommentForm()

    context = {
        'noticia': noticia,
        'comments': comments,
        'form': form,
    }
    return render(request, 'noticias/detalle.html', context)

#borrar comentario
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user.username:
        comment.delete()
    return redirect('noticias:detalle', pk=comment.noticia.pk)

#Agregar comentario
#@login_required
def add_comment(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        author = request.user.username
        # creacion de comentario
        Comment.objects.create(noticia=noticia, author=author, text=text)

    return redirect('noticias:detalle', pk=noticia_id)

#agregar una noticia por formulario
def add_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES) ##REQUEST FILE PARA LAS IMAGENES
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.author = request.user #autor de la noticia
            noticia.save()
            return redirect('home')
    else:
        form = NoticiaForm()
    
    return render(request, 'noticias/addNoticia.html', {'form': form})
@login_required
def EditNoticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)

    # Solo el autor puede editar la noticia
    if noticia.author != request.user:
        return HttpResponseForbidden("No tenes permiso para editar esta noticia.")

    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('noticias:detalle', pk=pk)
    else:
        form = NoticiaForm(instance=noticia)

    context = {
        'form': form,
    }
    return render(request, 'noticias/editNoticia.html', context)

# EDITAR COMENTARIOS
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    #mensaje de error si no sos el autor
    if comment.author != request.user.username:
        messages.error(request, 'No tienes permisos para editar este comentario.')
        return redirect('noticias:detalle', pk=comment.noticia.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('noticias:detalle', pk=comment.noticia.pk)
    else:
        form = CommentForm(instance=comment)

    context = {
        'form': form,
        'comment': comment,
    }
    return render(request, 'noticias/edit_comment.html', context)

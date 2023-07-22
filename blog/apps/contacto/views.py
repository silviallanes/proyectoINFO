from django.shortcuts import render, redirect
from .forms import FormularioContacto

# Create your views here.

def formulario_contacto(request):
    if request.method == 'POST':
        form = FormularioContacto(request.POST)
        if form.is_valid():
            form.save()
            # Aquí puedes agregar el código para procesar el formulario, como enviar un correo electrónico, almacenar los datos en una base de datos, etc.
            # En este ejemplo, simplemente guardamos los datos ingresados por el usuario en la base de datos y redirigimos a una página de éxito.
            return redirect('exito')
    else:
        form = FormularioContacto()

    return render(request, 'contacto/formulario_contacto.html', {'form': form})

def exito(request):
    return render(request, 'contacto/exito.html')

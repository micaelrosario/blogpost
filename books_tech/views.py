from django.shortcuts import render
from .forms import PostForm
from .models import Post

def usuarioView (request):

    if request.method == 'GET':
        context = {
            'formulario': UsuarioForm()
        }
        return render(request, 'usuario.html', context)
    elif request.method == 'POST':
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            # Redirect or render success message as needed


def home_view(request):
    """Render only the home page. This app has been simplified to a single-page site."""
    return render(request, 'home.html')


def criar_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('books_tech:home_view')
    return render(request, 'post_form.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .forms import PostForm, EditForm, ClearableFileInput, LoginForm, CategoriaForm, PerfilAutorForm, ComentarioForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Categoria, PerfilAutor, Comentario
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages



class HomeView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    success_url = '/'  
    login_url = '/login/'

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'update_post.html'
    form_class = EditForm 
    success_url = '/'  
    login_url = '/login/'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.autor != self.request.user:
            return redirect(f"{obj.get_absolute_url()}?edit_error=1")

        return obj

    def dispatch(self, request, *args, **kwargs):
        result = self.get_object()

        if hasattr(result, 'status_code'): 
            return result

        self.object = result
        return super().dispatch(request, *args, **kwargs)


@login_required
def delete_post_direct(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.autor != request.user:
        return redirect(f"{post.get_absolute_url()}?delete_error=1")

    post.delete()
    return redirect('/')



#--------------------------------------------------------------------------

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm
    #redirect_authenticated_user = True

    def get_success_url(self):
        return '/'
    
#----------------------------------------------------------------------------------

class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'add_categoria.html'
    success_url = '/'  



#----------------------------------------------------------------------------------

class PerfilAutorCreateView(CreateView):
    model = PerfilAutor
    form_class = PerfilAutorForm
    template_name = 'perfil_autor_form.html'
    fields = ['bio', 'foto', 'redes_sociais']
    success_url = '/'  

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


#----------------------------------------------------------------------------------


class AddComentarioView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'post_detail.html'
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()

#----------------------------------------------------------------------------------
class ComentarioDeleteView(DeleteView):
    model = Comentario
    template_name = 'comentario_confirm_delete.html'
    success_url = reverse_lazy('books_tech:home')

    def get_object(self, queryset=None):
        comentario = super().get_object(queryset)
        if comentario.autor != self.request.user:
            raise PermissionDenied("Você não tem permissão para deletar este comentário.")
        return comentario

#----------------------------------------------------------------------------------

def logout_view(request):
    logout(request)
    return redirect('books_tech:login')
from django.shortcuts import render
from .models import Post, Usuario
from django.views.generic import ListView, DetailView, CreateView , UpdateView, DeleteView
from .forms import PostForm, EditForm, ClearableFileInput
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm
from django.urls import reverse_lazy
from .models import Categoria
from .forms import CategoriaForm

#def home_view(request):
#    return render(request, 'home.html')


class HomeView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    success_url = '/'  

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    form_class = EditForm 
    success_url = '/'  

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = '/'

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
    template_name = 'categoria_form.html'
    success_url = reverse_lazy('books_tech:categoria_list')

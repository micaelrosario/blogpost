from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView, CreateView , UpdateView, DeleteView


#def home_view(request):
#    return render(request, 'home.html')


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class PostCreateView(CreateView):
    model = Post
    template_name = 'add_post.html'
    fields = '__all__'
    success_url = '/'  

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    fields = '__all__'
    success_url = '/'  

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = '/'
from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView


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
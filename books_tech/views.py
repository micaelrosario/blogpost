from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Usuario, Post, Categoria
from django.views.generic import ListView, DetailView


def home(request):
    posts = Post.objects.all() 
    categories = Categoria.objects.all() if 'Categoria' in globals() else []
    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'home.html', context)



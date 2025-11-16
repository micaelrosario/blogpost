from urllib import request
from django.shortcuts import render, get_object_or_404
from .models import Usuario, Post, Categoria
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect


def home(request):
    posts = Post.objects.all()  # Post.Meta.ordering ensures newest first
    categories = Categoria.objects.all() if 'Categoria' in globals() else []
    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'home.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})


def category_posts(request, pk):
    category = get_object_or_404(Categoria, pk=pk)
    posts = Post.objects.filter(categoria__pk=pk) if hasattr(Post, 'categoria') else []
    return render(request, 'category_posts.html', {'category': category, 'posts': posts})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        user = authenticate(
            username=request.POST['username'], 
            password=request.POST['password'])
        if user:
            auth_login(request, user=user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('login'))


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))
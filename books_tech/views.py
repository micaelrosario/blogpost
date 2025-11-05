from urllib import request
from django.shortcuts import render
from .models import Usuario
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect

def home(request):
    context = {
        'usuario': Usuario.objects.all()
    }
    return render(request, 'home.html', context)

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
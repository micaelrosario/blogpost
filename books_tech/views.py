from django.shortcuts import render
from .models import Usuario
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect

def home(request):
    context = {
        'user': Usuario.objects.all()
    }
    return render(request, 'home.html', context)

def login(request):
    return render(request, 'login.html')

def fazerLogin(request):
    user = authenticate(
        username=request.POST['username'], 
        password=request.POST['password'])
    if user:
        auth_login(request, user=user)
    return HttpResponseRedirect(reverse('home'))

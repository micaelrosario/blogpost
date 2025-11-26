from django.shortcuts import render


def home(request):
    """Backup of previous views.py"""
    return render(request, 'home.html')

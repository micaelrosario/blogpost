from django.urls import path
from . import views


app_name = 'books_tech'

urlpatterns = [
    path('', views.home, name='home'),
]
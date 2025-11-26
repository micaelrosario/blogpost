from django.urls import path
from . import views

app_name = 'books_tech'

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('novo_post', views.criar_post, name='criar_post'),
]
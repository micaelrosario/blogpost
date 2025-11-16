from django.urls import path
from . import views


app_name = 'books_tech'

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('category/<int:pk>/', views.category_posts, name='category_posts'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
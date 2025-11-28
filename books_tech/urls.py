from django.urls import path
from .views import HomeView, PostDetailView

app_name = 'books_tech'

urlpatterns = [
    #path('', views.home_view, name='home_view'),
    path('', HomeView.as_view(), name='home_view'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]
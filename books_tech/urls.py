from django.urls import path
from .views import HomeView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name = 'books_tech'

urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('add_post/', PostCreateView.as_view(), name='add_post'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
]
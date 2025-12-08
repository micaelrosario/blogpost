from django.urls import path
from .views import HomeView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CustomLoginView, CategoriaCreateView, PerfilAutorCreateView, UsuarioUpdateView, ComentarioCreateView, ComentarioDeleteView

app_name = 'books_tech'

urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/', PostCreateView.as_view(), name='add_post'),
    path('categoria/', CategoriaCreateView.as_view(), name='add_categoria'),
    path('post/edit/<int:pk>/', PostUpdateView.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('accounts/profile/', CustomLoginView.as_view(), name='login'),
]
from django.urls import path
from .views import HomeView, PostDetailView, PostCreateView, PostUpdateView, CustomLoginView, CategoriaCreateView, PerfilAutorCreateView, UsuarioUpdateView, ComentarioCreateView, ComentarioDeleteView, delete_post_direct

app_name = 'books_tech'

urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/', PostCreateView.as_view(), name='add_post'),
    path('categoria/', CategoriaCreateView.as_view(), name='add_categoria'),
    path('post/edit/<int:pk>/', PostUpdateView.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', delete_post_direct, name='delete_post'),
    path('perfil_autor/add/', PerfilAutorCreateView.as_view(), name='add_perfil_autor'),
    path('usuario/edit/', UsuarioUpdateView.as_view(), name='edit_usuario'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('accounts/profile/', CustomLoginView.as_view(), name='login'),
]
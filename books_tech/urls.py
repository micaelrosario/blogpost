from django.urls import path
from .views import HomeView, PostDetailView, PostCreateView, PostUpdateView, CustomLoginView, CategoriaCreateView, PerfilAutorCreateView, AddComentarioView, ComentarioDeleteView, delete_post_direct

app_name = 'books_tech'

urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/', PostCreateView.as_view(), name='add_post'),
    path('categoria/', CategoriaCreateView.as_view(), name='add_categoria'),
    path('post/edit/<int:pk>/', PostUpdateView.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', delete_post_direct, name='delete_post'),
    path('perfil_autor/', PerfilAutorCreateView.as_view(), name='perfil_autor'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('post/<int:post_id>/comentario/', AddComentarioView.as_view(), name='add_comentario'),
]
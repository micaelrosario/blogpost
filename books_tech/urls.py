from django.urls import path
from .views import HomeView, PostDetailView, PostCreateView, PostUpdateView, CustomLoginView, CategoriaCreateView, AddComentarioView, ComentarioDeleteView, ComentarioUpdateView, delete_post_direct, PerfilAutorProfile, CategoryView, logout_view, update_categoria, delete_categoria, perfil_autor_redirect, admin_panel, editarusuario

app_name = 'books_tech'

urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/', PostCreateView.as_view(), name='add_post'),
    path('categoria/', CategoriaCreateView.as_view(), name='add_categoria'),
    path('categoria/<int:pk>/edit/', update_categoria, name='update_categoria'),
    path('categoria/<int:pk>/delete/', delete_categoria, name='delete_categoria'),
    path('post/<int:pk>/edit', PostUpdateView.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', delete_post_direct, name='delete_post'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('post/<int:post_id>/comentario/', AddComentarioView.as_view(), name='add_comentario'),
    path('comentario/<int:pk>/edit/', ComentarioUpdateView.as_view(), name='update_comentario'),
    path('comentario/<int:pk>/delete/', ComentarioDeleteView.as_view(), name='delete_comentario'),
    path('perfil_autor/', perfil_autor_redirect, name='perfil_autor'),
    path("meu_perfil/", PerfilAutorProfile.as_view(), name="author_detail"),
    path('categoria/<str:category_name>/', CategoryView, name='categoria_posts'),
    path('painel/', admin_panel, name='admin_panel'),
    path('editarusuario/id/<int:id>/', editarusuario, name='editar_usuario'),
    #path('excluirusuario/id/<int:pk>/', excluirusuario, name='excluir_usuario'),

]
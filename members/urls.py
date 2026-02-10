from django.urls import path
from .views import UserRegisterView, UserEditView
from books_tech.views import PerfilAutorCreateView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('perfil_autor/', PerfilAutorCreateView.as_view(), name='perfil_autor'),

]
from django.urls import path
from .views import UserRegisterView, UserEditView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    # Mantido por compatibilidade (agora tudo é editado em edit_profile)
    path('perfil_autor/', UserEditView.as_view(), name='perfil_autor'),

]
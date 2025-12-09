from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from .forms import UserUpdateForm


class UserRegisterView(generic.CreateView):
    """View para registrar novos usuários."""
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserEditView(generic.UpdateView):
    """View para editar o perfil do usuário."""
    form_class = UserUpdateForm
    template_name = 'registration/edit_profile.html'
    success_url = '/' 

    def get_object(self):
        """Retorna o usuário atual."""
        return self.request.user
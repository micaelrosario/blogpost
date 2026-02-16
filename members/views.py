from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views import View

from books_tech.forms import PerfilAutorForm
from books_tech.models import PerfilAutor
from .forms import UserUpdateForm


class UserRegisterView(generic.CreateView):
    """View para registrar novos usuários."""
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserEditView(LoginRequiredMixin, View):
    """Edição unificada: dados do usuário + perfil do autor."""

    template_name = 'registration/edit_profile.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        perfil_autor = PerfilAutor.objects.filter(usuario=request.user).first()

        user_form = UserUpdateForm(instance=request.user)
        autor_form = PerfilAutorForm(instance=perfil_autor)

        return render(request, self.template_name, {
            'user_form': user_form,
            'autor_form': autor_form,
        })

    def post(self, request, *args, **kwargs):
        perfil_autor = PerfilAutor.objects.filter(usuario=request.user).first()

        user_form = UserUpdateForm(request.POST, instance=request.user)
        autor_form = PerfilAutorForm(request.POST, request.FILES, instance=perfil_autor)

        if user_form.is_valid() and autor_form.is_valid():
            user_form.save()
            autor_instance = autor_form.save(commit=False)
            autor_instance.usuario = request.user
            autor_instance.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('edit_profile')

        messages.error(request, 'Não foi possível atualizar o perfil. Verifique os campos e tente novamente.')
        return render(request, self.template_name, {
            'user_form': user_form,
            'autor_form': autor_form,
        })
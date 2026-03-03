from django import forms
from django.forms.widgets import ClearableFileInput
from django.contrib.auth.models import User
from .models import Post, Categoria, Comentario, PerfilAutor
from django.contrib.auth.forms import AuthenticationForm


# Widget que remove o texto "Currently:" exibido por padrão
class CustomClearableFileInput(ClearableFileInput):
    initial_text = ''
    input_text = 'Alterar'
    clear_checkbox_label = 'Remover'

# ------------------------------
# FORM PARA POST
# ------------------------------

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'categoria', 'conteudo', 'imagem', 'imagem_posicao']

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Post'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Conteúdo do Post'}),
            'imagem': CustomClearableFileInput(attrs={'class': 'form-control-file'}),
            'imagem_posicao': forms.Select(attrs={'class': 'form-control'}),
        }

#----------------------------------------------------------------------------------
class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'categoria', 'conteudo', 'imagem', 'imagem_posicao']

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Post'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Conteúdo do Post'}),
            'imagem': CustomClearableFileInput(attrs={'class': 'form-control-file'}),
            'imagem_posicao': forms.Select(attrs={'class': 'form-control'}),
        }

#----------------------------------------------------------------------------------

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuário'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'})
    )

#----------------------------------------------------------------------------------
# FORM PARA CATEGORIA
# ------------------------------
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da categoria'
            }),
        }

#----------------------------------------------------------------------------------

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']

        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escreva um comentário...'
            })
        }
#----------------------------------------------------------------------------------

class PerfilAutorForm(forms.ModelForm):
    class Meta: 
        model = PerfilAutor
        fields = ['bio', 'foto', 'redes_sociais']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows':4, 'placeholder': 'Escreva uma bio curta...'}),
            'foto': CustomClearableFileInput(attrs={'class': 'form-control-file'}),
            'redes_sociais': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Cole uma URL por linha\nhttps://instagram.com/seuusuario\nhttps://github.com/seuusuario'
            }),
        }

#----------------------------------------------------------------------------------
class UsuarioForm(forms.ModelForm):
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar senha'}),
        label='Confirmar senha',
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)

        # Guarda o hash original para evitar que o ModelForm zere a senha
        # quando o campo 'password' vier vazio no POST.
        self._original_password_hash = self.instance.password if self.instance and self.instance.pk else None

        self.fields['password'].required = False

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nome de usuário'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Primeiro Nome'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Sobrenome'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})

    def clean(self):
        cleaned_data = super().clean()
        password = (cleaned_data.get('password') or '').strip()
        confirm_password = (cleaned_data.get('confirm_password') or '').strip()

        # Se o usuário não informou senha, não altera a senha atual.
        if not password and not confirm_password:
            return cleaned_data

        # Se informou um dos campos, exige ambos.
        if password and not confirm_password:
            self.add_error('confirm_password', 'Confirme a senha.')
            return cleaned_data

        if confirm_password and not password:
            self.add_error('password', 'Informe a senha.')
            return cleaned_data

        if password != confirm_password:
            self.add_error('confirm_password', 'As senhas não conferem.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        password = (self.cleaned_data.get('password') or '').strip()
        if password:
            user.set_password(password)
        else:
            # Evita sobrescrever a senha atual com string vazia.
            if self._original_password_hash:
                user.password = self._original_password_hash

        if commit:
            user.save()
            self.save_m2m()

        return user
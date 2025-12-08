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
        fields = ['titulo', 'autor', 'categorias', 'conteudo', 'imagem']

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Post'}),
            'autor': forms.Select(attrs={'class': 'form-control'}),
            'categorias': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Conteúdo do Post'}),
            'imagem': CustomClearableFileInput(attrs={'class': 'form-control-file'}),
        }

#----------------------------------------------------------------------------------
class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'conteudo', 'imagem']

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Post'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Conteúdo do Post'}),
            'imagem': CustomClearableFileInput(attrs={'class': 'form-control-file'}),
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
            'redes_sociais': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://seusite.com'}),
        }


#----------------------------------------------------------------------------------
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
        }
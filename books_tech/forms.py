from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Post


# Widget que remove o texto "Currently:" exibido por padrão
class CustomClearableFileInput(ClearableFileInput):
    initial_text = ''
    input_text = 'Alterar'
    clear_checkbox_label = 'Remover'


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'autor', 'conteudo', 'imagem']

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Post'}),
            'autor': forms.Select(attrs={'class': 'form-control'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Conteúdo do Post'}),
            'imagem': CustomClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'conteudo', 'imagem']

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Post'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Conteúdo do Post'}),
            'imagem': CustomClearableFileInput(attrs={'class': 'form-control-file'}),
        }
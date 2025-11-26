from django import forms
from .models import Post


'''class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nome', 'email', 'senha']
'''

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'conteudo', 'imagem']
from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import Post

    username = forms.CharField(label='Usuário', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'nome de usuário'
    }))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Senha'
    }))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username')
        password = cleaned.get('password')

        if username and password:
            try:
                user_obj = User.objects.get(username=username)
            except User.DoesNotExist:
                raise forms.ValidationError('Usuário ou senha inválidos.')

            user = authenticate(self.request, username=user_obj.get_username(), password=password)
            if user is None:
                raise forms.ValidationError('Usuário ou senha inválidos.')

            self.user_cache = user

        return cleaned

    def get_user(self):
        return self.user_cache

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'conteudo', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do post'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Escreva seu post aqui...'}),
        }

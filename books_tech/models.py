from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    def __str__(self):
        return self.get_username()


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)
    conteudo = models.TextField('')
    imagem = models.ImageField(upload_to='posts/', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        autor_name = self.autor.username if self.autor else 'Anônimo'
        return f"{self.titulo} | {autor_name}"


class Autor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nome
    
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descricao = models.TextField('')

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name="comentarios")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField('')

    def __str__(self):
        return f'Comentário de {self.usuario} sobre {self.livro}'
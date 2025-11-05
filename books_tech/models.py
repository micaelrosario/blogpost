from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)
    conteudo = models.TextField('')

    def __str__(self):
        return self.titulo + ' | ' + str(self.autor)


class Usuario(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
    
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
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField('')

    def __str__(self):
        return f'Comentário de {self.usuario} sobre {self.livro}'
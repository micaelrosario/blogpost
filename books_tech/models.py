from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    categorias = models.ManyToManyField('Categoria', related_name="posts", default='coding')
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to='posts/', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.titulo} - {self.autor}" if self.autor else f"{self.titulo} - Autor desconhecido"

    def get_absolute_url(self):
        return reverse('books_tech:post_detail', args=[str(self.id)])


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor}"


class PerfilAutor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    foto = models.ImageField(upload_to="autores/")
    redes_sociais = models.URLField(blank=True, null=True)

from django.db import models
from django.ontrib.auth.models import AbstractUser

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to='posts/', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return self.titulo

class Usuario(AbstractUser):
    
    def __str__(self):
        return self.get_username()